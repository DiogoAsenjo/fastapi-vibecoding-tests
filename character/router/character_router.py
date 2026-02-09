from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from common.api_response import ApiResponse
from character.character_schema import (
    CreateCharacterSchema,
    UpdateCharacterSchema,
    CharacterResponse,
)
from character.service.character_service import CharacterService
from character.repository.character_repository import CharacterRepository

router = APIRouter(prefix="/characters", tags=["Characters"])


def get_service(db: Session = Depends(get_db)) -> CharacterService:
    repository = CharacterRepository(db)
    return CharacterService(repository)


@router.post(
    "/",
    response_model=ApiResponse[CharacterResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_character(
    data: CreateCharacterSchema,
    service: CharacterService = Depends(get_service),
):
    character = service.create(data)
    return ApiResponse(message="Character created", data=character)


@router.get(
    "/",
    response_model=ApiResponse[list[CharacterResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all_characters(service: CharacterService = Depends(get_service)):
    characters = service.get_all()
    return ApiResponse(message="Characters retrieved", data=characters)


@router.get(
    "/{character_id}",
    response_model=ApiResponse[CharacterResponse],
    status_code=status.HTTP_200_OK,
)
def get_character(
    character_id: int,
    service: CharacterService = Depends(get_service),
):
    character = service.get_by_id(character_id)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found",
        )
    return ApiResponse(message="Character retrieved", data=character)


@router.put(
    "/{character_id}",
    response_model=ApiResponse[CharacterResponse],
    status_code=status.HTTP_200_OK,
)
def update_character(
    character_id: int,
    data: UpdateCharacterSchema,
    service: CharacterService = Depends(get_service),
):
    character = service.update(character_id, data)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found",
        )
    return ApiResponse(message="Character updated", data=character)


@router.delete(
    "/{character_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
)
def delete_character(
    character_id: int,
    service: CharacterService = Depends(get_service),
):
    deleted = service.delete(character_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found",
        )
    return ApiResponse(message="Character deleted", data=None)
