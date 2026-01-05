"""거래내역 모델"""
from pydantic import BaseModel
from typing import Optional


# ============================================================
# API 요청 모델
# ============================================================
class TransactionQuery(BaseModel):
    """거래내역 조회 쿼리"""
    limit: int = 50
    offset: int = 0
    category: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    merchant: Optional[str] = None
    payment_method: Optional[str] = None
    time_range: Optional[str] = None
    is_weekend: Optional[bool] = None
    early_month: Optional[bool] = None


class TransactionUpdate(BaseModel):
    """거래내역 수정 요청"""
    description: Optional[str] = None
    amount: Optional[int] = None
    category: Optional[str] = None
    payment_method: Optional[str] = None
    
    def to_repository_dict(self) -> dict:
        """Repository용 dict 변환"""
        mapping = {
            "description": "내용",
            "amount": "금액",
            "category": "대분류",
            "payment_method": "결제수단",
        }
        return {
            mapping[k]: v 
            for k, v in self.model_dump(exclude_none=True).items()
            if k in mapping
        }


# ============================================================
# API 응답 모델
# ============================================================
class TransactionListResponse(BaseModel):
    """거래내역 목록 응답"""
    transactions: list[dict]
    total_count: int
    has_more: bool