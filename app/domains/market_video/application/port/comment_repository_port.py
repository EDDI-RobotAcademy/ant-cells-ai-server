from abc import ABC, abstractmethod

from app.domains.market_video.domain.entity.video_comment import VideoComment


class CommentRepositoryPort(ABC):
    @abstractmethod
    async def save_all(self, video_id: str, comments: list[VideoComment]) -> int:
        """댓글 목록을 저장한다. 이미 존재하는 comment_id는 건너뛴다. 저장된 수를 반환한다."""
        pass

    @abstractmethod
    async def find_contents_by_video_id(self, video_id: str) -> list[str]:
        """video_id에 해당하는 모든 댓글 텍스트를 반환한다."""
        pass

    @abstractmethod
    async def find_all_contents(self) -> list[str]:
        """저장된 모든 댓글 텍스트를 반환한다."""
        pass
