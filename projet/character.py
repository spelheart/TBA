import random

class Character:
    def __init__(self, name: str, description: str, current_room, msgs: list):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs

    def __str__(self) -> str:
        return f"{self.name} : {self.description} "

    def get_msg(self):
        if not self.msgs:
            return "..."
        msg = self.msgs.pop(0)
        self.msgs.append(msg)
        return msg

    def move(self):
        if random.choice([True, False]):
            possible_exits = [room for room in self.current_room.exits.values() if room is not None]
            if possible_exits:
                new_room = random.choice(possible_exits)
                
                from game import DEBUG
                if DEBUG:
                    print(f"DEBUG: {self.name} se déplace de {self.current_room.name} vers {new_room.name}")

                if self.name in self.current_room.inventory:
                    del self.current_room.inventory[self.name]
                self.current_room = new_room
                self.current_room.inventory[self.name] = self
                return True
        return False
