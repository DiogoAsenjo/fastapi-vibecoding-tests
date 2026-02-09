from pydantic import BaseModel


class CreateCharacterSchema(BaseModel):
    name: str
    health_points: int
    attack: int
    defense: int


class UpdateCharacterSchema(BaseModel):
    name: str | None = None
    health_points: int | None = None
    attack: int | None = None
    defense: int | None = None


class CharacterResponse(BaseModel):
    id: int
    name: str
    health_points: int
    attack: int
    defense: int

    model_config = {"from_attributes": True}
