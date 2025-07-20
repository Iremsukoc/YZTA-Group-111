from pydantic import BaseModel

class StartGeneralTestChatRequestDTO(BaseModel):
    user_id: str