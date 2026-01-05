"""
로깅 설정 모듈

사용법:
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info("정보 메시지")
    logger.error("에러 메시지", exc_info=True)
"""
import logging
import os
from datetime import datetime
from pathlib import Path


def configure_logging(log_dir: Path, debug: bool | None = None) -> None:
    """
    앱 시작 시 한 번만 호출하여 로깅 설정
    
    Args:
        log_dir: 로그 파일 저장 디렉토리
        debug: 디버그 모드 여부 (None이면 환경변수 DEBUG 확인)
    """
    # 디버그 모드 결정 (인자 > 환경변수 > 기본값)
    if debug is None:
        debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    log_level = logging.DEBUG if debug else logging.INFO
    
    # 로그 디렉토리 생성
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 로그 파일명 (날짜별)
    log_filename = log_dir / f'log_{datetime.now().strftime("%Y%m%d")}.log'
    
    # 포맷 설정
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 파일 핸들러
    file_handler = logging.FileHandler(log_filename, encoding='utf-8', mode='a')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # 기존 핸들러 제거 후 새로 추가
    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # 외부 라이브러리 로그 레벨 조정 (너무 시끄러운 것 방지)
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    # 초기화 완료 로그
    logging.info(f"로깅 초기화 완료 (level={logging.getLevelName(log_level)}, file={log_filename})")
