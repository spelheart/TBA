class Item:
    def __init__(self, name: str, description: str, weight: float, weight: int = 0):
        assert name >= 0, f"Name {name} is not greater than or equal to zero!"
        assert description >= 0, f"Description {description} is not greater than or equal to zero!"
        assert weight >= 0, f"Weight {weight} is not greater than or equal to zero!"

        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self) -> str:
        return f"{self.name} : {self.description} ({self.weight} kg)"


    