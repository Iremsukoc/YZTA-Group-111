from pydantic import BaseModel

class GeneralTestChatHistoryResponseDTO(BaseModel):
    user_id: str
    session_id: str
    history: list
