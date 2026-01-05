from pydantic import BaseModel
from typing import List, Optional


class OverspendingReason(BaseModel):
    """과소비 이유"""
    type: str
    count: int
    message: str


class OverspendingPattern(BaseModel):
    """과소비 패턴"""
    category: str
    total_amount: int
    reasons: List[OverspendingReason]


class OverspendingPatternsResponse(BaseModel):
    """과소비 패턴 응답"""
    count: int
    patterns: List[OverspendingPattern]


class RecurringPattern(BaseModel):
    """반복 소비 패턴"""
    key: str
    merchant: str
    time_range: str
    day_of_week: Optional[str] = None
    category: str
    payment_method: str
    count: int
    total_amount: int
    average_amount: int
    first_date: str
    last_date: str
    period_days: int
    amounts: List[int]


class RecurringPatternsResponse(BaseModel):
    """반복 소비 패턴 응답"""
    count: int
    patterns: List[RecurringPattern]


class TimeBasedPattern(BaseModel):
    """시간대 소비 패턴"""
    type: str
    name: str
    description: str
    count: int
    total_amount: int
    average_amount: int
    time_range: Optional[str] = None
    days: Optional[str] = None


class TimeBasedPatternsResponse(BaseModel):
    """시간대 소비 패턴 응답"""
    count: int
    patterns: List[TimeBasedPattern]