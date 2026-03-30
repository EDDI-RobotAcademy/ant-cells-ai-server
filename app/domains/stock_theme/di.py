from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.stock_theme.adapter.outbound.persistence.stock_theme_persistence_adapter import StockThemePersistenceAdapter
from app.domains.stock_theme.application.usecase.get_stock_themes_usecase import GetStockThemesUseCase
from app.infrastructure.database.database import get_db_session


def get_stock_themes_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> GetStockThemesUseCase:
    return GetStockThemesUseCase(
        stock_theme_repository=StockThemePersistenceAdapter(session=session),
    )
