import json
from pathlib import Path
import logging

from src.core.config.paths import SRC_DIR

logger = logging.getLogger(__name__)


OVERSPENDING_RULES_PATH = SRC_DIR / "features" / "analysis" / "overspending" / "data" / "overspending_rules.json"

# --------------------------------
# public functions
# --------------------------------
def load_rules_from_file(include_disabled: bool = False) -> list[dict]:
    """규칙 파일에서 JSON 데이터 로드
    
    Args:
        include_disabled: 비활성 규칙 포함 여부 (기본값: False)
    
    Returns:
        규칙 리스트 (enabled 필터링 적용)
    """
    # 파일이 없으면 빈 리스트 반환
    if not OVERSPENDING_RULES_PATH.exists():
        logger.warning(f"규칙 파일이 없습니다: {OVERSPENDING_RULES_PATH}. 빈 규칙 리스트를 반환합니다.")
        return []

    data = _load_json_file(OVERSPENDING_RULES_PATH)

    rules = data.get("rules")
    if not isinstance(rules, list):
        raise ValueError("규칙 파일 형식이 올바르지 않습니다")

    # enabled 필터링
    if not include_disabled:
        rules = [r for r in rules if r.get("enabled", True)]

    return rules

def save_rules_to_file(rules: list[dict]) -> bool:
    """과소비 규칙을 JSON 파일에 저장"""
    data = {"rules": rules}
    if not OVERSPENDING_RULES_PATH.exists():
        OVERSPENDING_RULES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OVERSPENDING_RULES_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True


# --------------------------------
# private functions
# --------------------------------
def _load_json_file(path: Path) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # 파일이 없으면 빈 규칙 리스트 반환
        logger.warning(f"규칙 파일이 없습니다: {path}. 빈 규칙 리스트를 반환합니다.")
        return {"rules": []}
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 파싱 실패: {e}")
