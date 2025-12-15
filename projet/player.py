# Define the Player class.
class Player():

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Add the room to the history if not already visited
        
        self.history.append(self.current_room)
        
        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        print(self.get_history())
        
        return True

    def get_history(self):
        
        message = "\nVoici les pièces que vous avez visitées :\n"
        for room in self.history:
            message += f"- {room.name}\n"
        return message
    
    # Define the get_inventory method.
    def get_inventory(self):
        # If inventory is empty, return the empty message.
        try:
            is_empty = len(self.inventory) == 0
        except Exception:
            # Fallback: treat falsy inventory as empty
            is_empty = not bool(self.inventory)

        if is_empty:
            return "Votre inventaire est vide."

        # Build the inventory display
        lines = ["Vous disposez des items suivants :"]

        # Normalize to an iterable of items for dicts/lists/sets
        items = None
        if isinstance(self.inventory, dict):
            items = list(self.inventory.values())
        elif isinstance(self.inventory, (list, tuple, set)):
            items = list(self.inventory)
        else:
            # Try to iterate
            try:
                items = list(self.inventory)
            except Exception:
                items = [self.inventory]

        for it in items:
            try:
                item_str = str(it)
            except Exception:
                # Fallback to attribute-based formatting
                if hasattr(it, 'name') and hasattr(it, 'description') and hasattr(it, 'weight'):
                    item_str = f"{it.name} : {it.description} ({it.weight} kg)"
                else:
                    item_str = repr(it)
            lines.append(f"    - {item_str}")

        return "\n".join(lines)
    
