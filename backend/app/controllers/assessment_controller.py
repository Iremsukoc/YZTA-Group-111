from fastapi import APIRouter, Depends, Path, HTTPException, File, UploadFile, Form, Query
import traceback

from app.dto.assessment.assessment_dto import (
    CreateAssessmentDTO,
    CreateMessageDTO,
    AssessmentResponseDTO,
    MessageResponseDTO,
    ReportSummaryDTO
)
from app.core.dependencies import get_current_user
from app.services.assessment_service import AssessmentService 
from pydantic import BaseModel

assessment_service = AssessmentService()


class ImageUploadDTO(BaseModel):
    model_type: str


class AssessmentController:
    def __init__(self):
        self.router = APIRouter(
            prefix="/assessments",
            tags=["Assessments"]
        )

        self.router.add_api_route(
            "", self.create_new_assessment,
            methods=["POST"], status_code=201,
            response_model=AssessmentResponseDTO
        )

        self.router.add_api_route(
            "/{assessment_id}/messages", self.post_new_message,
            methods=["POST"], response_model=MessageResponseDTO
        )

        self.router.add_api_route(
            "/{assessment_id}/messages", self.get_messages,
            methods=["GET"], response_model=list[MessageResponseDTO]
        )

        self.router.add_api_route(
            "/{assessment_id}/image", self.upload_image,
            methods=["POST"]
        )

        self.router.add_api_route(
            "", self.list_assessments,
            methods=["GET"], response_model=list[AssessmentResponseDTO]
        )

        self.router.add_api_route(
            "/report_summaries", self.get_report_summaries,
            methods=["GET"], response_model=list[ReportSummaryDTO]
        )

        self.router.add_api_route(
            "/{assessment_id}", self.get_assessment_detail,
            methods=["GET"], response_model=AssessmentResponseDTO
        )

    async def create_new_assessment(
        self,
        assessment_data: CreateAssessmentDTO,
        current_user: dict = Depends(get_current_user)
    ) -> AssessmentResponseDTO:
        user_id = current_user.get("uid")
        new_assessment_id = assessment_service.create_assessment_session(
            user_id=user_id,
            assessment_type=assessment_data.assessment_type
        )
        return AssessmentResponseDTO(
            assessment_id=new_assessment_id,
            user_id=user_id,
            status="active",
            created_at="now"
        )

    async def post_new_message(
        self,
        message_data: CreateMessageDTO,
        assessment_id: str = Path(...),
        current_user: dict = Depends(get_current_user)
    ) -> MessageResponseDTO:
        user_id = current_user.get("uid")
        try:
            assistant_response_dict = assessment_service.add_message_to_assessment(
                assessment_id=assessment_id,
                user_id=user_id,
                message_content=message_data.content
            )
            return MessageResponseDTO(
                role="assistant",
                content=assistant_response_dict.get("content"),
                new_status=assistant_response_dict.get("new_status")
            )
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except Exception:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    async def get_messages(
        self,
        assessment_id: str = Path(...),
        current_user: dict = Depends(get_current_user)
    ) -> list[MessageResponseDTO]:
        user_id = current_user.get("uid")
        try:
            messages = assessment_service.get_assessment_messages(assessment_id, user_id)
            return [MessageResponseDTO(**msg) for msg in messages]
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except Exception:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    async def upload_image(
        self,
        assessment_id: str = Path(...),
        image_file: UploadFile = File(...),
        current_user: dict = Depends(get_current_user)
    ):
        user_id = current_user.get("uid")
        try:
            ml_result = await assessment_service.analyze_image(
                user_id, assessment_id, image_file
            )
            return ml_result
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except Exception:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="An unexpected error occurred during ML prediction.")

    async def list_assessments(
        self,
        status: str = Query(None),
        current_user: dict = Depends(get_current_user)
    ) -> list[AssessmentResponseDTO]:
        user_id = current_user.get("uid")
        return assessment_service.get_all_assessments(user_id, status)

    async def get_report_summaries(
        self,
        current_user: dict = Depends(get_current_user)
    ) -> list[ReportSummaryDTO]:
        user_id = current_user.get("uid")
        return assessment_service.get_report_summaries(user_id)

    async def get_assessment_detail(
        self,
        assessment_id: str = Path(...),
        current_user: dict = Depends(get_current_user)
    ) -> AssessmentResponseDTO:
        user_id = current_user.get("uid")
        try:
            assessment_data = assessment_service.get_assessment_detail(assessment_id, user_id)
            return AssessmentResponseDTO(**assessment_data)
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except Exception:
            traceback.print_exc()
            raise HTTPException(status_code=404, detail="Assessment not found")
