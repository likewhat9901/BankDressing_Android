from pydantic import BaseModel

class InquiryRequest(BaseModel):
    subject: str
    body: str
    email: str | None = None  # 발신자 이메일 (선택)