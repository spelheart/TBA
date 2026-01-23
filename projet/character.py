"""Module defining the Character class for NPCs in the game."""
import random


class Character:
    """Represents a non-player character in the game."""
    def __init__(
        self,
        name: str,
        description: str,
        current_room,
        msgs: list,
        immobile: bool = False,
        patrol_rooms: list = None,
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        self.last_msg = None  # Track last message for quest failures
        self.repeat_last_msg = False  # Flag to repeat last message
        self.immobile = immobile  # If True, the character won't move
        self.patrol_rooms = patrol_rooms or []  # List of rooms to patrol between
        self.is_patrolling = False  # Whether the character is currently patrolling

    def __str__(self) -> str:
        """Return string representation of the character."""
        return f"{self.name} : {self.description} "

    def get_msg(self):
        """Get the next message from the character's dialogue list."""
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
        """Move the character to a random adjacent room."""
        # If the character is immobile, don't move
        if self.immobile:
            return False

        # If patrolling, use patrol logic
        if self.is_patrolling and self.patrol_rooms:
            if random.random() < 0.5:  # 50% chance to move
                # Find next room in patrol list
                if self.current_room in self.patrol_rooms:
                    current_idx = self.patrol_rooms.index(self.current_room)
                    next_idx = (current_idx + 1) % len(self.patrol_rooms)
                    new_room = self.patrol_rooms[next_idx]
                    
                    from game import DEBUG  # pylint: disable=import-outside-toplevel
                    
                    if DEBUG:
                        debug_msg = (
                            f"DEBUG: {self.name} patrouille de {self.current_room.name} "
                            f"vers {new_room.name}"
                        )
                        print(debug_msg)
                    
                    if self.name in self.current_room.inventory:
                        del self.current_room.inventory[self.name]
                    self.current_room = new_room
                    self.current_room.inventory[self.name] = self
            return True

        if random.choice([True, False]):
            # Build list of (direction, room) pairs for available exits
            possible_pairs = [
                (dirc, room)
                for dirc, room in self.current_room.exits.items()
                if room is not None
            ]
            if possible_pairs:
                dirc, new_room = random.choice(possible_pairs)

                from game import DEBUG  # pylint: disable=import-outside-toplevel

                if DEBUG:
                    # Show the direction (N/E/S/O) in parentheses
                    debug_msg = (
                        f"DEBUG: {self.name} se déplace de {self.current_room.name} "
                        f"vers {new_room.name} ({dirc})"
                    )
                    print(debug_msg)

                if self.name in self.current_room.inventory:
                    del self.current_room.inventory[self.name]
                self.current_room = new_room
                self.current_room.inventory[self.name] = self
                return True
        return False
