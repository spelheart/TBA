
# Define the Room class.

class Room:

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        # Inventory: list chosen to hold Item objects (allows duplicates and ordered traversal)
        self.inventory = {}
        # Characters (PNJ) present in the room — initialized empty, filled from Game.setup()
        self.characters = {}
    
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
        # Build lists for items and characters (PNJ)
        # Normalize inventory to a list
        try:
            items = []
            if isinstance(self.inventory, dict):
                items = list(self.inventory.values())
            elif isinstance(self.inventory, (list, tuple, set)):
                items = list(self.inventory)
            else:
                try:
                    items = list(self.inventory)
                except Exception:
                    items = [self.inventory]
        except Exception:
            items = []

        # Normalize characters to a list
        try:
            chars = []
            if hasattr(self, 'characters'):
                if isinstance(self.characters, dict):
                    chars = list(self.characters.values())
                elif isinstance(self.characters, (list, tuple, set)):
                    chars = list(self.characters)
                else:
                    try:
                        chars = list(self.characters)
                    except Exception:
                        chars = [self.characters]
        except Exception:
            chars = []

        if len(items) == 0 and len(chars) == 0:
            return "Il n'y a rien ici."

        lines = []
        if len(items) > 0:
            lines.append("La pièce contient :")
            for it in items:
                try:
                    item_str = str(it)
                except Exception:
                    if hasattr(it, 'name') and hasattr(it, 'description') and hasattr(it, 'weight'):
                        item_str = f"{it.name} : {it.description} ({it.weight} kg)"
                    else:
                        item_str = repr(it)
                lines.append(f"    - {item_str}")

        if len(chars) > 0:
            lines.append("Personnages présents :")
            for c in chars:
                try:
                    cstr = str(c)
                except Exception:
                    cstr = getattr(c, 'name', repr(c))
                lines.append(f"    - {cstr}")

        return "\n".join(lines)
    

