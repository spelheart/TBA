
# Define the Room class.

class Room:

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        # Inventory: list chosen to hold Item objects (allows duplicates and ordered traversal)
        self.inventory = {}
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"
    
    # Define the get_inventory method.
    def get_inventory(self):
        # If inventory is empty, return the empty message.
        try:
            is_empty = len(self.inventory) == 0
        except Exception:
            # Fallback: treat falsy inventory as empty
            is_empty = not bool(self.inventory)

        if is_empty:
            return "Il n'y a rien ici."

        # Build the inventory display
        lines = ["La pièce contient :"]

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
    

