from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.market_video.application.port.comment_repository_port import CommentRepositoryPort
from app.domains.market_video.domain.entity.video_comment import VideoComment
from app.domains.market_video.infrastructure.mapper.video_comment_mapper import VideoCommentMapper
from app.domains.market_video.infrastructure.orm.video_comment_orm import VideoCommentORM


class CommentPersistenceAdapter(CommentRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save_all(self, video_id: str, comments: list[VideoComment]) -> int:
        existing_result = await self._session.execute(
            select(VideoCommentORM.comment_id).where(VideoCommentORM.video_id == video_id)
        )
        existing_ids = {row[0] for row in existing_result.fetchall()}

        new_comments = [c for c in comments if c.comment_id not in existing_ids]
        for comment in new_comments:
            self._session.add(VideoCommentMapper.to_orm(comment, video_id))

        await self._session.commit()
        return len(new_comments)

    async def find_contents_by_video_id(self, video_id: str) -> list[str]:
        result = await self._session.execute(
            select(VideoCommentORM.content).where(VideoCommentORM.video_id == video_id)
        )
        return [row[0] for row in result.fetchall()]

    async def find_all_contents(self) -> list[str]:
        result = await self._session.execute(select(VideoCommentORM.content))
        return [row[0] for row in result.fetchall()]
