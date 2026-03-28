from app.domains.market_video.application.port.video_repository_port import VideoRepositoryPort
from app.domains.market_video.application.port.youtube_channel_port import YouTubeChannelPort
from app.domains.market_video.domain.entity.saved_video import SavedVideo
from app.domains.market_video.domain.service.video_filter_service import VideoFilterService

CHANNEL_IDS = [
    "UCF8AeLlUbEpKju6v1H6p8Eg",  # 한국경제TV
    "UCbMjg2EvXs_RUGW-KrdM3pw",  # SBS Biz
    "UCTHCOPwqNfZ0uiKOvFyhGwg",  # 연합뉴스TV
    "UCcQTRi69dsVYHN3exePtZ1A",  # KBS News
    "UCG9aFJTZ-lMCHAiO1KJsirg",  # MBN
    "UCsU-I-vHLiaMfV_ceaYz5rQ",  # JTBC News
    "UClErHbdZKUnD1NyIUeQWvuQ",  # 머니투데이
    "UC8Sv6O3Ux8ePVqorx8aOBMg",  # 이데일리TV
    "UCnfwIKyFYRuqZzzKBDt6JOA",  # 매일경제TV
]
WITHIN_DAYS = 7


class CollectAndSaveVideosUseCase:
    def __init__(
        self,
        youtube_channel: YouTubeChannelPort,
        video_repository: VideoRepositoryPort,
    ):
        self.youtube_channel = youtube_channel
        self.video_repository = video_repository

    async def execute(self) -> list[SavedVideo]:
        if not CHANNEL_IDS:
            return []

        raw_videos = await self.youtube_channel.fetch_recent_videos(
            channel_ids=CHANNEL_IDS,
            within_days=WITHIN_DAYS,
        )

        filtered = VideoFilterService.filter_and_sort(raw_videos)

        if not filtered:
            return []

        saved: list[SavedVideo] = []
        for video in filtered:
            try:
                result = await self.video_repository.upsert(video)
                saved.append(result)
            except Exception as e:
                print(f"[CollectVideos] video_id={video.video_id} 저장 실패: {e}")
                continue

        return saved
