from app.domains.market_video.application.port.comment_repository_port import CommentRepositoryPort
from app.domains.market_video.application.port.video_repository_port import VideoRepositoryPort
from app.domains.market_video.application.port.youtube_comment_port import YouTubeCommentPort


class SaveVideoCommentsUseCase:
    def __init__(
        self,
        youtube_comment: YouTubeCommentPort,
        video_repository: VideoRepositoryPort,
        comment_repository: CommentRepositoryPort,
    ):
        self.youtube_comment = youtube_comment
        self.video_repository = video_repository
        self.comment_repository = comment_repository

    async def execute(self, video_id: str, max_count: int = 200) -> int:
        video = await self.video_repository.find_by_video_id(video_id)
        if video is None:
            return 0

        raw_comments = await self.youtube_comment.fetch_comments(
            video_id=video_id,
            max_count=max_count,
            order="time",
        )

        seen_ids: set[str] = set()
        unique_comments = []
        for c in raw_comments:
            if c.comment_id not in seen_ids:
                seen_ids.add(c.comment_id)
                unique_comments.append(c)

        return await self.comment_repository.save_all(video_id=video_id, comments=unique_comments)
