from pydantic import BaseModel, Field
from typing import Literal
from typing import Optional
from datetime import datetime
from typing import Union



class CreateAssessmentDTO(BaseModel):
    
    assessment_type: Literal["general_test", "detailed_analysis", "image_processing"] = Field(
        ...,
        description="The type of assessment being initiated."
    )

class CreateMessageDTO(BaseModel):

    content: str = Field(
        ...,
        min_length=1,
        description="The text content of the user's message."
    )

class AssessmentResponseDTO(BaseModel):

    assessment_id: str
    user_id: str
    status: str
    created_at: str
    assessment_type: Optional[str] = None
    risk_level: Optional[str] = None
    confidence: Optional[float] = None
    conversation: Optional[list[dict]] = None


class MessageResponseDTO(BaseModel):

    role: Literal["assistant"]
    content: Union[str, dict]
    new_status: Optional[str] = None

class ReportSummaryDTO(BaseModel):
    assessment_id: str
    assessment_type: str
    status: str
    created_at: Optional[str]
    updated_at: Optional[str]
    predicted_class: Optional[str] = None
    confidence: Optional[float] = None
    risk_level: Optional[str] = None
    title: Optional[str] = None

