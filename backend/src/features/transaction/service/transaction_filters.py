"""거래내역 필터링 로직"""
import pandas as pd
from typing import Optional

from src.features.transaction.model.transaction import TransactionQuery


def filter_transactions(
    df: pd.DataFrame,
    query: TransactionQuery
) -> pd.DataFrame:
    """거래내역 필터링"""
    df = _filter_by_category(df, query.category)
    df = _filter_by_date_range(df, query.start_date, query.end_date)
    df = _filter_by_merchant(df, query.merchant)
    df = _filter_by_payment_method(df, query.payment_method)
    df = _filter_by_time_range(df, query.time_range)
    df = _filter_by_weekend(df, query.is_weekend)
    df = _filter_by_early_month(df, query.early_month)
    return df


def _filter_by_category(df: pd.DataFrame, category: Optional[str]) -> pd.DataFrame:
    """카테고리 필터링"""
    if category:
        return df[df["대분류"] == category]
    return df


def _filter_by_date_range(
    df: pd.DataFrame, 
    start_date: Optional[str], 
    end_date: Optional[str]
) -> pd.DataFrame:
    """날짜 범위 필터링"""
    if start_date:
        df = df[df["거래일시"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["거래일시"] <= pd.to_datetime(end_date)]
    return df


def _filter_by_merchant(df: pd.DataFrame, merchant: Optional[str]) -> pd.DataFrame:
    """상호명 필터링"""
    if merchant:
        return df[df["내용"].str.contains(merchant, na=False)]
    return df


def _filter_by_payment_method(df: pd.DataFrame, payment_method: Optional[str]) -> pd.DataFrame:
    """결제수단 필터링"""
    if payment_method:
        return df[df["결제수단"] == payment_method]
    return df


def _filter_by_time_range(df: pd.DataFrame, time_range: Optional[str]) -> pd.DataFrame:
    """시간대 필터링"""
    if not time_range:
        return df
    
    parts = time_range.split("-")
    if len(parts) != 2:
        return df
    
    start_hour = int(parts[0].split(":")[0])
    end_hour = int(parts[1].split(":")[0])
    hours = df["거래일시"].dt.hour
    
    if start_hour < end_hour:
        return df[(hours >= start_hour) & (hours < end_hour)]
    else:  # 야간 (22:00-06:00)
        return df[(hours >= start_hour) | (hours < end_hour)]


def _filter_by_weekend(df: pd.DataFrame, is_weekend: Optional[bool]) -> pd.DataFrame:
    """주말 필터링"""
    if is_weekend:
        return df[df["거래일시"].dt.dayofweek >= 5]  # 5=토, 6=일
    return df


def _filter_by_early_month(df: pd.DataFrame, early_month: Optional[bool]) -> pd.DataFrame:
    """월 초 필터링 (1~5일)"""
    if early_month:
        return df[df["거래일시"].dt.day <= 5]
    return df