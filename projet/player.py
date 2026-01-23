# Define the Player class.
"""Module defining the Player class."""
from item import Item


class Player:  # pylint: disable=too-many-instance-attributes
    """Represents the player character in the game."""

    # Define the constructor.
    def __init__(self, name, max_weight: float = 2.0):
        self.name = name
        self.current_room = None
        self.history = []
        # Inventory stored as name->Item
        self.inventory = {}
        # Maximum weight the player can carry (kg)
        self.max_weight = max_weight
        # Quest manager
        self.quest_manager = None
        # Current page of carnet being read
        self.carnet_current_page = 0
        # Track if player is reading the carnet
        self.is_reading_carnet = False
        # Track if player has talked to Max
        self.talked_to_max = False
        # Track if player has talked to Tunnel at the gym
        self.talked_to_tunnel = False
        # Track if player has talked to Tunnel on the way back
        self.talked_to_tunnel_return = False
        # Track if player talked to Tunnel during current gym visit (resets on room change)
        self.tunnel_talked_this_visit = False
        # Money the player has
        self.money = 0
        # Flag for access to Maxou's secret room
        self.maxou_room_unlocked = False
        # Hint flag for the exam locker code
        self.has_exam_code_hint = False
        # Locker state for exam subjects
        self.casier_opened = False
        # Track if first visit to salle des profs after exam quest activation
        self.first_visit_salle_profs_after_exam_quest = False
        # Track if Koro's patrol has started
        self.koro_patrol_started = False

    def get_current_weight(self) -> float:
        """Return the total weight of items currently carried by the player."""
        try:
            return sum(getattr(it, "weight", 0) for it in self.inventory.values())
        except (TypeError, AttributeError):
            return 0.0

    # Define the move method.
    def move(self, direction):
        """Move the player in the specified direction."""
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
        print(self.get_history())
        print(self.current_room.get_long_description())

        return True

    def get_history(self):
        """Return a formatted list of previously visited rooms."""

        message = "\nVoici les pièces que vous avez visitées :\n"
        for room in self.history:
            message += f"- {room.name}\n"
        return message

    # Define the get_inventory method.
    def get_inventory(self):
        """Return a formatted string of the player's inventory."""
        # If inventory is empty, return the empty message.
        try:
            is_empty = len(self.inventory) == 0
        except (TypeError, AttributeError):
            # Fallback: treat falsy inventory as empty
            is_empty = not bool(self.inventory)

        if is_empty:
            current_weight = self.get_current_weight()
            return (
                "Votre inventaire est vide.\n"
                f"💰 Argent: {self.money}€\n"
                f"⚖️  Poids: {current_weight:.3f} kg / {self.max_weight} kg"
            )

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
            except (TypeError, AttributeError):
                items = [self.inventory]

        for it in items:
            try:
                item_str = str(it)
            except (TypeError, AttributeError):
                # Fallback to attribute-based formatting
                if (
                    hasattr(it, "name")
                    and hasattr(it, "description")
                    and hasattr(it, "weight")
                ):
                    item_str = f"{it.name} : {it.description} ({it.weight} kg)"
                else:
                    item_str = repr(it)
            lines.append(f"    - {item_str}")

        # Add weight summary at the end
        current_weight = self.get_current_weight()
        lines.append(f"\n💰 Argent: {self.money}€")
        lines.append(f"⚖️  Poids: {current_weight:.3f} kg / {self.max_weight} kg")

        return "\n".join(lines)

    def add_reward(self, reward_text):
        """Add a reward message for completing a quest."""
        print(f"📦 Récompense reçue: {reward_text}")

        # Create an Item object for the reward and add it to inventory
        reward_item = Item(
            reward_text.lower().replace(" ", "_"), f"Récompense: {reward_text}", 0.033
        )

        # Check if adding this item would exceed weight capacity
        current_weight = self.get_current_weight()
        new_total_weight = current_weight + reward_item.weight

        if new_total_weight > self.max_weight:
            excess_weight = new_total_weight - self.max_weight
            print(
                "\n❌ C'est trop lourd mon pote va falloir lâcher un item, "
                "j'ai pas 4 bras nn plus"
            )
            print(f"❌ Il y a {excess_weight:.3f} kg en trop\n")
            return False

        # Add the reward to inventory
        self.inventory[reward_item.name] = reward_item
        return True
