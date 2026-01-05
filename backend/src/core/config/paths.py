"""프로젝트 경로 설정"""
from pathlib import Path

# project root
BASE_DIR = Path(__file__).parent.parent.parent.parent

# directories
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
TESTS_DIR = BASE_DIR / "tests"

# data directories
PROCESSED_DATA_DIR = DATA_DIR / "processed"
RAW_DATA_DIR = DATA_DIR / "raw"

# directories auto creation
for path in [DATA_DIR, LOG_DIR, TESTS_DIR, PROCESSED_DATA_DIR, RAW_DATA_DIR]:
    path.mkdir(parents=True, exist_ok=True)