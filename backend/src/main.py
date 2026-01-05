import logging
from contextlib import asynccontextmanager

# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# 로컬 - core
from src.core.config.paths import LOG_DIR
from src.core.config.settings import ALLOWED_ORIGINS
from src.core.log.logger import configure_logging
from src.core.exceptions.http_exceptions import setup_http_exception_handlers

# 로컬 - features (라우터)
from src.features.upload.router.upload_router import upload_router
from src.features.analysis.overspending.router.analysis_router import analysis_router
from src.features.analysis.overspending.router.rule_router import rule_router
from src.features.transaction.router.transaction_router import transaction_router
from src.features.analysis.statistic.router.statistic_router import statistic_router
from src.features.saving.router.saving_router import saving_router
from src.features.user.router.personality_router import personality_router
from src.features.inquiry.router.inquiry_router import inquiry_router

# 로깅 설정
configure_logging(LOG_DIR, debug=True)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("앱 시작")
    logger.info(f"로그파일 경로: {LOG_DIR}")
    yield
    # Shutdown (필요시)

# 앱 설정
app = FastAPI(
    title="Banksalad 과소비 분석 API",
    description="뱅크샐러드 데이터 기반 과소비 패턴 분석",
    version="1.0.0",
    lifespan=lifespan,
)

# 예외 핸들러 등록
setup_http_exception_handlers(app)

# Flutter 앱에서 호출할 수 있도록 CORS 설정
app.add_middleware(
    CORSMiddleware,
    # TODO: 프로덕션 배포 시 특정 도메인으로 제한
    allow_origins=ALLOWED_ORIGINS,  # 개발 중에는 전체 허용
    allow_credentials=ALLOWED_ORIGINS != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(upload_router)
app.include_router(analysis_router)
app.include_router(rule_router)
app.include_router(transaction_router)
app.include_router(statistic_router)
app.include_router(saving_router)
app.include_router(personality_router)
app.include_router(inquiry_router)

# 경로 핸들러
@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <h1>Banksalad API</h1>
    <ul>
        <li><a href="/health">/health</a></li>
        <li><a href="/docs">/docs (Swagger)</a></li>
    </ul>
    """

@app.get("/health")
def health_check():
    return {"status": "healthy"}