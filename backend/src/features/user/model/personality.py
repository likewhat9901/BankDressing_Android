from pydantic import BaseModel

# ======================= personality scores model =======================
class PersonalityScores(BaseModel):
    """소비 성향 점수"""
    planning: float
    saving: float

# ======================= personality model =======================
class Personality(BaseModel):
    """소비 성향 정보"""
    code: str           # ANT, FOX, SQUIRREL, LION
    animal: str         # 개미, 여우, 다람쥐, 사자
    name: str           # 착실한 저축가, 전략적 투자자 등
    emoji: str          # 🐜, 🦊, 🐿️, 🦁
    image: str          # 캐릭터 이미지 경로
    description: str    # 성향 설명
    traits: list[str]   # 성향 특징
    strength: str       # 강점
    weakness: str       # 약점
    advice: str         # 조언

    def to_response(self, scores: dict) -> dict:
        """API 응답 생성"""
        return _build_response_dict(self, scores)

# ======================= response builder =======================
def _build_response_dict(personality: Personality, scores: dict) -> dict:
    """API 응답 dict 구성"""
    return {
        "type": personality.code,
        "animal": personality.animal,
        "name": personality.name,
        "emoji": personality.emoji,
        "image": personality.image,
        "description": personality.description,
        "traits": personality.traits,
        "strength": personality.strength,
        "weakness": personality.weakness,
        "advice": personality.advice,
        "scores": {
            "planning": round(scores.get("planning", 0.5), 2),
            "saving": round(scores.get("saving", 0.5), 2),
        },
    }