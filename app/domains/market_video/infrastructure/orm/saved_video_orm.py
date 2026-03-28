from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, String

from app.domains.post.infrastructure.orm.post_orm import Base


class SavedVideoORM(Base):
    __tablename__ = "saved_videos"

    video_id = Column(String(50), primary_key=True)
    title = Column(String(500), nullable=False)
    channel_name = Column(String(255), nullable=False)
    published_at = Column(String(50), nullable=False)
    view_count = Column(BigInteger, nullable=False, default=0)
    thumbnail_url = Column(String(1000), nullable=False)
    video_url = Column(String(500), nullable=False)
    saved_at = Column(DateTime, nullable=False, default=datetime.utcnow)
