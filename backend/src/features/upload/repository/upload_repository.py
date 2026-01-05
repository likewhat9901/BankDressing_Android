import pandas as pd
from pathlib import Path

from src.core.config.paths import RAW_DATA_DIR


def save_uploaded_file(filename: str, content: bytes) -> Path:
    """업로드된 파일 저장"""

    # 파일 저장
    file_path = RAW_DATA_DIR / filename
    try:
        with open(file_path, "wb") as f:
            f.write(content)
        return file_path
    except Exception as e:
        raise ValueError(f"파일 저장 실패: {e}")


def read_excel_to_dataframe(path: Path, sheet_name: int = 1) -> pd.DataFrame:
    """엑셀 → DataFrame (I/O 담당)"""
    return pd.read_excel(path, sheet_name)

def save_dataframe_to_parquet(df: pd.DataFrame, path: Path) -> None:
    """DataFrame → Parquet (I/O 담당)"""
    df.to_parquet(path, index=False)



