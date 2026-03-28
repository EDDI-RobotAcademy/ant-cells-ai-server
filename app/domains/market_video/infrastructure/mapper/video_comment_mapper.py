from app.domains.market_video.domain.entity.video_comment import VideoComment
from app.domains.market_video.infrastructure.orm.video_comment_orm import VideoCommentORM


class VideoCommentMapper:
    @staticmethod
    def to_entity(orm: VideoCommentORM) -> VideoComment:
        return VideoComment(
            comment_id=orm.comment_id,
            author=orm.author,
            content=orm.content,
            published_at=orm.published_at,
            like_count=orm.like_count,
        )

    @staticmethod
    def to_orm(entity: VideoComment, video_id: str) -> VideoCommentORM:
        return VideoCommentORM(
            comment_id=entity.comment_id,
            video_id=video_id,
            author=entity.author,
            content=entity.content,
            published_at=entity.published_at,
            like_count=entity.like_count,
        )
