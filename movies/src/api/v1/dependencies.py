from fastapi import Query


class PaginateQueryParams:
    """Dependency class to parse pagination query params."""

    def __init__(
        self,
        page_number: int = Query(
            1,
            title="Страница",
            description="Номер страницы",
            ge=1,
        ),
        page_size: int = Query(
            50,
            title="Размер страницы",
            description="Количество записей на странице",
            ge=1,
            le=500,
        ),
    ):
        self.page_number = str(page_number)
        self.page_size = str(page_size)
