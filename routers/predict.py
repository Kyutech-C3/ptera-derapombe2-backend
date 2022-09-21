import cv2
from schemas.predict import PredictResult
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from strawberry.file_uploads import Upload
from functions.predict import predict as predict_function
import requests
import numpy as np

def predict(file: str) -> PredictResult:
	# try:
	# 	suffix = Path(file.filename).suffix
	# 	with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
	# 		shutil.copyfileobj(file.file, tmp)
	# 	tmp_path = Path(tmp.name)
	# finally:
	# 	file.file.close()
	# print(tmp_path)
	frame = cv2.imdecode(np.array(bytearray(requests.get(file).content), dtype=np.uint8), -1)

	return predict_function(frame, file)
