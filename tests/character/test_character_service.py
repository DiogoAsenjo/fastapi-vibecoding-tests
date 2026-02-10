from unittest.mock import MagicMock

import pytest

from character.character import Character
from character.character_schema import CreateCharacterSchema
from character.exceptions.character_exception import CharacterException
from character.repository.character_repository import CharacterRepository
from character.service.character_service import CharacterService


@pytest.fixture
def mock_repository():
    return MagicMock(spec=CharacterRepository)


@pytest.fixture
def service(mock_repository):
    return CharacterService(mock_repository)


class TestCreateCharacter:

    def test_create_character_success(self, service, mock_repository):
        # Arrange
        schema = CreateCharacterSchema(
            name="Gandalf", health_points=100, attack=80, defense=50
        )
        mock_repository.create.return_value = Character(
            id=1, name="Gandalf", health_points=100, attack=80, defense=50
        )

        # Act
        result = service.create(schema)

        # Assert
        assert result.id == 1
        assert result.name == "Gandalf"
        assert result.health_points == 100
        assert result.attack == 80
        assert result.defense == 50
        mock_repository.create.assert_called_once()

    def test_create_character_with_zero_health_points_raises_exception(self, service):
        schema = CreateCharacterSchema(
            name="Gandalf", health_points=0, attack=80, defense=50
        )

        with pytest.raises(
            CharacterException, match="health_points must be greater than 0"
        ):
            service.create(schema)

    def test_create_character_with_negative_health_points_raises_exception(
        self, service
    ):
        schema = CreateCharacterSchema(
            name="Gandalf", health_points=-10, attack=80, defense=50
        )

        with pytest.raises(
            CharacterException, match="health_points must be greater than 0"
        ):
            service.create(schema)
