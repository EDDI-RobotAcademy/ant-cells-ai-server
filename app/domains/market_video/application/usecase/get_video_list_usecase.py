from fastapi import HTTPException, status

from app.domains.market_video.application.port.user_token_read_port import UserTokenReadPort
from app.domains.market_video.application.port.video_repository_port import VideoRepositoryPort
from app.domains.market_video.application.response.video_list_response import VideoItemResponse, VideoListResponse

PAGE_SIZE = 9


class GetVideoListUseCase:
    def __init__(
        self,
        video_repository: VideoRepositoryPort,
        user_token_read: UserTokenReadPort,
    ):
        self.video_repository = video_repository
        self.user_token_read = user_token_read

    async def execute(
        self,
        user_token: str,
        page: int = 1,
    ) -> VideoListResponse:
        account_id = await self.user_token_read.get_account_id(user_token)
        if account_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired user token",
            )

        videos, total_results = await self.video_repository.find_all(page=page, size=PAGE_SIZE)

        return VideoListResponse(
            items=[
                VideoItemResponse(
                    video_id=v.video_id,
                    title=v.title,
                    thumbnail_url=v.thumbnail_url,
                    channel_name=v.channel_name,
                    published_at=v.published_at,
                    video_url=v.video_url,
                )
                for v in videos
            ],
            next_page_token=None,
            prev_page_token=None,
            total_results=total_results,
        )
