from pydantic import BaseModel, Field


class Live(BaseModel):
    live: bool
    title: str | None = None
    category: str | None = None
    tags: list[str] = Field(default_factory=list)
    viewer: int = 0

    @classmethod
    def offline(cls) -> "Live":
        return cls(live=False)

    @classmethod
    def online(
        cls,
        *,
        title: str,
        category: str,
        tags: list[str],
        viewer: int,
    ) -> "Live":
        return cls(
            live=True,
            title=title,
            category=category,
            tags=tags,
            viewer=viewer,
        )
