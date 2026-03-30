from app.domains.stock_theme.application.port.stock_theme_repository_port import StockThemeRepositoryPort
from app.domains.stock_theme.application.request.recommend_stocks_request import RecommendStocksRequest
from app.domains.stock_theme.application.response.stock_recommendation_response import (
    StockRecommendationItemResponse,
    StockRecommendationResponse,
)
from app.domains.stock_theme.domain.service.stock_recommendation_service import StockRecommendationService


class RecommendStocksUseCase:
    def __init__(self, stock_theme_repository: StockThemeRepositoryPort):
        self.stock_theme_repository = stock_theme_repository

    async def execute(self, request: RecommendStocksRequest) -> StockRecommendationResponse:
        keyword_counts = {item.keyword: item.count for item in request.keywords}

        stocks = await self.stock_theme_repository.find_all()
        results = StockRecommendationService.recommend(stocks, keyword_counts)

        return StockRecommendationResponse(
            total=len(results),
            recommendations=[
                StockRecommendationItemResponse(
                    name=r.stock.name,
                    code=r.stock.code,
                    themes=r.stock.themes,
                    matched_keywords=r.matched_keywords,
                    relevance_score=r.relevance_score,
                )
                for r in results
            ],
        )
