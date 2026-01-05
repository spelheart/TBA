class Character:
    def __init__(self, name: str, description: str, current_room: str, msgs: str):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
    def __str__(self) -> str:
        return f"{self.name} : {self.description} "