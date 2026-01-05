import pandas as pd


def filter_by_rule(df: pd.DataFrame, rule: dict) -> pd.DataFrame:
    """규칙에 따라 데이터 필터링"""
    # 카테고리 필터링
    filtered_df = df[df["대분류"] == rule["category_filter"]]
    if filtered_df.empty:
        return filtered_df
    
    # 시간대 필터 (선택)
    if "time_filter" in rule:
        start_hour, end_hour = rule["time_filter"]
        if start_hour > end_hour:
            time_mask = (filtered_df["hour"] >= start_hour) | (filtered_df["hour"] < end_hour)
        else:
            time_mask = (filtered_df["hour"] >= start_hour) & (filtered_df["hour"] < end_hour)
        filtered_df = filtered_df[time_mask]
    
    return filtered_df