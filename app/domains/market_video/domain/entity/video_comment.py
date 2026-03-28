from dataclasses import dataclass


@dataclass
class VideoComment:
    comment_id: str
    author: str
    content: str
    published_at: str
    like_count: int
