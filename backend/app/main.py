from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.auth_controller import AuthController
from app.controllers.user_controller import UserController
from app.controllers.assessment_controller import AssessmentController

from app.config.firebase_config import initialize_firebase_app

app = FastAPI(
    title="regAI Health Assistant API",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    initialize_firebase_app()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthController().router)
app.include_router(UserController().router)
app.include_router(AssessmentController().router)


@app.get("/")
def read_root():
    return {"message": "API is running..."}