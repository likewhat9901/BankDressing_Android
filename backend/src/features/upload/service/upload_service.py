import pandas as pd
from pathlib import Path
import logging

from src.core.config.paths import PROCESSED_DATA_DIR
from src.features.upload.repository.upload_repository import read_excel_to_dataframe, save_dataframe_to_parquet, save_uploaded_file


logger = logging.getLogger(__name__)


# ----------------------------------------------------------------
# public functions
# ----------------------------------------------------------------
def process_excel_upload(filename: str, content: bytes) -> dict:
    """엑셀 파일 업로드 처리 (검증 → 저장 → 변환)"""
    try:
        logger.info(f"엑셀 파일 업로드 시작: {filename}")
        
        # 1. 파일 저장
        excel_file_path = save_uploaded_file(filename, content)
        
        # 2. Parquet 변환
        result = _process_excel_to_parquet(excel_file_path)

        # 3. 결과 반환
        return result
 
    except Exception as e:
        logger.error(f"엑셀 업로드 실패: {filename} - {e}", exc_info=True)
        raise


# ----------------------------------------------------------------
# private functions (비즈니스 로직)
# ----------------------------------------------------------------
def _process_excel_to_parquet(excel_file_path: Path, sheet_name: int = 1) -> dict:
    """엑셀 파일을 Parquet로 변환"""
    try:
        logger.info(f"엑셀 파일 '{excel_file_path.name}' 변환 시작")
    
        # 엑셀 파일 읽기 (Repository)
        df = read_excel_to_dataframe(excel_file_path, sheet_name)
        
        # 데이터 가공 (비즈니스 로직)
        df = _process_transaction_data(df)
        
        # DataFrame → Parquet (Repository)
        output_path = PROCESSED_DATA_DIR / "transactions.parquet"
        save_dataframe_to_parquet(df, output_path)
        
        logger.info(f"변환 완료: {len(df)}행 → {output_path}")

        # 결과 반환
        return {
            "row_count": len(df),
        }
    except Exception as e:
        logger.error(f"엑셀 변환 실패: {excel_file_path.name} - {e}", exc_info=True)
        raise

def _process_transaction_data(df: pd.DataFrame) -> pd.DataFrame:
    """거래 데이터 가공"""
    # 거래일시 생성
    df['거래일시'] = pd.to_datetime(df['날짜'], unit='ms') + pd.to_timedelta(df['시간'].astype(str))
    
    # 컬럼 재정렬
    other_cols = [col for col in df.columns if col not in ['거래일시', '날짜', '시간']]
    df = df[['거래일시'] + other_cols]
    
    # ID 컬럼 추가
    df = df.sort_values("거래일시", ascending=False).reset_index(drop=True)
    df['id'] = (len(df) - 1) - df.index
    
    # ID 컬럼을 첫 번째 위치로 이동
    cols = ['id'] + [col for col in df.columns if col != 'id']
    df = df[cols]
    
    return df