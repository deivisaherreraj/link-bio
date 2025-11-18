from pydantic import BaseModel

class Live(BaseModel):
    live: bool
    title: str
    category: str    
    tags: list[str]
    viewer: int