from app.domains.market_video.domain.entity.saved_video import SavedVideo

DEFENSE_KEYWORDS = [
    "전쟁", "군사", "미사일", "방위산업", "무기", "NATO", "국방",
    "방어", "전투", "핵", "국방부", "전술", "방산", "육군", "해군",
    "공군", "방위", "안보", "전략", "나토", "탄도", "핵무기",
    "K2", "K9", "천무", "레드백", "방산주",
]
MIN_KEYWORD_MATCH = 1  # 제목에서 방산 키워드가 최소 1개 이상 포함되어야 한다


class VideoFilterService:
    @staticmethod
    def filter_and_sort(videos: list[SavedVideo]) -> list[SavedVideo]:
        filtered = [
            v for v in videos
            if VideoFilterService._count_defense_keywords(v.title) >= MIN_KEYWORD_MATCH
        ]
        return sorted(filtered, key=lambda v: v.published_at, reverse=True)

    @staticmethod
    def _count_defense_keywords(title: str) -> int:
        title_lower = title.lower()
        return sum(1 for kw in DEFENSE_KEYWORDS if kw.lower() in title_lower)
