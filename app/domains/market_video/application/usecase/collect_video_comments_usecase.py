from app.domains.market_video.application.port.video_repository_port import VideoRepositoryPort
from app.domains.market_video.application.port.youtube_comment_port import YouTubeCommentPort
from app.domains.market_video.application.response.video_comment_response import (
    VideoCommentListResponse,
    VideoCommentResponse,
)

MAX_COMMENTS = 50
DEFAULT_ORDER = "time"


class CollectVideoCommentsUseCase:
    def __init__(
        self,
        youtube_comment: YouTubeCommentPort,
        video_repository: VideoRepositoryPort,
    ):
        self.youtube_comment = youtube_comment
        self.video_repository = video_repository

    async def execute(
        self,
        video_id: str,
        max_count: int = MAX_COMMENTS,
        order: str = DEFAULT_ORDER,
    ) -> VideoCommentListResponse:
        video = await self.video_repository.find_by_video_id(video_id)
        if video is None:
            return VideoCommentListResponse(video_id=video_id, comments=[], total_count=0)

        raw_comments = await self.youtube_comment.fetch_comments(
            video_id=video_id,
            max_count=max_count,
            order=order,
        )

        seen_ids: set[str] = set()
        unique_comments = []
        for c in raw_comments:
            if c.comment_id not in seen_ids:
                seen_ids.add(c.comment_id)
                unique_comments.append(c)

        return VideoCommentListResponse(
            video_id=video_id,
            comments=[
                VideoCommentResponse(
                    comment_id=c.comment_id,
                    author=c.author,
                    content=c.content,
                    published_at=c.published_at,
                    like_count=c.like_count,
                )
                for c in unique_comments
            ],
            total_count=len(unique_comments),
        )
