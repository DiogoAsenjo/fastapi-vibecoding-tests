from dataclasses import dataclass


@dataclass
class Character:
    name: str
    health_points: int
    attack: int
    defense: int
    id: int | None = None
