from typing import List
from pydantic import BaseModel


class VideoCommentResponse(BaseModel):
    comment_id: str
    author: str
    content: str
    published_at: str
    like_count: int


class VideoCommentListResponse(BaseModel):
    video_id: str
    comments: List[VideoCommentResponse]
    total_count: int
