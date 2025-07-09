from fastapi import FastAPI
from controllers import auth_controller, user_controller
from fastapi.middleware.cors import CORSMiddleware
from core.firebase_config import initialize_firebase_app

app = FastAPI(
    title="YZTA-Bootcamp Health Assistant API",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
        
        initialize_firebase_app()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Geliştirme için şimdilik hepsi, sonra düzenlenmeli
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router)
app.include_router(user_controller.router)

@app.get("/")
def read_root():
    return {"message": "API is running..."}
