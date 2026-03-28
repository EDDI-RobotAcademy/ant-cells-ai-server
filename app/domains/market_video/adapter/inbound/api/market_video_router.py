from fastapi import APIRouter, Cookie, Depends

from app.domains.market_video.application.response.noun_frequency_response import NounFrequencyResponse
from app.domains.market_video.application.response.video_comment_response import VideoCommentListResponse
from app.domains.market_video.application.response.video_list_response import VideoListResponse
from app.domains.market_video.application.usecase.collect_and_save_videos_usecase import CollectAndSaveVideosUseCase
from app.domains.market_video.application.usecase.collect_video_comments_usecase import CollectVideoCommentsUseCase
from app.domains.market_video.application.usecase.extract_nouns_usecase import ExtractNounsUseCase
from app.domains.market_video.application.usecase.get_video_list_usecase import GetVideoListUseCase
from app.domains.market_video.application.usecase.save_video_comments_usecase import SaveVideoCommentsUseCase
from app.domains.market_video.di import (
    get_collect_and_save_usecase,
    get_collect_video_comments_usecase,
    get_extract_nouns_usecase,
    get_save_video_comments_usecase,
    get_video_list_usecase,
)

router = APIRouter(prefix="/youtube", tags=["market_video"])


@router.get("/list", response_model=VideoListResponse)
async def get_video_list(
    page: int = 1,
    user_token: str = Cookie(..., alias="user_token"),
    usecase: GetVideoListUseCase = Depends(get_video_list_usecase),
):
    return await usecase.execute(user_token=user_token, page=page)


@router.post("/collect")
async def collect_videos(
    usecase: CollectAndSaveVideosUseCase = Depends(get_collect_and_save_usecase),
):
    saved = await usecase.execute()
    return {"saved_count": len(saved)}


@router.get("/comments", response_model=VideoCommentListResponse)
async def get_video_comments(
    video_id: str,
    max_count: int = 50,
    order: str = "time",
    user_token: str = Cookie(..., alias="user_token"),
    usecase: CollectVideoCommentsUseCase = Depends(get_collect_video_comments_usecase),
):
    return await usecase.execute(video_id=video_id, max_count=max_count, order=order)


@router.post("/comments/save")
async def save_video_comments(
    video_id: str,
    max_count: int = 200,
    usecase: SaveVideoCommentsUseCase = Depends(get_save_video_comments_usecase),
):
    saved_count = await usecase.execute(video_id=video_id, max_count=max_count)
    return {"video_id": video_id, "saved_count": saved_count}


@router.get("/nouns", response_model=NounFrequencyResponse)
async def get_nouns(
    video_id: str = None,
    top_n: int = 30,
    usecase: ExtractNounsUseCase = Depends(get_extract_nouns_usecase),
):
    return await usecase.execute(video_id=video_id, top_n=top_n)
