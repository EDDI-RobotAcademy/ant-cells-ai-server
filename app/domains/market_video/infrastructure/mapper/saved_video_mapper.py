from app.domains.market_video.domain.entity.saved_video import SavedVideo
from app.domains.market_video.infrastructure.orm.saved_video_orm import SavedVideoORM


class SavedVideoMapper:
    @staticmethod
    def to_entity(orm: SavedVideoORM) -> SavedVideo:
        return SavedVideo(
            video_id=orm.video_id,
            title=orm.title,
            channel_name=orm.channel_name,
            published_at=orm.published_at,
            view_count=orm.view_count,
            thumbnail_url=orm.thumbnail_url,
            video_url=orm.video_url,
        )

    @staticmethod
    def to_orm(entity: SavedVideo) -> SavedVideoORM:
        return SavedVideoORM(
            video_id=entity.video_id,
            title=entity.title,
            channel_name=entity.channel_name,
            published_at=entity.published_at,
            view_count=entity.view_count,
            thumbnail_url=entity.thumbnail_url,
            video_url=entity.video_url,
        )
