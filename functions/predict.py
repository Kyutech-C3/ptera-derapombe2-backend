import numpy as np
import cv2
import os, glob
from schemas.predict import PredictResult, SuggestResult
import requests
import json

BASE_MODEL_SERVER_URL = os.environ.get('BASE_MODEL_SERVER_URL')

font = cv2.FONT_HERSHEY_SIMPLEX
alpha, beta = 1.5, -50.0

signList = glob.glob("./assets/image/X100-2/*.png")

sign_name_json_open = open('./assets/SignTypeNameCorrespondenceTable.json', 'r')
sign_name_json_load = json.load(sign_name_json_open)

# 標準標識画像のファイル名から「クラス番号」と「標識名」を得る
signDict = {}
for no, fname in enumerate(signList):
	signName = os.path.basename(fname)        # フォルダー名無しにする
	classNo = int(signName[:2])    # 先頭2文字がクラス番号
	signName = signName[2:-6]    # Sign名の取り出し(クラス番号、'-STD.png' 除去）
	signDict[classNo] = signName

# エッジ強調フィルター
def medianFilter(k, image):
	kernel = np.array([
		[-k / 9, -k / 9, -k / 9],
		[-k / 9, 1 + 8 * k / 9, k / 9],
		[-k / 9, -k / 9, -k / 9]
	], np.float32)
	result = cv2.filter2D(image, -1, kernel).astype(np.uint8)
	return result
	# result = result - 0
	# return np.clip(result, 0, 255).astype(np.uint8)

# 明るさ、コントラスト調整
def brightnessContrastAdjustment(image):
	image = alpha * image + beta
	return np.clip(image, 0, 255).astype(np.uint8)

# 画像の明るさチェック
def checkBrightness(image):
	img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
	img = img.astype('float')
	img /= 255
	sumGray = img.sum()
	meanGray = sumGray/(img.shape[0] * img.shape[1])
	return meanGray

def transImage(imgColor):
	print("transImage")
	imgGray = cv2.cvtColor(imgColor, cv2.COLOR_BGR2GRAY)    # 入力画像をグレースケール化
	imgGray = cv2.GaussianBlur(imgGray, (5, 5), 0)    # 5x5のgaussianフィルターでノイズ抑制
	imgThresh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)    # アダプティブ二値化
	return imgGray, imgThresh

def detectSignFromThresh(imgThresh):
	print("detectSignFromThresh")
	imgR, imgC = imgThresh.shape[:2]
	contours, hierarchy = cv2.findContours(imgThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	wjMin, hjMin = 100, 100    # 最小文字サイズ
	signCont = []        # parentがなく、childがあるcontoursのリスト
	signRectList = []        # 選択された標識外形座標リスト
	if len(contours) > 0:
		for i in range(len(contours)):
			parentNo = hierarchy[0][i][3]    # 0:Next, 1:Prev, 2:Child, 3:Parent
			childNo = hierarchy[0][i][2]
			if parentNo != -1 and childNo > 0:    # parentがなく、childがある輪郭を選択
				signCont.append([contours[i], hierarchy[0][i]])
		for i in range(len(signCont)):
			cont = signCont[i][0]
			(xj, yj, wj, hj) = cv2.boundingRect(cont)        # (x, y , w, h) = 外接矩形の座標を示すタプル。 座標のデータの型はint
			if wj >= wjMin and hj >= hjMin:    # エリアがwjMin x hjMin より大きいならOK（小さなノイズを除去）
				ptj1 = (xj, yj)
				ptj2 = (xj + wj, yj + hj)
				signRectList.append([i, [ptj1, ptj2], cont])
		noRect = len(signRectList)
		rectDelNo = []
		statJ = False
		for i in range(noRect):        # 入れ子になっている輪郭は除外
			statJ = False
			no1, [pti1, pti2], cont = signRectList[i]
			dx = (pti2[0] - pti1[0]) * 0.5
			dy = (pti2[1] - pti1[1]) * 0.5
			for j in range(noRect):
				if i == j:
					continue
				no2, [ptj1, ptj2], cont = signRectList[j]
				statJ = False
				if (pti1[0] - dx) <= ptj1[0] and ptj1[0] <= pti1[0]:    # pxi - dx < pxj < pxi
					if (pti1[1] - dy) <= ptj1[1] and ptj1[1] <= pti1[1]:    # pyi - dy < pyj < pyi
						if pti2[0] <= ptj2[0] and ptj2[0] <= (pti2[0] + dx):    # pxi < pxj < pxi + dx
							if pti2[1] <= ptj2[1] and ptj2[1] <= (pti2[1] + dy):    # pyi < pyj < pyi + dy
								statJ = True    # jが親だった場合、検索終了
								break
			if statJ is True:    # 親があった場合、削除リストにiを追加
				rectDelNo.append(i)
		rectDelNo.reverse()            # 後から順に削除
		for i in range(len(rectDelNo)):
			del signRectList[rectDelNo[i]]
	return contours, signRectList

def makeAImgColor(imgColor, pt):
	print("makeAImgColor")
	pt1, pt2 = pt
	if ((pt2[1] - pt1[1]) > 0) and ((pt2[0] - pt1[0]) > 0):
		imgCrop = imgColor[pt1[1]: pt2[1], pt1[0]: pt2[0]]        # [row1 : row2, col1 : col2]
		w = pt2[0] - pt1[0]
		h = pt2[1] - pt1[1]
		ww = round(max(w, h) * 1.1)     # w, hの大きい方の長さwwで正方形画像、余白10%
		spc = np.full((ww, ww, 3), 255, dtype=np.uint8)        # 画像を白に
		wy = (ww - h) // 2    # 高さ方向の余白を計算
		wx = (ww - w) // 2    # 幅方向の余白を計算
		origin = imgCrop.astype('uint8')
		spc[wy:wy + h, wx: wx + w, :] = imgCrop    # 余白の内側に標識画像を入れる
		img50x50 = cv2.resize(spc, (100, 100))  # 50 x 50サイズに揃える
		imgAI = img50x50.astype("float32") / 255        # CNNの場合、入力画像は50x50x3(GBR)
		statOK = True
	else:
		origin = imgColor.copy()
		imgAI = imgColor.copy()
		statOK = False
	return statOK, imgAI, origin

def recognizeSign(imgAI):
	print("recognizeSign")
	headers = {"content-type": "application/json"}
	body = {"inputs": np.array([imgAI]).tolist()}
	r = requests.post(f'https://sign-gress-model-server.azurewebsites.net/v1/models/model:predict', data=json.dumps(body), headers=headers, verify=False)
	r_json = json.loads(r.text)
	probArray = r_json['outputs']
	result = np.argsort(probArray[0])[::-1][:3]    # probArray(np.array)の 最大値のindex(0-10)が検出標識
	prob = np.sort(probArray[0])[::-1][:3]    # 検出標識の確率
	print(f"result: {result}")
	print(f"prob: {prob}")
	return result, prob

def drawResult(allContours, signRectList, recogSignList, imgColor, imgThresh, file_path):
	print("drawResult")
	# folder_name = file_path.split('/')[-1].split('.')[0]
	# print(folder_name)
	# os.mkdir(f'./assets/image/predicted/{folder_name}')
	# cv2.imwrite(f'./assets/image/predicted/{folder_name}/origin.jpg', imgColor)
	rgbIm = imgThresh.copy()
	imgThreshColor = cv2.merge((rgbIm, rgbIm, rgbIm))    # 二値化画像をRGBに
	imgThreshColor = cv2.drawContours(imgThreshColor, allContours, -1, (0, 255, 0), 1)    # 全ての輪郭を「グリーン」で描画
	for i in range(len(recogSignList)):    # 検出したサイン
		signNo, signIndex, signName, prob = recogSignList[i]
		contNo, [pt1, pt2], cont = signRectList[signNo]
		(xb, yb) = pt1
		pttxt = (xb, yb - 10)
		pttxt2 = (xb - 20, yb - 10)
		signNoName = str(signIndex) + ":" + signName + " prob : " + str(prob)
		cv2.putText(imgColor, signNoName, pttxt, font, 0.5, (255, 116, 0), 1, cv2.LINE_AA, False)    # クラス番号と認識標識名を表示
		cv2.rectangle(imgColor, pt1, pt2, (255, 255, 0), 2)    # 検出サイン外形矩形をブルーで囲む
		cv2.rectangle(imgThreshColor, pt1, pt2, (255, 255, 0), 2)    # 検出サイン外形矩形をブルーで囲む
	# cv2.imwrite(f'./assets/image/predicted/{folder_name}/predict_result.jpg', imgColor)
	# cv2.imwrite(f'./assets/image/predicted/{folder_name}/thresh_result.jpg', imgThreshColor)

def contCheck(contNo, cont):
	print("contCheck")
	(xb, yb, wb, hb) = cv2.boundingRect(cont)
	conArea = cv2.contourArea(cont)  # 輪郭の面積計算（単位がピクセルではない）
	# 回転を考慮した外接矩形面積は実態に近い
	rectR = cv2.minAreaRect(cont)        # rectR : ((x,y), (w,h), angle) x,y,w,h,angleはfloat
	box = cv2.boxPoints(rectR)    # 4角のコーナーの座標
	boxNP = np.int0(box)    # 整数に。[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
	conBoxArea = cv2.contourArea(boxNP)  # 輪郭の面積計算 →　単位はピクセルではないので、w x hは使えない
	stat = False if conArea / conBoxArea < 0.4 else True        # 輪郭面積が計算上の矩形面積より小さい場合は対象外
	return stat

def predict(frame, tmp_path) -> PredictResult:
	frame = medianFilter(1, frame)
	# meanGray = checkBrightness(frame)
	frame = brightnessContrastAdjustment(frame)
	imgGray, imgThresh = transImage(frame)        # 解析用の画像変換
	allContours, signRectList = detectSignFromThresh(imgThresh)
# allContours: 検出したすべての輪郭データ（原画に表示）
# signRectList = リスト[no, (p1x, p1y), contours]
	recogSignList = []
	if len(signRectList) > 0:        # サインを１個以上検出した場合
		result = []
		for signNo in range(len(signRectList)):
			print(signNo)
			contNo, [pt1, pt2], cont = signRectList[signNo]
			if contCheck(contNo, cont):    # contoursデータから標識らしさをチェック
				statOK, imgAI, origin = makeAImgColor(frame, [pt1, pt2])    # 認識する50x50のカラー画像に加工(imgAI)
				if statOK:
					print("OK")
					# folder_name = str(tmp_path).split('/')[-1].split('.')[0]
					# # print(f'./assets/image/predicted/{folder_name}/input_img_.jpg')
					# cv2.imwrite(f'./assets/image/predicted/input_img_{signNo}.jpg', origin)
					signIndex, prob = recognizeSign(imgAI)
# signIndex:認識した標識index, prob:確率
					scores = []
					for i in range(3):
						print(f"Recognized  Sign Index {i} = ", signIndex[i], signDict[signIndex[i]], prob[i])
						print(type(prob[i]))
						print(type(signDict[signIndex[i]]))
						scores.append(SuggestResult(score=prob[i], sign_type=int(signIndex[i]), sign_name=sign_name_json_load[int(signIndex[i])]))
					result.append(scores)
				recogSignList.append([signNo, signIndex[0], signDict[signIndex[0]], prob[0]])
		drawResult(allContours, signRectList, recogSignList, frame, imgThresh, str(tmp_path))
		return PredictResult(
			status=True,
			scores=result
		)
	else:
		print("NG! 認識ラベル無し")
		return PredictResult(
			status=False,
			scores=[]
		)
