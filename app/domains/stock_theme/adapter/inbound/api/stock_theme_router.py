from typing import Optional

from fastapi import APIRouter, Depends

from app.domains.stock_theme.application.response.stock_theme_response import StockThemeListResponse
from app.domains.stock_theme.application.usecase.get_stock_themes_usecase import GetStockThemesUseCase
from app.domains.stock_theme.di import get_stock_themes_usecase

router = APIRouter(prefix="/stock-themes", tags=["stock_theme"])


@router.get("", response_model=StockThemeListResponse)
async def get_stock_themes(
    theme: Optional[str] = None,
    usecase: GetStockThemesUseCase = Depends(get_stock_themes_usecase),
):
    return await usecase.execute(theme=theme)
