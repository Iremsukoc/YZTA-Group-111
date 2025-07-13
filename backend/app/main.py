from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import AuthController, UserController, GeneralTestChatController
from app.services.firebase_service import FirebaseService


app = FastAPI(
    title="YZTA-Bootcamp Health Assistant API",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    FirebaseService.initialize_firebase_app()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Controller'lar
auth_controller = AuthController()
user_controller = UserController()
general_test_chat_controller = GeneralTestChatController()

app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(general_test_chat_controller.router)

@app.get("/")
def read_root():
    return {"message": "API is running..."}


def main():
    import uvicorn
    uvicorn.run("app.main:app", reload=True)