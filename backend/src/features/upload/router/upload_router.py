from fastapi import APIRouter, UploadFile, File

from src.features.upload.service.upload_service import process_excel_upload
from src.features.upload.util.file_validation import validate_file_extension

upload_router = APIRouter(prefix="/upload", tags=["업로드"])

@upload_router.post("/excel")
async def upload_excel(file: UploadFile = File(...)):
    """엑셀 파일 업로드 및 변환"""

    # 1. 파일 확장자 검증
    if not file.filename:
        raise ValueError("파일명이 없습니다.")
    validate_file_extension(file.filename)
    
    # 2. 파일 내용 읽기
    content = await file.read()
    
    # 3. 파일 업로드 및 변환
    result = process_excel_upload(file.filename, content)

    # 4. 결과 반환
    return {
        "status": "success",
        "message": "엑셀 파일 업로드 및 변환 완료",
        "row_count": result["row_count"],
    }