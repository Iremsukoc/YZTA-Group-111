from pydantic import BaseModel

class StartGeneralTestChatResponseDTO(BaseModel):
    session_id: str
    message: str
