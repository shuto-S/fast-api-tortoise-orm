from pydantic import BaseModel, Field

class ItemModel(BaseModel):
    name: str = Field(None, min_length=2, max_length=5)
    description: str = Field(None, max_length=100)
