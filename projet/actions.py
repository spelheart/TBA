# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def setup(self):
        """
        Initialise un dictionnaire d'alias pour chaque direction canonique.
        """
        self.aliases = {
            "N": ["N", "NORD", "Nord", "nord"],
            "E": ["E", "EST", "Est", "est"],
            "S": ["S", "SUD", "Sud", "sud"],
            "O": ["O", "OUEST", "Ouest", "ouest"]
        }

    def go(game, list_of_words, number_of_parameters):
        player = game.player
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(f"Commande '{command_word}' : nombre de paramètres incorrect.")
            return False

        user_input = list_of_words[1]
        # Récupère les directions possibles dans la salle courante
        exits = player.current_room.exits
        possible = []
        for canonique, alias_list in game.actions.aliases.items():
            if canonique in exits and exits[canonique]:
                possible.extend(alias_list)
        # Vérifie si l'entrée utilisateur correspond à une direction possible
        direction_norm = None
        for canonique, alias_list in game.actions.aliases.items():
            if user_input in alias_list and canonique in exits and exits[canonique]:
                direction_norm = canonique
                break

        if direction_norm is None:
            print(f"\n cherie t'y es contre sens, dirait sch donc'{user_input}' est FAUX ah nn pas valide plutôt. Va là bas tu verras c'est mimi : {', '.join(possible)}. il y a des licornes et des arc-en-ciel.\n")
            return False


        # Utilise la méthode move du joueur pour effectuer le déplacement
        player.move(direction_norm)
        #print(player.current_room.get_long_description())
    
        return True

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nDégage {player.name} surtout ne revient pas stp.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
    
    def back(game, list_of_words, number_of_parameters):
        """
        Retourne à la pièce précédente.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> back(game, ["back"], 0)
        True
        >>> back(game, ["back", "N"], 0)
        False
        >>> back(game, ["back", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        if len(player.history) == 0:
            print("\nVous n'avez aucune pièce précédente à laquelle revenir.\n")
            return False
        previous_room = player.history.pop()
        player.current_room = previous_room
        print(player.current_room.get_long_description())
        print(player.get_history())
        return True
    
    def look(game, list_of_words, number_of_parameters):
        """Affiche les items présents dans la pièce courante.
        Usage: `look` (aucun paramètre)
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        room = player.current_room
        # Use Room.get_inventory() if available
        try:
            inv_str = room.get_inventory()
        except Exception:
            # Fallback: try to print raw inventory
            try:
                inv_str = str(getattr(room, 'inventory', {}))
            except Exception:
                inv_str = "Il n'y a rien ici."
        # Also include characters (PNJ) present in the room if any
        chars_str = ""
        try:
            chars = getattr(room, 'characters', None)
            char_list = []
            if isinstance(chars, dict):
                char_list = list(chars.values())
            elif isinstance(chars, (list, tuple, set)):
                char_list = list(chars)
            else:
                try:
                    char_list = list(chars) if chars is not None else []
                except Exception:
                    char_list = [chars] if chars is not None else []

            if len(char_list) > 0:
                lines = ["Personnages présents :"]
                for c in char_list:
                    try:
                        cstr = str(c)
                    except Exception:
                        cstr = getattr(c, 'name', repr(c))
                    lines.append(f"    - {cstr}")
                chars_str = "\n" + "\n".join(lines)
        except Exception:
            chars_str = ""

        print(inv_str + chars_str)
        return True
    
    def take(game, list_of_words, number_of_parameters):
        """Permet au joueur de ramasser un item dans la pièce courante.
        Usage: `take <item_name>`
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1]
        player = game.player
        room = player.current_room

        # Check if the item is in the room's inventory
        if item_name not in room.inventory:
            print(f"\nIl n'y a pas d'item nommé '{item_name}' ici.\n")
            return False

        # Check weight capacity before taking
        item = room.inventory.get(item_name)
        #also guard against a Character instance accidentally placed in inventory
        try:
            from character import Character
            if isinstance(item, Character):
                print(f"\n'{item_name}' est un personnage, vous ne pouvez pas le prendre. \n")
                return False
        except Exception:
            pass
        item_weight = getattr(item, 'weight', 0)
        current = 0
        try:
            current = player.get_current_weight()
        except Exception:
            # fallback: compute from inventory
            try:
                current = sum(getattr(it, 'weight', 0) for it in player.inventory.values())
            except Exception:
                current = 0

        if current + item_weight > getattr(player, 'max_weight', 0):
            print(f"\nVous ne pouvez pas porter {item_name} ({item_weight} kg). Capacité restante: {max(0, getattr(player, 'max_weight',0) - current)} kg.\n")
            return False

        # Remove the item from the room and add it to the player's inventory
        item = room.inventory.pop(item_name)
        player.inventory[item_name] = item
        print(f"\nVous avez ramassé : {item}\n")
        return True
    
    def check(game, list_of_words, number_of_parameters):
        """Affiche l'inventaire du joueur.
        Usage: `check` (aucun paramètre)
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        try:
            inv_str = player.get_inventory()
        except Exception:
            try:
                inv_str = str(getattr(player, 'inventory', {}))
            except Exception:
                inv_str = "Votre inventaire est vide."

        print(inv_str)
        return True
    
    def drop(game, list_of_words, number_of_parameters):
        """Permet au joueur de déposer un item de son inventaire dans la pièce courante.
        Usage: `drop <item_name>`
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1]
        player = game.player
        room = player.current_room

        # Check if the item is in the player's inventory
        if item_name not in player.inventory:
            print(f"\nVous n'avez pas d'item nommé '{item_name}' dans votre inventaire.\n")
            return False

        # Remove the item from the player's inventory and add it to the room's inventory
        item = player.inventory.pop(item_name)
        room.inventory[item_name] = item
        print(f"\nVous avez déposé : {item}\n")
        return True

    def talk(game, list_of_words, number_of_parameters):
        """Parler à un personnage.
        Usage: `talk <character_name>`
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        character_name = list_of_words[1]
        player = game.player
        room = player.current_room

        # Check if the character is in the room
        if character_name not in room.inventory:
            print(f"\nIl n'y a pas de personnage nommé '{character_name}' ici.\n")
            return False
        
        character = room.inventory[character_name]
        
        if hasattr(character, 'get_msg'):
             print(f"\n{character.get_msg()}\n")
        else:
             print(f"\nVous ne pouvez pas parler à {character_name}.\n")
        return True
    
