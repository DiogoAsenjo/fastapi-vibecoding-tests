from sqlalchemy import Column, Integer, String

from database import Base


class CharacterModel(Base):
    """Modelo ORM — representa a tabela 'characters' no PostgreSQL."""

    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    health_points = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
