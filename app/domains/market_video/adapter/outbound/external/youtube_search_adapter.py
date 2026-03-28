from typing import Optional

import httpx

from app.domains.market_video.application.port.youtube_search_port import YouTubeSearchPort
from app.domains.market_video.domain.entity.video_item import VideoItem

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
SEARCH_KEYWORD = "한국 방산주 방위산업 주식"
PAGE_SIZE = 9


class YouTubeSearchAdapter(YouTubeSearchPort):
    def __init__(self, api_key: str):
        self._api_key = api_key

    async def search(
        self,
        page_token: Optional[str] = None,
    ) -> tuple[list[VideoItem], Optional[str], Optional[str], int]:
        params = {
            "part": "snippet",
            "q": SEARCH_KEYWORD,
            "type": "video",
            "maxResults": PAGE_SIZE,
            "key": self._api_key,
            "relevanceLanguage": "ko",
        }
        if page_token:
            params["pageToken"] = page_token

        async with httpx.AsyncClient() as client:
            response = await client.get(YOUTUBE_SEARCH_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()

        next_page_token: Optional[str] = data.get("nextPageToken")
        prev_page_token: Optional[str] = data.get("prevPageToken")
        total_results: int = data.get("pageInfo", {}).get("totalResults", 0)

        items = [
            VideoItem(
                video_id=item["id"]["videoId"],
                title=item["snippet"].get("title", ""),
                thumbnail_url=(
                    item["snippet"].get("thumbnails", {})
                    .get("medium", {})
                    .get("url", "")
                ),
                channel_name=item["snippet"].get("channelTitle", ""),
                published_at=item["snippet"].get("publishedAt", ""),
                video_url=f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            )
            for item in data.get("items", [])
        ]

        return items, next_page_token, prev_page_token, total_results
