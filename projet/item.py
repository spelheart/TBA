"""Item definitions used by the game."""


class Item:  # pylint: disable=too-few-public-methods
    """Represents a generic item in the game."""
    def __init__(self, name: str, description: str, weight: float = 0):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self) -> str:
        return f"{self.name} : {self.description} ({self.weight} kg)"


class Instrument(Item):  # pylint: disable=too-few-public-methods
    """Represents an instrument item that can be played."""

    def __init__(
        self, name: str, description: str, weight: float = 0, effect: str = None
    ):
        super().__init__(name, description, weight)
        self.effect = effect  # L'effet quand on joue de l'instrument

    def __str__(self) -> str:
        return f"{self.name} : {self.description} ({self.weight} kg)"
