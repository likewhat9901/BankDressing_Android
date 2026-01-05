import pandas as pd


def enrich_with_analysis_data(df: pd.DataFrame) -> pd.DataFrame:
    """시간, 주, 월 데이터 추가"""
    df["hour"] = df["거래일시"].dt.hour
    df["week"] = df["거래일시"].dt.isocalendar().week
    df["month"] = df["거래일시"].dt.to_period("M")
    return df