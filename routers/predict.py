import cv2
from schemas.predict import PredictResult
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from strawberry.file_uploads import Upload
from functions.predict import predict as predict_function

def predict(file: Upload) -> PredictResult:
	try:
		suffix = Path(file.filename).suffix
		with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
			shutil.copyfileobj(file.file, tmp)
		tmp_path = Path(tmp.name)
	finally:
		file.file.close()
	print(tmp_path)
	frame = cv2.imread(str(tmp_path))

	return predict_function(frame, tmp_path)
