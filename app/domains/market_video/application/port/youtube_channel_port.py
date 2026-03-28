from abc import ABC, abstractmethod

from app.domains.market_video.domain.entity.saved_video import SavedVideo


class YouTubeChannelPort(ABC):
    @abstractmethod
    async def fetch_recent_videos(
        self,
        channel_ids: list[str],
        within_days: int,
    ) -> list[SavedVideo]:
        """사전 정의된 채널에서 최근 N일 이내 영상을 조회한다."""
        pass
