# main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from lung_service import LungService

app = FastAPI()
service = LungService("lung_cancer_cnn.h5")

@app.post("/predict-lung")
async def predict_lung(file: UploadFile = File(...)):
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    try:
        image_bytes = await file.read()
        result = service.predict_from_file(image_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
