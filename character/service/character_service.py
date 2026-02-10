from character.character import Character
from character.character_schema import CreateCharacterSchema, UpdateCharacterSchema
from character.exceptions.character_exception import CharacterException
from character.repository.character_repository import CharacterRepository


class CharacterService:

    def __init__(self, repository: CharacterRepository):
        self.repository = repository

    def create(self, data: CreateCharacterSchema) -> Character:
        if data.health_points <= 0:
            raise CharacterException("health_points must be greater than 0")

        character = Character(
            name=data.name,
            health_points=data.health_points,
            attack=data.attack,
            defense=data.defense,
        )
        return self.repository.create(character)

    def get_by_id(self, character_id: int) -> Character | None:
        return self.repository.get_by_id(character_id)

    def get_all(self) -> list[Character]:
        return self.repository.get_all()

    def update(
        self, character_id: int, data: UpdateCharacterSchema
    ) -> Character | None:
        update_data = data.model_dump(exclude_unset=True)
        return self.repository.update(character_id, update_data)

    def delete(self, character_id: int) -> bool:
        return self.repository.delete(character_id)
