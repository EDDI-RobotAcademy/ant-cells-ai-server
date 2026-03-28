import httpx

from app.domains.market_video.application.port.youtube_comment_port import YouTubeCommentPort
from app.domains.market_video.domain.entity.video_comment import VideoComment

YOUTUBE_COMMENT_URL = "https://www.googleapis.com/youtube/v3/commentThreads"


class YouTubeCommentAdapter(YouTubeCommentPort):
    def __init__(self, api_key: str):
        self._api_key = api_key

    async def fetch_comments(
        self,
        video_id: str,
        max_count: int,
        order: str,
    ) -> list[VideoComment]:
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": min(max_count, 100),
            "order": order,
            "key": self._api_key,
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(YOUTUBE_COMMENT_URL, params=params, timeout=10.0)

                if response.status_code in (403, 404):
                    return []

                response.raise_for_status()
                data = response.json()
        except Exception as e:
            print(f"[YouTubeComment] video_id={video_id} 댓글 조회 실패: {e}")
            return []

        comments = []
        for item in data.get("items", []):
            snippet = (
                item.get("snippet", {})
                .get("topLevelComment", {})
                .get("snippet", {})
            )
            content = snippet.get("textDisplay", "").strip()
            if not content:
                continue
            comments.append(
                VideoComment(
                    comment_id=item.get("id", ""),
                    author=snippet.get("authorDisplayName", ""),
                    content=content,
                    published_at=snippet.get("publishedAt", ""),
                    like_count=snippet.get("likeCount", 0),
                )
            )

        return comments
