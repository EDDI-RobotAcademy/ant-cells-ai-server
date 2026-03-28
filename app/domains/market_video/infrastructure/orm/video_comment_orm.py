from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, Integer, String

from app.domains.post.infrastructure.orm.post_orm import Base


class VideoCommentORM(Base):
    __tablename__ = "video_comments"

    comment_id = Column(String(100), primary_key=True)
    video_id = Column(String(50), nullable=False, index=True)
    author = Column(String(255), nullable=False)
    content = Column(String(5000), nullable=False)
    published_at = Column(String(50), nullable=False)
    like_count = Column(BigInteger, default=0)
    saved_at = Column(DateTime, default=datetime.utcnow)
