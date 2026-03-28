from dataclasses import dataclass


@dataclass
class SavedVideo:
    video_id: str
    title: str
    channel_name: str
    published_at: str  # ISO 8601 format (UTC)
    view_count: int
    thumbnail_url: str
    video_url: str
