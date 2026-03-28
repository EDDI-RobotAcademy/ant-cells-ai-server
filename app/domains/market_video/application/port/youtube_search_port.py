from abc import ABC, abstractmethod
from typing import Optional
from app.domains.market_video.domain.entity.video_item import VideoItem


class YouTubeSearchPort(ABC):
    @abstractmethod
    async def search(
        self,
        page_token: Optional[str] = None,
    ) -> tuple[list[VideoItem], Optional[str], Optional[str], int]:
        """YouTube에서 방산주 관련 영상을 검색한다.

        Returns:
            (items, next_page_token, prev_page_token, total_results)
        """
        pass
