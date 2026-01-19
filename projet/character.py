import random

class Character:
    def __init__(self, name: str, description: str, current_room, msgs: list, immobile: bool = False):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        self.last_msg = None  # Track last message for quest failures
        self.repeat_last_msg = False  # Flag to repeat last message
        self.immobile = immobile  # If True, the character won't move

    def __str__(self) -> str:
        return f"{self.name} : {self.description} "

    def get_msg(self):
        if not self.msgs:
            return "..."
        
        # If we need to repeat the last message, do so
        if self.repeat_last_msg and self.last_msg is not None:
            self.repeat_last_msg = False  # Reset flag for next call
            return self.last_msg
        
        msg = self.msgs.pop(0)
        self.msgs.append(msg)
        self.last_msg = msg  # Store as last message
        return msg

    def move(self):
        # If the character is immobile, don't move
        if self.immobile:
            return False
            
        if random.choice([True, False]):
            # Build list of (direction, room) pairs for available exits
            possible_pairs = [(dirc, room) for dirc, room in self.current_room.exits.items() if room is not None]
            if possible_pairs:
                dirc, new_room = random.choice(possible_pairs)

                from game import DEBUG
                if DEBUG:
                    # Show the direction (N/E/S/O) in parentheses
                    print(f"DEBUG: {self.name} se déplace de {self.current_room.name} vers {new_room.name} ({dirc})")

                if self.name in self.current_room.inventory:
                    del self.current_room.inventory[self.name]
                self.current_room = new_room
                self.current_room.inventory[self.name] = self
                return True
        return False
