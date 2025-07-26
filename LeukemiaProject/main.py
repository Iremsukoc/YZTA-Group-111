from fastapi import FastAPI, File, UploadFile, HTTPException
from ColonProject.colon_service import ColonService
from LungProject.lung_service import LungService
from LeukemiaProject.leukemia_service import LeukemiaService
import tempfile

app = FastAPI()

colon_service = ColonService("ColonProject/model_cnn.h5")
lung_service = LungService("LungProject/lung_cancer_cnn.h5")
leukemia_service = LeukemiaService()

@app.get("/")
def root():
    return {"message": "Cancer Classification API"}

@app.post("/predict/colon")
async def predict_colon(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = colon_service.predict_from_file(image_bytes)
    return {"prediction": result}

@app.post("/predict/lung")
async def predict_lung(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = lung_service.predict_from_file(image_bytes)
    return {"prediction": result}

@app.post("/predict/leukemia")
async def predict_leukemia(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    try:
        image_bytes = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name

        result = leukemia_service.predict_from_file(tmp_path)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")