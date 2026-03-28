from datetime import datetime, timedelta, timezone

import httpx

from app.domains.market_video.application.port.youtube_channel_port import YouTubeChannelPort
from app.domains.market_video.domain.entity.saved_video import SavedVideo

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
MAX_RESULTS_PER_CHANNEL = 50


class YouTubeChannelAdapter(YouTubeChannelPort):
    def __init__(self, api_key: str):
        self._api_key = api_key

    async def fetch_recent_videos(
        self,
        channel_ids: list[str],
        within_days: int,
    ) -> list[SavedVideo]:
        published_after = (
            datetime.now(timezone.utc) - timedelta(days=within_days)
        ).strftime("%Y-%m-%dT%H:%M:%SZ")

        async with httpx.AsyncClient() as client:
            all_search_items: list[dict] = []
            for channel_id in channel_ids:
                items = await self._search_channel(client, channel_id, published_after)
                all_search_items.extend(items)

            if not all_search_items:
                return []

            video_ids = [item["id"]["videoId"] for item in all_search_items]
            stats_map = await self._fetch_statistics(client, video_ids)

        return [
            SavedVideo(
                video_id=item["id"]["videoId"],
                title=item["snippet"].get("title", ""),
                channel_name=item["snippet"].get("channelTitle", ""),
                published_at=item["snippet"].get("publishedAt", ""),
                view_count=stats_map.get(item["id"]["videoId"], 0),
                thumbnail_url=(
                    item["snippet"].get("thumbnails", {})
                    .get("medium", {})
                    .get("url", "")
                ),
                video_url=f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            )
            for item in all_search_items
        ]

    async def _search_channel(
        self,
        client: httpx.AsyncClient,
        channel_id: str,
        published_after: str,
    ) -> list[dict]:
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "type": "video",
            "order": "date",
            "maxResults": MAX_RESULTS_PER_CHANNEL,
            "publishedAfter": published_after,
            "key": self._api_key,
        }
        try:
            response = await client.get(YOUTUBE_SEARCH_URL, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json().get("items", [])
        except Exception as e:
            print(f"[YouTubeChannel] channel_id={channel_id} 조회 실패: {e}")
            return []

    async def _fetch_statistics(
        self,
        client: httpx.AsyncClient,
        video_ids: list[str],
    ) -> dict[str, int]:
        stats_map: dict[str, int] = {}
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i : i + 50]
            params = {
                "part": "statistics",
                "id": ",".join(batch),
                "key": self._api_key,
            }
            try:
                response = await client.get(YOUTUBE_VIDEOS_URL, params=params, timeout=10.0)
                response.raise_for_status()
                for item in response.json().get("items", []):
                    stats_map[item["id"]] = int(
                        item.get("statistics", {}).get("viewCount", 0)
                    )
            except Exception as e:
                print(f"[YouTubeChannel] statistics 조회 실패: {e}")
        return stats_map
