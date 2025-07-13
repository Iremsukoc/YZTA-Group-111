from fastapi import APIRouter, Depends, HTTPException
from app.services.general_test_chat_service import GeneralTestChatService
from app.dto.general_test_chat.start_general_test_chat_request_dto import StartGeneralTestChatRequestDTO
from app.dto.general_test_chat.start_general_test_chat_response_dto import StartGeneralTestChatResponseDTO
from app.dto.general_test_chat.general_test_chat_message_request_dto import GeneralTestChatMessageRequestDTO
from app.dto.general_test_chat.general_test_chat_history_response_dto import GeneralTestChatHistoryResponseDTO

class GeneralTestChatController:
    def __init__(self):
        self.router = APIRouter(prefix="/chat", tags=["Chat"])
        self._setup_routes()

    def _setup_routes(self):
        self.router.add_api_route(
            path="/start",
            endpoint=self.start_chat,
            methods=["POST"]
        )
        self.router.add_api_route(
            path="/send",
            endpoint=self.send_chat_message,
            methods=["POST"]
        )
        self.router.add_api_route(
            path="/history/{user_id}/{session_id}",
            endpoint=self.get_history,
            methods=["GET"]
        )

    async def start_chat(
        self, 
        request: StartGeneralTestChatRequestDTO,
        service: GeneralTestChatService = Depends()
    ) -> StartGeneralTestChatResponseDTO:
        session_id = service.start_new_chat(request.user_id)
        return StartGeneralTestChatResponseDTO(session_id=session_id, message="Chat session started.")

    async def send_chat_message(
        self, 
        request: GeneralTestChatMessageRequestDTO,
        service: GeneralTestChatService = Depends()
    ):
        try:
            response = service.send_message(request.user_id, request.session_id, request.message)
            return {"response": response}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_history(
        self, 
        user_id: str, 
        session_id: str,
        service: GeneralTestChatService = Depends()
    ) -> GeneralTestChatHistoryResponseDTO:
        history = service.get_chat_history(user_id, session_id)
        return GeneralTestChatHistoryResponseDTO(user_id=user_id, session_id=session_id, history=history)