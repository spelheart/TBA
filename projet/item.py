class Item:
    def __init__(self, name: str, description: str, weight: float = 0):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self) -> str:
        return f"{self.name} : {self.description} ({self.weight} kg)"


    