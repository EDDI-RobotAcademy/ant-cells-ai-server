from abc import ABC, abstractmethod

from app.domains.market_video.domain.entity.video_comment import VideoComment


class YouTubeCommentPort(ABC):
    @abstractmethod
    async def fetch_comments(
        self,
        video_id: str,
        max_count: int,
        order: str,
    ) -> list[VideoComment]:
        """YouTube에서 특정 영상의 댓글을 수집한다.

        Args:
            video_id: YouTube 영상 ID
            max_count: 최대 수집 댓글 수
            order: 정렬 기준 (time | relevance)
        """
        pass
