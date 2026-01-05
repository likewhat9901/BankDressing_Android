ALLOWED_EXCEL_EXTENSIONS = {".xlsx", ".xls"}
# MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

def validate_file_extension(filename: str) -> None:
    """파일 확장자 검증"""
    # 1. 파일명 존재 확인
    if not filename:
        raise ValueError("파일명이 없습니다.")
    
    # 2. 확장자 검증
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXCEL_EXTENSIONS:
        raise ValueError(f"허용되지 않는 파일 형식입니다. 허용: {', '.join(ALLOWED_EXCEL_EXTENSIONS)}")

# TODO: 파일 크기 검증, 경로 순회 공격 방지