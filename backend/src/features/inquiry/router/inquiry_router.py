from fastapi import APIRouter

from src.features.inquiry.model.inquiry import InquiryRequest
from src.features.inquiry.service.email_service import send_inquiry_email


inquiry_router = APIRouter(prefix="/inquiry", tags=["문의"])


@inquiry_router.post("/")
def submit_inquiry(request: InquiryRequest):
    """문의 제출"""
    send_inquiry_email(
        subject=request.subject,
        body=request.body,
        sender_email=request.email
    )
    return {"status": "success", "message": "문의가 접수되었습니다"}