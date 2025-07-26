# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from colon_service import ColonService

app = FastAPI()
service = ColonService("model_cnn.h5")

@app.post("/predict-colon")
async def predict_colon(file: UploadFile = File(...)):
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    try:
        image_bytes = await file.read()
        result = service.predict_from_file(image_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
