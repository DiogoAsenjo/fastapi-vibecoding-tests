from sqlalchemy.orm import Session

from character.character import Character
from character.character_model import CharacterModel


class CharacterRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, character: Character) -> Character:
        db_character = CharacterModel(
            name=character.name,
            health_points=character.health_points,
            attack=character.attack,
            defense=character.defense,
        )
        self.db.add(db_character)
        self.db.commit()
        self.db.refresh(db_character)
        return self._to_entity(db_character)

    def get_by_id(self, character_id: int) -> Character | None:
        db_character = (
            self.db.query(CharacterModel)
            .filter(CharacterModel.id == character_id)
            .first()
        )
        if not db_character:
            return None
        return self._to_entity(db_character)

    def get_all(self) -> list[Character]:
        db_characters = self.db.query(CharacterModel).all()
        return [self._to_entity(c) for c in db_characters]

    def update(self, character_id: int, data: dict) -> Character | None:
        db_character = (
            self.db.query(CharacterModel)
            .filter(CharacterModel.id == character_id)
            .first()
        )
        if not db_character:
            return None

        for key, value in data.items():
            setattr(db_character, key, value)

        self.db.commit()
        self.db.refresh(db_character)
        return self._to_entity(db_character)

    def delete(self, character_id: int) -> bool:
        db_character = (
            self.db.query(CharacterModel)
            .filter(CharacterModel.id == character_id)
            .first()
        )
        if not db_character:
            return False

        self.db.delete(db_character)
        self.db.commit()
        return True

    def _to_entity(self, model: CharacterModel) -> Character:
        """Converte o modelo ORM para a entidade de domínio."""
        return Character(
            id=model.id,
            name=model.name,
            health_points=model.health_points,
            attack=model.attack,
            defense=model.defense,
        )
