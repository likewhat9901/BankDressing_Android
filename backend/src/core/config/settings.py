"""앱 전역 설정"""
import os

# 배포 환경 확인 (Railway 등)
IS_DEPLOYMENT = os.getenv("RAILWAY_ENVIRONMENT") is not None or os.getenv("PORT") is not None

# CORS 설정
ALLOWED_ORIGINS = [
    "https://banksalad-backend.up.railway.app",
]