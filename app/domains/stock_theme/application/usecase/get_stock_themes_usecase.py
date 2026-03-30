from typing import Optional

from app.domains.stock_theme.application.port.stock_theme_repository_port import StockThemeRepositoryPort
from app.domains.stock_theme.application.response.stock_theme_response import StockThemeItemResponse, StockThemeListResponse
from app.domains.stock_theme.domain.service.stock_theme_service import StockThemeService


class GetStockThemesUseCase:
    def __init__(self, stock_theme_repository: StockThemeRepositoryPort):
        self.stock_theme_repository = stock_theme_repository

    async def execute(self, theme: Optional[str] = None) -> StockThemeListResponse:
        stocks = await self.stock_theme_repository.find_all()

        if theme:
            stocks = StockThemeService.filter_by_theme(stocks, theme)

        return StockThemeListResponse(
            total=len(stocks),
            stocks=[
                StockThemeItemResponse(id=s.id, name=s.name, code=s.code, themes=s.themes)
                for s in stocks
            ],
        )
