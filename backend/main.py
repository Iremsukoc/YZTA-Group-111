from fastapi import FastAPI
from api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Cancer Risk Assessment API",
    description="Kanser riski belirleme uygulaması için backend servisleri.",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",  # Vite React projesinin varsayılan adresi
    "http://127.0.0.1:5173",
    # Buraya deploy ettiğinizde frontend'inizin domain adresini de ekleyebilirsiniz.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Tüm HTTP metodlarına izin ver (GET, POST, vb.)
    allow_headers=["*"], # Tüm header'lara izin ver
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "API is running..."}
