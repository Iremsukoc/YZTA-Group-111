from pydantic import BaseModel

class GeneralTestChatMessageRequestDTO(BaseModel):
    user_id: str
    session_id: str
    message: str