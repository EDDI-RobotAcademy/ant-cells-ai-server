from typing import List, Optional
from pydantic import BaseModel


class VideoItemResponse(BaseModel):
    video_id: str
    title: str
    thumbnail_url: str
    channel_name: str
    published_at: str
    video_url: str


class VideoListResponse(BaseModel):
    items: List[VideoItemResponse]
    next_page_token: Optional[str]
    prev_page_token: Optional[str]
    total_results: int
