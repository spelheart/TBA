class Item:
    def __init__(self, name: str, description: str, weight: float = 0):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self) -> str:
        return f"{self.name} : {self.description} ({self.weight} kg)"


class Instrument(Item):
    """Classe pour les instruments jouables dans le jeu"""
    def __init__(self, name: str, description: str, weight: float = 0, effect: str = None):
        super().__init__(name, description, weight)
        self.effect = effect  # L'effet quand on joue de l'instrument
    
    def __str__(self) -> str:
        return f"{self.name} : {self.description} ({self.weight} kg)"


    