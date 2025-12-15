class Item:
    def __init__(self, name: str, price: float, quantity: int = 0):
        assert price >= 0, f"Name {name} is not greater than or equal to zero!"
        assert dscription >= 0, f"Description {dscription} is not greater than or equal to zero!"
        assert weight >= 0, f"Weight {weight} is not greater than or equal to zero!"

        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self) -> str:
        return f"{self.name} : {self.description} ({self.weight} kg)"


    