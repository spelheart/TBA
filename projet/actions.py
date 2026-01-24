# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,line-too-long,trailing-whitespace,no-self-argument,no-member,broad-exception-caught,import-outside-toplevel,unused-import,inconsistent-return-statements,redefined-builtin,too-many-branches,duplicate-code,attribute-defined-outside-init,too-many-lines

import random
import threading

# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"


def input_with_timeout(prompt, timeout_sec=15):
    """Prompt user for input with a timeout. Returns None if timeout occurs."""
    result = [None]
    
    def input_thread():
        try:
            result[0] = input(prompt)
        except:
            pass
    
    thread = threading.Thread(target=input_thread, daemon=True)
    thread.start()
    thread.join(timeout=timeout_sec)
    
    if thread.is_alive():
        print("\n⏱️ Temps écoulé! Vous avez dépassé les 15 secondes!\n")
        return None
    return result[0]


class Actions:

    def setup(self):
        """
        Initialise un dictionnaire d'alias pour chaque direction canonique.
        """
        self.aliases = {
            "N": ["N", "NORD", "Nord", "nord"],
            "E": ["E", "EST", "Est", "est"],
            "S": ["S", "SUD", "Sud", "sud"],
            "O": ["O", "OUEST", "Ouest", "ouest"],
        }

    def go(game, list_of_words, number_of_parameters):
        player = game.player
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(f"Commande '{command_word}' : nombre de paramètres incorrect.")
            return False

        user_input = list_of_words[1].lower()
        
        # Check for special exits first (like "comptoir")
        if hasattr(player.current_room, 'special_exits') and user_input in player.current_room.special_exits:
            destination = player.current_room.special_exits[user_input]
            player.history.append(player.current_room)
            player.current_room = destination
            print(player.current_room.get_long_description())
            return True
        
        # Récupère les directions possibles dans la salle courante
        exits = player.current_room.exits
        possible = []
        for canonique, alias_list in game.actions.aliases.items():
            if canonique in exits and exits[canonique]:
                possible.extend(alias_list)
        
        # Add special exits to possible directions
        if hasattr(player.current_room, 'special_exits'):
            possible.extend(player.current_room.special_exits.keys())
        
        # Vérifie si l'entrée utilisateur correspond à une direction possible
        direction_norm = None
        for canonique, alias_list in game.actions.aliases.items():
            if user_input in alias_list and canonique in exits and exits[canonique]:
                direction_norm = canonique
                break

        if direction_norm is None:
            print(
                f"\n cherie t'y es contre sens, dirait sch donc'{user_input}' est FAUX ah nn pas valide plutôt. Va là bas tu verras c'est mimi : {', '.join(possible)}. il y a des licornes et des arc-en-ciel.\n"
            )
            return False

        # Utilise la méthode move du joueur pour effectuer le déplacement
        old_room = player.current_room
        player.move(direction_norm)
        
        # Move all characters BEFORE checking for encounter
        for character in game.characters:
            character.move()

        # CHECK FOR JOSEPH ENCOUNTER
        if player.hunted_by_joseph:
            room = player.current_room
            if "Joseph" in room.inventory:
                character = room.inventory["Joseph"]
                if hasattr(character, 'escape_phrases') and character.escape_phrases and len(character.escape_phrases) > 0:
                    # Encounter! Launch mini-game
                    print(f"\n⚠️ {character.get_msg()}\n")
                    print("Vous avez une chance de vous échapper!\n")
                    
                    escape_phrase = random.choice(character.escape_phrases)
                    print(f"Tapez rapidement: '{escape_phrase}'\n")
                    
                    player_input = input_with_timeout("> ", timeout_sec=15)
                    if player_input is None:
                        print(f"\n💀 Vous n'avez pas été assez rapide!\n")
                        print(f"{character.name}: C'est fini pour toi!\n")
                        return "LOSE"
                    elif player_input.strip() == escape_phrase:
                        print(f"\n✅ Vous réussissez à vous échapper de justesse!\n")
                        # You escape back to the previous room
                        player.current_room = old_room
                    else:
                        print(f"\n💀 Vous n'avez pas été assez rapide!\n")
                        print(f"{character.name}: C'est fini pour toi!\n")
                        return "LOSE"
        
        # CHECK FOR JOLYNE ENCOUNTER
        if player.hunted_by_jolyne:
            room = player.current_room
            if "Jolyne" in room.inventory:
                character = room.inventory["Jolyne"]
                if hasattr(character, 'escape_phrases') and character.escape_phrases and len(character.escape_phrases) > 0:
                    # Encounter! Launch mini-game
                    print(f"\n⚠️ {character.get_msg()}\n")
                    print("Vous avez une chance de vous échapper!\n")
                    
                    escape_phrase = random.choice(character.escape_phrases)
                    print(f"Tapez rapidement: '{escape_phrase}'\n")
                    
                    player_input = input_with_timeout("> ", timeout_sec=15)
                    if player_input is None:
                        print(f"\n💀 Vous n'avez pas été assez rapide!\n")
                        print(f"{character.name}: C'est fini pour toi!\n")
                        return "LOSE"
                    elif player_input.strip() == escape_phrase:
                        print(f"\n✅ Vous réussissez à vous échapper de justesse!\n")
                        # You escape back to the previous room
                        player.current_room = old_room
                    else:
                        print(f"\n💀 Vous n'avez pas été assez rapide!\n")
                        print(f"{character.name}: C'est fini pour toi!\n")
                        return "LOSE"

        # Reset flag when entering gym (allowing free entry)
        if old_room.name != "Gymnase" and player.current_room.name == "Gymnase":
            player.tunnel_talked_this_visit = False
        
        # GYMNASE SECURITY: Check if leaving gym without talking to Tunnel (only after talking to Maxou)
        if old_room.name == "Gymnase" and player.current_room.name != "Gymnase":
            # Only game over if they talked to Maxou and haven't talked to Tunnel on the way back
            if player.talked_to_max and not player.tunnel_talked_this_visit:
                print(
                    "\n💀 Vous vous précipitez vers la sortie sans regarder où vous allez.\n"
                )
                print("Soudain, un ballon arrive à toute vitesse et vous frappe de plein fouet !\n")
                print("*BOOOOOM*\n")
                print("Tunnel: T'avais qu'à m'écouter! Je t'avais dit que c'était dangereux!\n")
                print("Vous vous écroulez sur le sol du gymnase, sonnés.\n")
                return "LOSE"
            # Reset flag when leaving gym
            player.tunnel_talked_this_visit = False

        # Check quest objectives for visiting rooms
        if player.quest_manager:
            player.quest_manager.check_room_objectives(player.current_room.name)

        # Trigger Koro's patrol if entering salle des profs after exam quest activation
        if player.current_room.name == "Salle des profs":
            if player.quest_manager:
                quete_exam = None
                for quest in player.quest_manager.get_all_quests():
                    if quest.title == "Mission impossible" and quest.is_active:
                        quete_exam = quest
                        break
                
                # If exam quest is active
                if quete_exam:
                    # First visit: just mark it
                    if not player.first_visit_salle_profs_after_exam_quest:
                        player.first_visit_salle_profs_after_exam_quest = True
                    # Second visit and onwards: start patrol (silently)
                    elif not player.koro_patrol_started:
                        player.koro_patrol_started = True
                        # Find Koro and start his patrol
                        for character in game.characters:
                            if character.name == "Professeur Koro":
                                character.immobile = False
                                character.is_patrolling = True
                                break

        # Don't print here - player.move() already does it
        # print(player.current_room.get_long_description())
        # print(player.get_history())
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

        # Print the list of available commands grouped by category.
        print("\nVoici les commandes disponibles:\n")

        # Group commands by category
        categories = {}
        for command in game.commands.values():
            # Filter quest-related commands
            should_show = True
            
            # Command "open" only shows if exam quest is active
            if command.command_word == "open":
                should_show = False
                if game.player.quest_manager:
                    for quest in game.player.quest_manager.get_all_quests():
                        if quest.title == "Mission impossible" and quest.is_active:
                            should_show = True
                            break
            
            if should_show:
                if command.category not in categories:
                    categories[command.category] = []
                categories[command.category].append(command)

        # Display commands by category
        for category in sorted(categories.keys()):
            print(f"📌 {category}:")
            for command in categories[category]:
                print("\t- " + str(command))
            print()

        return True

    def help_help(game, list_of_words, number_of_parameters):
        """Affiche un indice contextuel basé sur l'état des quêtes.
        Usage: `help_help` (aucun paramètre)
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        
        # Vérifier l'état des quêtes
        quete_exam = None
        quete_victoria = None
        
        if player.quest_manager:
            for quest in player.quest_manager.get_all_quests():
                if quest.title == "Mission impossible":
                    quete_exam = quest
                if quest.title == "Le Prix du Chic":
                    quete_victoria = quest
        
        # Déterminer le message d'aide basé sur l'état des quêtes
        message = ""
        
        # Si la quête exam est activée et pas terminée
        if quete_exam and quete_exam.is_active and not quete_exam.is_completed:
            message = "peut etre que parler aux gens qui vous sont chère serait utile"
        # Si la quête exam n'est pas activée et Victoria est activée
        elif (not quete_exam or not quete_exam.is_active) and quete_victoria and quete_victoria.is_active and not quete_victoria.is_completed:
            message = "attention à ne pas vous faire raquetter"
        # Si les deux quêtes sont terminées
        elif quete_exam and quete_exam.is_completed and quete_victoria and quete_victoria.is_completed:
            message = "la 'meilleure amie' de Victoria pourrait avoir des informations intéressantes à partager..."
        # Si aucune n'est activée
        else:
            message = "abuse, joue un peu avant de demander de l'aide"
        
        print(f"\n💡 {message}\n")
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
        
        # Check if player is trying to leave gym without talking to Tunnel (only after talking to Maxou)
        old_room = player.current_room
        previous_room = player.history[-1]  # Peek at the previous room
        
        if old_room.name == "Gymnase" and previous_room.name != "Gymnase":
            # Only game over if they talked to Maxou and haven't talked to Tunnel on the way back
            if player.talked_to_max and not player.tunnel_talked_this_visit:
                print(
                    "\n💀 Vous vous précipitez vers la sortie sans regarder où vous allez.\n"
                )
                print("Soudain, un ballon arrive à toute vitesse et vous frappe de plein fouet !\n")
                print("*BOOOOOM*\n")
                print("Tunnel: T'avais qu'à m'écouter! Je t'avais dit que c'était dangereux!\n")
                print("Vous vous écroulez sur le sol du gymnase, sonnés.\n")
                return "LOSE"
            # Reset flag when leaving gym
            player.tunnel_talked_this_visit = False
        
        # Perform the back action
        previous_room = player.history.pop()
        player.current_room = previous_room
        
        # Move all characters BEFORE checking for encounter
        for character in game.characters:
            character.move()
        
        # Check for Joseph encounter during hunt
        if player.hunted_by_joseph:
            room = player.current_room
            if "Joseph" in room.inventory:
                character = room.inventory["Joseph"]
                if hasattr(character, 'escape_phrases') and character.escape_phrases and len(character.escape_phrases) > 0:
                    print(f"\n⚠️ {character.get_msg()}\n")
                    print("Vous avez une chance de vous échapper!\n")
                    
                    escape_phrase = random.choice(character.escape_phrases)
                    print(f"Tapez rapidement: '{escape_phrase}'\n")
                    
                    player_input = input_with_timeout("> ", timeout_sec=15)
                    if player_input is None:
                        print(f"\n💀 Vous n'avez pas été assez rapide!\n")
                        print(f"{character.name}: C'est fini pour toi!\n")
                        return "LOSE"
                    elif player_input.strip() == escape_phrase:
                        print(f"\n✅ Vous réussissez à vous échapper de justesse!\n")
                        # You escape back to the previous room
                        player.current_room = previous_room
                        player.history.append(previous_room)
                    else:
                        print(f"\n💀 Vous n'avez pas été assez rapide!\n")
                        print(f"{character.name}: C'est fini pour toi!\n")
                        return "LOSE"
        
        # Check for Jolyne encounter during hunt
        if player.hunted_by_jolyne:
            room = player.current_room
            if "Jolyne" in room.inventory:
                character = room.inventory["Jolyne"]
                if hasattr(character, 'escape_phrases') and character.escape_phrases and len(character.escape_phrases) > 0:
                    print(f"\n⚠️ {character.get_msg()}\n")
                    print("Vous avez une chance de vous échapper!\n")
                    
                    escape_phrase = random.choice(character.escape_phrases)
                    print(f"Tapez rapidement: '{escape_phrase}'\n")
                    
                    player_input = input_with_timeout("> ", timeout_sec=15)
                    if player_input is None:
                        print(f"\n💀 Vous n'avez pas été assez rapide!\n")
                        print(f"{character.name}: C'est fini pour toi!\n")
                        return "LOSE"
                    elif player_input.strip() == escape_phrase:
                        print(f"\n✅ Vous réussissez à vous échapper de justesse!\n")
                        # You escape back to the previous room
                        player.current_room = previous_room
                        player.history.append(previous_room)
                    else:
                        print(f"\n💀 Vous n'avez pas été assez rapide!\n")
                        print(f"{character.name}: C'est fini pour toi!\n")
                        return "LOSE"
        
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
                inv_str = str(getattr(room, "inventory", {}))
            except Exception:
                inv_str = "Il n'y a rien ici."
        # Also include characters (PNJ) present in the room if any
        chars_str = ""
        try:
            chars = getattr(room, "characters", None)
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
                        cstr = getattr(c, "name", repr(c))
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
        # also guard against a Character instance accidentally placed in inventory
        try:
            from character import Character

            if isinstance(item, Character):
                print(
                    f"\n'{item_name}' est un personnage, vous ne pouvez pas le prendre. \n"
                )
                return False
        except Exception:
            pass
        item_weight = getattr(item, "weight", 0)
        current = 0
        try:
            current = player.get_current_weight()
        except Exception:
            # fallback: compute from inventory
            try:
                current = sum(
                    getattr(it, "weight", 0) for it in player.inventory.values()
                )
            except Exception:
                current = 0

        if current + item_weight > getattr(player, "max_weight", 0):
            print(
                f"\nVous ne pouvez pas porter {item_name} ({item_weight} kg). Capacité restante: {max(0, getattr(player, 'max_weight',0) - current)} kg.\n"
            )
            return False

        # Remove the item from the room and add it to the player's inventory
        item = room.inventory.pop(item_name)
        player.inventory[item_name] = item
        print(f"\nVous avez ramassé : {item}\n")

        # Check if we're in Réserve Victoria and track items taken
        if room.name == "Réserve Victoria":
            # Initialize counter if it doesn't exist
            if not hasattr(player, 'reserve_victoria_items_taken'):
                player.reserve_victoria_items_taken = 0
            
            player.reserve_victoria_items_taken += 1
            
            # If player took more than 1 item, GAME OVER
            if player.reserve_victoria_items_taken > 1:
                print("\n" + "=" * 70)
                print("  ⚠️ MAXOU SURGIT DANS LA SALLE ! ⚠️")
                print("=" * 70)
                print("\nMaxou: HÉHO ! Tu t'es cru chez toi à tout prendre ?!")
                print("Maxou: Tu te prends pour qui exactement ?!")
                print("Maxou: Je t'ai fait confiance et c'est comme ça que tu me remercies ?!")
                print("Maxou: *Il vous arrache tous les objets des mains*")
                print("\nMaxou: CASSE-TOI DE MA RÉSERVE ! ET NE REVIENS PLUS JAMAIS !")
                print("Maxou: Je ne t'aiderai PLUS. C'est terminé entre nous !")
                print("\n" + "=" * 70)
                print("\n💀 Vous avez trahi la confiance de Maxou. Victoria ne sera jamais conquise.\n")
                print("=" * 70 + "\n")
                return "LOSE"

        # Check quest objectives for taking items
        if player.quest_manager:
            player.quest_manager.complete_objective(f"Récupérer {item_name}")

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
                inv_str = str(getattr(player, "inventory", {}))
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
            print(
                f"\nVous n'avez pas d'item nommé '{item_name}' dans votre inventaire.\n"
            )
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

        # Handle name aliases for easier typing
        name_aliases = {
            "Koro": "Professeur Koro",
            "koro": "Professeur Koro",
        }
        
        # Convert alias to full name if it exists
        if character_name in name_aliases:
            character_name = name_aliases[character_name]

        # Check if the character is in the room
        if character_name not in room.inventory:
            print(f"\nIl n'y a pas de personnage nommé '{character_name}' ici.\n")
            return False

        character = room.inventory[character_name]

        # Special handling for Joseph - trigger hunt
        if character_name == "Joseph":
            if not player.hunted_by_joseph:
                player.hunted_by_joseph = True
                print(f"\n⚠️ {character_name}: Tu aurais pas dû faire ça...\n")
                print("Il te prend en chasse!\n")
        
        # Special handling for Jolyne - trigger hunt
        if character_name == "Jolyne":
            if not player.hunted_by_jolyne:
                player.hunted_by_jolyne = True
                print(f"\n⚠️ {character_name}: Tu aurais pas dû faire ça...\n")
                print("Elle te prend en chasse!\n")

        # Special handling for Lucas - gives locker code hint only if exam quest is active
        if character_name == "Lucas":
            quete_exam_active = False
            if player.quest_manager:
                for quest in player.quest_manager.get_all_quests():
                    if quest.title == "Mission impossible" and quest.is_active:
                        quete_exam_active = True
                        break

            if quete_exam_active and not player.has_exam_code_hint:
                player.has_exam_code_hint = True
                print(
                    "\nLucas: J'ai entendu un truc sur un coffre fort verrouillé : 'Les lettres comptent beaucoup'."
                )
            # Continue normal dialogue too

        # Special handling for Maxou - main quest for Victoria's gift
        if character_name == "Maxou":
            # If player is in the gym and hasn't talked to Tunnel during this visit, it's a game over
            if player.current_room.name == "Gymnase" and not player.tunnel_talked_this_visit:
                print(
                    "\n💀 Vous avez voulu aller parler à Maxou mais vous êtes passé sur le terrain sans regarder."
                )
                print(
                    "Il y avait un match en cours et vous vous êtes reçu une balle en pleine figure."
                )
                print("Quelle idée...\n")
                return "LOSE"
            
            player.talked_to_max = True
            
            # Reset tunnel flag - player must talk to Tunnel again before leaving
            player.tunnel_talked_this_visit = False

            # Display Maxou's message
            if hasattr(character, "get_msg"):
                print(f"\n{character.get_msg()}\n")

            # Activate main quest if not already done
            if player.quest_manager:
                quete_maxou = None
                for quest in player.quest_manager.get_all_quests():
                    if quest.title == "Le Prix du Chic":
                        quete_maxou = quest
                        break

                if quete_maxou and not quete_maxou.is_active:
                    quete_maxou.activate()
                    player.quest_manager.active_quests.append(quete_maxou)

                # Check if player has 1000$ to give Maxou
                if quete_maxou and quete_maxou.is_active and not quete_maxou.is_completed:
                    if player.money < 1000:
                        print(
                            f"\nMaxou: Reviens quand tu auras 1000$. Tu en as {player.money}$ pour l'instant.\n"
                        )
                        return True

                    # Player has the money - finalize the quest
                    print("\n✨ Maxou ouvre la porte de sa salle secrète ! ✨\n")
                    player.money -= 1000
                    print(f"Vous avez payé 1000$. Argent restant: {player.money}$\n")

                    # Mark objective as completed and complete quest
                    if quete_maxou and not quete_maxou.is_completed:
                        quete_maxou.complete_objective(
                            "Collecter 1000 dollars", player
                        )
                        quete_maxou.is_completed = True
                        print(f"\n🏆 Quête terminée: {quete_maxou.title}")
                        print("🎁 Récompense: Accès à la salle secrète de Maxou\n")

                        # Call the secret room effect function
                        from game import maxou_secret_room_effect
                        maxou_secret_room_effect(game)

                        # Mark that player has access to Maxou's secret room
                        player.maxou_room_unlocked = True

                        # Activate the final quest
                        quete_finale = None
                        for quest in player.quest_manager.get_all_quests():
                            if quest.title == "Le Cadeau Parfait":
                                quete_finale = quest
                                break
                        
                        if quete_finale and not quete_finale.is_active:
                            quete_finale.activate()
                            player.quest_manager.active_quests.append(quete_finale)

                        # Maxou's instruction 
                        print("Maxou: Voilà, tu peux y aller maintenant.")
                        print("Maxou: Prends ce dont tu as besoin pour impressionner Victoria.")
                        print("Maxou: Bonne chance mec.\n")

                        return True

                # Special handling for Lucas - hint already handled above

        # Special handling for Tunnel - mark that player talked to them
        if character_name == "Tunnel":
            # Mark that player talked to Tunnel during this visit
            player.tunnel_talked_this_visit = True
            
            # Check if this is on the way back (after talking to Maxou)
            if player.talked_to_max:
                player.talked_to_tunnel_return = True
                # Display the return dialogue
                print(
                    "\nTunnel: Ah te revoilà ! Alors, ça a été avec Maxou ? Il a l'air sympa mec. Enfin bon sympa c'est un grand mot. En tout cas il regarde attentivement hein. Mais écoute, tu peux pas partir maintenant, le match vient de commencer ! Regarde la foule, l'énergie, c'est dingue ! Les joueurs sont en feu ! L'équipe adverse a déjà marqué deux points, et notre équipe riposte... OUIIIII GOAL ! Tu vois ? T'aurais raté ça si tu t'en allais ! C'est ça la beauté du match en direct mec. Pas comme à la télé où tu peux mettre en pause. Non, ici c'est du live, du vrai ! Regarde ce buteur... c'est un genie ! Il dribble comme un fou, il esquive, il feinte... C'est de l'art ! Et puis tu sais quoi ? Le terrain est encore dangereux hein. Y a des ballons qui volent partout, des gens qui crient, qui sautent... C'est chaotique mais c'est magnifique. Et puis honnêtement, si tu sors du gymnase pendant que tu es entré faire une truffe, ça va pas passer inaperçu tu sais. Faut rester un peu, regarder la fin de la première mi-temps au moins. C'est par respect pour le jeu, pour les joueurs, pour moi aussi franchement ! Allez reste, on regarde ensemble. Je te montre les meilleurs joueurs, les tactiques... C'est clairement plus intéressant qu'à l'extérieur ! Et puis qui sait, peut-être que Maxou va demander comment c'était dehors ou un truc du genre...\n"
                )
                return True
            else:
                player.talked_to_tunnel = True
                # Display the initial dialogue (first message only)
                if character.msgs and len(character.msgs) > 0:
                    print(f"\n{character.msgs[0]}\n")
                return True

        # Special handling for Proviseur - gives money first time with disdain
        if character_name == "Proviseur":
            if not player.proviseur_gave_money:
                # First time talking - give money with condescension
                player.proviseur_gave_money = True
                player.money += 5
                print("\nLe proviseur vous regarde de haut en bas avec un sourire suffisant. Proviseur: Ah, encore un élève démuni qui ne peut même pas s'offrir un repas décent... *Il soupire théâtralement* En tant que proviseur EXTRÊMEMENT généreux et bienveillant de cet établissement, je ne peux pas laisser mes élèves mourir de faim. Ce serait mauvais pour notre réputation. *Il sort son portefeuille en cuir avec lenteur calculée* Tenez, je vous donne 5$. Cinq dollars de MA poche personnelle ! Vous vous rendez compte de ma MAGNANIMITÉ ? De ma BONTÉ sans limites ? *Il vous tend l'argent du bout des doigts* J'espère que vous apprécierez ce geste d'une rare générosité. Peu de proviseurs feraient autant pour leurs élèves. N'oubliez jamais ce que j'ai fait pour vous.\n")
                print(f"💰 Vous recevez 5$ ! Argent total : {player.money}$\n")
                return True
            else:
                # Already gave money, normal dialogue
                if hasattr(character, "get_msg"):
                    print(f"\n{character.get_msg()}\n")
                return True

        # Special handling for Patoche and JP - bullies
        if character_name in ["Patoche", "JP"]:
            if not player.talked_to_max:
                print("\nPatoche et JP te regardent avec mépris.\n")
                print(
                    "Patoche: Dégage de là, le loser. On n'a pas de temps à perdre avec toi.\n"
                )
                print("JP: *te pousse violemment* Casse-toi !\n")
                return True

            # Player has talked to Max, display dialogue and activate the exam quest if first time
            if hasattr(character, "get_msg"):
                print(f"\n{character.get_msg()}\n")

            if player.quest_manager:
                quete_exam = None
                for quest in player.quest_manager.get_all_quests():
                    if quest.title == "Mission impossible":
                        quete_exam = quest
                        break

                # Activate the quest if not already active
                if quete_exam and not quete_exam.is_active:
                    quete_exam.activate()
                    player.quest_manager.active_quests.append(quete_exam)

                # If the player returns with the copies, finalize the quest here
                if quete_exam and quete_exam.is_active and not quete_exam.is_completed:
                    if "piles de copies d'examen" in player.inventory:
                        # Patoche et JP arrachent les copies et donnent l'argent
                        item = player.inventory.pop("piles de copies d'examen")
                        _ = item  # avoid unused variable
                        print(
                            "\nPatoche te arrache les copies des mains, \net JP te jette un billet froissé à la figure...\n"
                        )
                        player.money += 1000
                        print(
                            f"💰 Tu reçois 1000$. Argent total: {player.money}$.\n"
                        )

                        # Marquer l'objectif final et terminer la quête
                        quete_exam.complete_objective(
                            "Remettre les copies à Patoche et JP", player
                        )
                        quete_exam.is_completed = True
                        print(
                            f"\n🏆 Quête terminée: {quete_exam.title}\n"
                            "😊 Tu as enfin assez d'argent pour payer le cadeau pour Vic.\n"
                        )

            return True

        # Special handling for Sophie - different dialogue based on quest status
        if character_name == "Sophie":
            quete_exam_completed = False
            quete_victoria_completed = False
            
            if player.quest_manager:
                for quest in player.quest_manager.get_all_quests():
                    if quest.title == "Mission impossible" and quest.is_completed:
                        quete_exam_completed = True
                    if quest.title == "Le Prix du Chic" and quest.is_completed:
                        quete_victoria_completed = True
            
            # Si les deux quêtes sont terminées, elle révèle le secret de Victoria
            if quete_exam_completed and quete_victoria_completed:
                print("\nSophie: Oh salut ! Tu t'intéresses à ma *chère* amie Victoria ? Entre nous... elle chante horriblement mal. Genre vraiment catastrophique ! La pauvre, elle en a tellement honte qu'elle s'entraîne en secret dans la salle de musique... Mais bon, c'est ma meilleure amie, donc je la soutiens *évidemment*... *soupir*\n")
            else:
                # Sinon, elle joue la reine du monde
                if hasattr(character, "get_msg"):
                    print(f"\n{character.get_msg()}\n")
            
            return True

        if hasattr(character, "get_msg"):
            print(f"\n{character.get_msg()}\n")
        else:
            print(f"\nVous ne pouvez pas parler à {character_name}.\n")

        # Check quest objectives for talking to characters
        if player.quest_manager:
            # Track total completed objectives before attempt
            total_completed_before = sum(
                len(q.completed_objectives)
                for q in player.quest_manager.get_all_quests()
            )

            player.quest_manager.check_action_objectives("parler", character_name)

            # Check if any objective was completed
            total_completed_after = sum(
                len(q.completed_objectives)
                for q in player.quest_manager.get_all_quests()
            )

            # If no new objectives were completed, mark character to repeat message
            if total_completed_after == total_completed_before and hasattr(
                character, "repeat_last_msg"
            ):
                character.repeat_last_msg = True

        return True

    def open_safe(game, list_of_words, number_of_parameters):
        """Ouvrir le coffre fort de la salle des profs. Usage: open coffre fort"""
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        room = player.current_room

        # Must be in salle des profs
        if room.name != "Salle des profs":
            print("\nIl n'y a pas de coffre fort ici.\n")
            return False

        # If characters present, it's game over
        characters_in_room = getattr(room, "characters", {})
        if characters_in_room:
            # Get the first character's name
            character_name = list(characters_in_room.keys())[0]
            print(f"\n💀 {character_name} vous surprend en train d'essayer d'ouvrir le coffre fort !")
            print(f"{character_name}: QU'EST-CE QUE VOUS FAITES LÀ ?! GAME OVER.\n")
            return "LOSE"
        
        # Also check if any character from game.characters is in the room (for patrol/dynamic NPCs)
        for character in game.characters:
            if character.current_room == room:
                print(f"\n💀 {character.name} vous surprend en train d'essayer d'ouvrir le coffre fort !")
                print(f"{character.name}: QU'EST-CE QUE VOUS FAITES LÀ ?! GAME OVER.\n")
                return "LOSE"

        # If already opened
        if player.casier_opened:
            print("\nLe coffre fort est déjà ouvert.\n")
            return True

        # Ask for the code
        code_entered = input("\nVeuillez entrer le code du coffre fort: ")
        correct_code = "3788"  # Les (3) lettres(7) comptent(8) beaucoup(8)

        # Wrong code
        if code_entered != correct_code:
            print("\n❌ Code incorrect. Le coffre fort reste verrouillé.\n")
            return False

        # Open the safe
        player.casier_opened = True
        print("\n✅ Le coffre fort s'ouvre en grinçant...\n")

        # Create and place the exam copies in the room if not already there
        if "piles de copies d'examen" not in room.inventory:
            from item import Item
            copie = Item(
                "piles de copies d'examen", "une copie d'examen avec une note de 0/20", 1
            )
            room.inventory[copie.name] = copie
            print("Les sujets d'examen apparaissent à l'intérieur du coffre !\n")

        # Give the exam copies to the player
        if "piles de copies d'examen" in room.inventory:
            item = room.inventory.pop("piles de copies d'examen")
            player.inventory[item.name] = item
            print("Vous récupérez les sujets d'examen !\n")

        # Marquer les objectifs liés au coffre fort, sans terminer la quête
        if player.quest_manager:
            for quest in player.quest_manager.get_all_quests():
                if quest.title == "Mission impossible":
                    # Mettre à jour la formulation pour 'coffre fort'
                    quest.complete_objective("Ouvrir le coffre fort", player)
                    quest.complete_objective("Récupérer les sujets d'examen", player)
                    print(
                        "\n➡️ Ramène maintenant les copies à Patoche et JP pour terminer la quête.\n"
                    )
                    break

        return True

    def show_quests(game, list_of_words, number_of_parameters):
        """Affiche la liste de toutes les quêtes du joueur.
        Usage: `quests` (aucun paramètre)
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        if player.quest_manager:
            player.quest_manager.show_quests()
        else:
            print("\nAucune quête disponible.\n")

        return True

    def show_quest_details(game, list_of_words, number_of_parameters):
        """Affiche les détails d'une quête spécifique.
        Usage: `quest <quest_name>`
        """
        l = len(list_of_words)
        if l < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        quest_name = " ".join(list_of_words[1:])  # Support multi-word quest names
        player = game.player

        if player.quest_manager:
            player.quest_manager.show_quest_details(quest_name)
        else:
            print("\nAucune quête disponible.\n")

        return True

    def play(game, list_of_words, number_of_parameters):
        """Permet au joueur de jouer d'un instrument.
        Usage: `play <instrument_name>`
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        instrument_name = list_of_words[1]
        player = game.player
        room = player.current_room

        # Check if the instrument is in the room's inventory
        if instrument_name not in room.inventory:
            print(f"\nIl n'y a pas d'instrument nommé '{instrument_name}' ici.\n")
            return False

        item = room.inventory[instrument_name]

        # Check if it's an Instrument
        from item import Instrument

        if not isinstance(item, Instrument):
            print(f"\n'{instrument_name}' n'est pas un instrument jouable.\n")
            return False

        # Execute the effect if it exists
        if item.effect:
            print(f"\n🎵 Vous jouez du {instrument_name}...\n")
            if callable(item.effect):
                # If effect is a function, call it with game as parameter
                item.effect(game)
            else:
                # Otherwise just print the effect message
                print(item.effect)
        else:
            print(
                f"\n🎵 Vous jouez du {instrument_name}... La musique résonne dans la salle.\n"
            )

        return True

    def buy(game, list_of_words, number_of_parameters):
        """Permet au joueur d'acheter un sandwich au comptoir de la cafétéria.
        Usage: `buy sandwich`
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1].lower()
        player = game.player
        room = player.current_room

        # Check if trying to buy sandwich
        if item_name != "sandwich":
            print(f"\nVous ne pouvez pas acheter '{item_name}'.\n")
            return False

        # Check if at comptoir
        if room.name != "Comptoir":
            print("\nVous devez être au comptoir pour acheter un sandwich. Allez au nord depuis la cafétéria.\n")
            return False

        # Check if player has enough money
        if player.money < 3:
            print(f"\nVous n'avez pas assez d'argent. Le sandwich coûte 3$ et vous avez {player.money}$.\n")
            return False

        # Check if player already has a sandwich
        if "sandwich" in player.inventory:
            print("\nVous avez déjà un sandwich. Mangez-le d'abord avant d'en acheter un autre !\n")
            return False

        # Check if Mission impossible quest is completed - GAME OVER if buying sandwich after
        if player.quest_manager:
            for quest in player.quest_manager.get_all_quests():
                if quest.title == "Mission impossible" and quest.is_completed:
                    print("\n" + "=" * 60)
                    print("💀 GAME OVER 💀")
                    print("=" * 60)
                    print("\nVous décidez d'acheter un sandwich à 3$...\n")
                    print("Alors que vous aviez ENFIN assez d'argent pour offrir")
                    print("le cadeau parfait à Victoria et conquérir son cœur,")
                    print("vous préférez vous goinfrer plutôt que de faire plaisir")
                    print("à votre bien-aimée.\n")
                    print("Victoria apprend que vous avez dépensé votre argent")
                    print("dans un vulgaire sandwich alors que vous étiez censé")
                    print("lui offrir le cadeau de ses rêves...\n")
                    print("Elle vous regarde avec dégoût et mépris.")
                    print("'Tu n'es qu'un égoïste pathétique !'\n")
                    print("💔 Vous avez perdu toute chance de conquérir Victoria.")
                    print("La gourmandise a eu raison de l'amour...\n")
                    print("=" * 60)
                    return "LOSE"

        # Buy the sandwich and add to inventory
        from item import Item
        player.money -= 3
        sandwich = Item(
            "sandwich",
            "un délicieux sandwich de la cafétéria",
            0.2
        )
        player.inventory["sandwich"] = sandwich
        
        print("\n🥪 L'employé vous présente un sandwich appétissant.\n")
        print("Employé: Ça fait 3$.\n")
        print("💰 Vous achetez le sandwich pour 3$.\n")
        print("💡 Tu préfères manger ou séduire Vic à toi de voir ?\n")
        print("Le sandwich est maintenant dans votre inventaire. Utilisez 'eat sandwich' pour le manger.\n")
        print(f"💰 Argent restant : {player.money}$\n")
        return True

    def eat(game, list_of_words, number_of_parameters):
        """Permet au joueur de manger un item comestible.
        Usage: `eat <item>`
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1].lower()
        player = game.player

        # Check if item is in inventory
        if item_name not in player.inventory:
            print(f"\nVous n'avez pas de {item_name} dans votre inventaire.\n")
            return False

        # Check if it's a sandwich
        if item_name != "sandwich":
            print(f"\nVous ne pouvez pas manger {item_name}.\n")
            return False

        # Eat the sandwich
        player.inventory.pop("sandwich")
        print("\n🥪 Vous dévorez le sandwich rapidement.\n")
        print("Mmmh, c'était délicieux ! Mais vous auriez pu économiser cet argent pour séduire Vic...\n")
        return True

    def climb(game, list_of_words, number_of_parameters):
        """Permet au joueur de monter l'escalier secret via la commande 'up'.
        Usage: `up`
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        room = player.current_room

        # Check if there's an upward exit
        if "U" not in room.exits or room.exits["U"] is None:
            print("\nIl n'y a pas d'escalier pour monter ici.\n")
            return False

        player.history.append(room)
        player.current_room = room.exits["U"]
        print(player.current_room.get_long_description())
        return True

    def descend(game, list_of_words, number_of_parameters):
        """Permet au joueur de descendre l'escalier secret via la commande 'down'.
        Usage: `down`
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        room = player.current_room

        # Check if there's a downward exit
        if "D" not in room.exits or room.exits["D"] is None:
            print("\nIl n'y a pas d'escalier pour descendre ici.\n")
            return False

        player.history.append(room)
        player.current_room = room.exits["D"]
        print(player.current_room.get_long_description())
        return True

    def read(game, list_of_words, number_of_parameters):
        """Permet au joueur de lire le contenu du carnet.
        Usage: `read <objet>` ou `read <objet> next/prev`
        """
        import random

        l = len(list_of_words)
        if l < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        item_name = list_of_words[1].lower()

        # Check if the player has the item in their inventory
        if item_name not in player.inventory:
            print(f"\nVous n'avez pas de {item_name} à lire.\n")
            return False

        # Check if it's the carnet
        if item_name != "carnet":
            print(f"\nVous ne pouvez pas lire {item_name}.\n")
            return False

        # Define all pages of the carnet
        pages = [
            # Page 1: Wish list
            {
                "title": "Page 1 - Ma liste de souhaits",
                "content": [
                    "Voici les choses que j'aimerais recevoir:",
                    "  • Un collier de diamants étincelants",
                    "  • Des chaussures Louboutin rouge vif",
                    "  • Un sac à main Hermès Birkin",
                    "  • Une montre Rolex en or",
                    "  • Un foulard Hermès en soie pure",
                    "  • Un parfum Chanel No. 5",
                ],
            },
            # Page 2: Family history
            {
                "title": "Page 2 - Mon enfance",
                "content": [
                    "Quand j'étais petite, ma mère m'emmenait au musée du Louvre.",
                    "Je me souviens des peintures impressionnantes, mais ce qui m'a vraiment",
                    "marquée, c'était la beauté des cadres dorés qui entouraient les œuvres.",
                    "Ma mère me disait: 'Victoria, la vraie beauté réside dans les détails.'",
                    "Je n'ai jamais oublié ces paroles.",
                ],
            },
            # Page 3: Friendship with Sophie
            {
                "title": "Page 3 - Sophie",
                "content": [
                    "Sophie prétend être ma meilleure amie, mais je sais qu'elle est jalouse.",
                    "Elle n'arrête pas de vouloir s'approprier mes vêtements et mes accessoires.",
                    "L'autre jour, elle a essayé de porter ma veste Chanel en cachette.",
                    "Je n'ai pas apprécié. On ne touche pas aux affaires de quelqu'un",
                    "sans sa permission, surtout les pièces de créateurs.",
                ],
            },
            # Page 4: School life
            {
                "title": "Page 4 - À l'école",
                "content": [
                    "J'ai remarqué que les gens jugent les autres à première vue.",
                    "C'est la raison pour laquelle je prends soin de mon apparence.",
                    "Les bonnes chaussures, les bons accessoires... tout compte.",
                    "Quand je porte mes Louboutin, les gens me traitent différemment.",
                    "Ils sont plus respectueux. C'est malheureusement comme ça que fonctionne le monde.",
                ],
            },
            # Page 5: Shopping adventure
            {
                "title": "Page 5 - Mon jour préféré",
                "content": [
                    "Hier, je suis allée faire du shopping aux Galeries Lafayette.",
                    "J'ai découvert une nouvelle collection de bijoux de créateurs.",
                    "Il y avait une bague en particulier... magnifique, délicate, intemporelle.",
                    "Elle coûtait trop cher pour moi, mais je pense souvent à elle.",
                    "Je la revois souvent dans mes rêves, brillant sous les lumières du magasin.",
                ],
            },
            # Page 6: Secret dream (with subtle hint about real gift)
            {
                "title": "Page 6 - Mon vrai rêve secret",
                "content": [
                    "Si je devais choisir un seul cadeau au monde... ce serait quelque chose",
                    "qui m'a été volé autrefois. Quelque chose qui avait une profonde signification.",
                    "C'était une bague - pas une Rolex ou un diamant extravagant -",
                    "mais une simple bague en or blanc avec une pierre bleue. Une bague que ma",
                    "grand-mère m'avait donnée avant de disparaître quand j'avais 10 ans.",
                    "Je la chercherai toute ma vie. Ce serait le plus beau cadeau du monde.",
                ],
            },
            # Page 7: Beauty routine
            {
                "title": "Page 7 - Mon rituel beauté",
                "content": [
                    "Chaque matin, je me réveille et je me demande qui je veux être ce jour.",
                    "Je me recoiffe, j'ajuste mon maquillage avec soin, je sélectionne mon parfum.",
                    "C'est mon moment personnel, où je deviens vraiment moi-même.",
                    "Certains pensent que c'est superficiel, mais pour moi, c'est une forme",
                    "d'art. Je suis une toile blanche que je peins chaque jour.",
                ],
            },
            # Page 8: Memories of mother
            {
                "title": "Page 8 - Ma mère",
                "content": [
                    "Ma mère travaillait dans la mode. Elle m'a appris à apprécier la qualité.",
                    "Elle disait que les vêtements bon marché se voient tout de suite.",
                    "Mais aussi qu'une personne vraie brille à travers les tissus.",
                    "Parfois, je sens son parfum autour de moi, même s'il y a des années",
                    "que je ne l'ai pas vue. Je pense qu'elle serait fière de moi.",
                ],
            },
            # Page 9: Insecurities
            {
                "title": "Page 9 - Mes peurs secrètes",
                "content": [
                    "Malgré tout ce que les gens voient, je suis terrifiée à l'idée",
                    "que quelqu'un découvre que je ne suis pas aussi riche qu'ils le pensent.",
                    "Je dois garder les apparences. Le luxe que j'affiche, c'est aussi",
                    "une protection, un mur entre le monde et ma véritable nature.",
                    "Parfois, j'aimerais juste être acceptée pour qui je suis, pas pour ce que j'ai.",
                ],
            },
            # Page 10: Future dreams
            {
                "title": "Page 10 - L'avenir",
                "content": [
                    "Je rêve d'une vie où je n'aurai pas besoin de tout ce luxe pour me sentir",
                    "valorisée. Un jour, peut-être, je trouverai quelqu'un qui m'aimera",
                    "malgré ma façade de matérialiste. Quelqu'un qui verra au-delà des vêtements",
                    "et des bijoux. Quelqu'un qui trouvera la vraie Victoria, celle",
                    "qui existe derrière le maquillage et la fierté.",
                ],
            },
            # Page 11: Recent reflections
            {
                "title": "Page 11 - Réflexions récentes",
                "content": [
                    "En vieillissant, j'ai commencé à réaliser que les choses matérielles",
                    "ne remplissent jamais vraiment le vide. L'amour de ma grand-mère,",
                    "le sourire de ma mère, ces choses-là ne peuvent pas s'acheter.",
                    "Si quelqu'un avait la gentillesse de chercher cette bague perdue...",
                    "ce serait un acte d'amour plus précieux que toutes les bijouteries du monde.",
                ],
            },
            # Page 12: Last page
            {
                "title": "Page 12 - Un dernier souhait",
                "content": [
                    "Je ferme ce carnet en espérant que personne ne le lira jamais.",
                    "Mais si quelqu'un le fait... sachez que derrière la fille superficielle",
                    "que vous voyez à l'école, il y a quelqu'un de brisée qui cherche désespérément",
                    "à se reconstruire. Peut-être qu'un jour, je trouverai le courage",
                    "de montrer ma vraie face au monde. En attendant, j'endure.",
                ],
            },
        ]

        print("\n" + "=" * 60)
        print("📖 CARNET DE VICTORIA - ÉDITION LUXE")
        print("=" * 60 + "\n")

        # Check for navigation command
        navigation = None
        if len(list_of_words) > 2:
            navigation = list_of_words[2].lower()

        # Handle page navigation
        if navigation == "next":
            player.carnet_current_page += 1
            if player.carnet_current_page >= len(pages):
                player.carnet_current_page = len(pages) - 1
                print("\n⚠️  Vous êtes à la dernière page du carnet.\n")
        elif navigation == "prev":
            player.carnet_current_page -= 1
            if player.carnet_current_page < 0:
                player.carnet_current_page = 0
                print("\n⚠️  Vous êtes à la première page du carnet.\n")
        else:
            # Reset to first page on initial read
            player.carnet_current_page = 0

        # Display current page
        current_page = pages[player.carnet_current_page]

        print("\n" + "=" * 60)
        print("📖 CARNET DE VICTORIA - ÉDITION LUXE")
        print("=" * 60 + "\n")
        print(f"\n--- {current_page['title']} ---\n")
        for line in current_page["content"]:
            print(line)
        print()

        # Display navigation info
        print("=" * 60)
        print(f"Page {player.carnet_current_page + 1}/{len(pages)}")
        if player.carnet_current_page > 0:
            print("Utilisez 'prev' pour la page précédente")
        if player.carnet_current_page < len(pages) - 1:
            print("Utilisez 'next' pour la page suivante")
        print("=" * 60 + "\n")

        # Set flag that player is reading carnet
        player.is_reading_carnet = True

        return True

    def next_page(game, list_of_words, number_of_parameters):
        """Aller à la page suivante du carnet.
        Usage: `next`
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player

        # Check if player is reading carnet
        if not player.is_reading_carnet:
            print("\nVous ne lisez pas le carnet en ce moment.\n")
            return False

        # Define all pages of the carnet (same as in read function)
        pages = [
            {
                "title": "Page 1 - Ma liste de souhaits",
                "content": [
                    "Voici les choses que j'aimerais recevoir:",
                    "  • Un collier de diamants étincelants",
                    "  • Des chaussures Louboutin rouge vif",
                    "  • Un sac à main Hermès Birkin",
                    "  • Une montre Rolex en or",
                    "  • Un foulard Hermès en soie pure",
                    "  • Un parfum Chanel No. 5",
                ],
            },
            {
                "title": "Page 2 - Mon enfance",
                "content": [
                    "Quand j'étais petite, ma mère m'emmenait au musée du Louvre.",
                    "Je me souviens des peintures impressionnantes, mais ce qui m'a vraiment",
                    "marquée, c'était la beauté des cadres dorés qui entouraient les œuvres.",
                    "Ma mère me disait: 'Victoria, la vraie beauté réside dans les détails.'",
                    "Je n'ai jamais oublié ces paroles.",
                ],
            },
            {
                "title": "Page 3 - Sophie",
                "content": [
                    "Sophie prétend être ma meilleure amie, mais je sais qu'elle est jalouse.",
                    "Elle n'arrête pas de vouloir s'approprier mes vêtements et mes accessoires.",
                    "L'autre jour, elle a essayé de porter ma veste Chanel en cachette.",
                    "Je n'ai pas apprécié. On ne touche pas aux affaires de quelqu'un",
                    "sans sa permission, surtout les pièces de créateurs.",
                ],
            },
            {
                "title": "Page 4 - À l'école",
                "content": [
                    "J'ai remarqué que les gens jugent les autres à première vue.",
                    "C'est la raison pour laquelle je prends soin de mon apparence.",
                    "Les bonnes chaussures, les bons accessoires... tout compte.",
                    "Quand je porte mes Louboutin, les gens me traitent différemment.",
                    "Ils sont plus respectueux. C'est malheureusement comme ça que fonctionne le monde.",
                ],
            },
            {
                "title": "Page 5 - Mon jour préféré",
                "content": [
                    "Hier, je suis allée faire du shopping aux Galeries Lafayette.",
                    "J'ai découvert une nouvelle collection de bijoux de créateurs.",
                    "Il y avait une bague en particulier... magnifique, délicate, intemporelle.",
                    "Elle coûtait trop cher pour moi, mais je pense souvent à elle.",
                    "Je la revois souvent dans mes rêves, brillant sous les lumières du magasin.",
                ],
            },
            {
                "title": "Page 6 - Mon vrai rêve secret",
                "content": [
                    "Si je devais choisir un seul cadeau au monde... ce serait quelque chose",
                    "qui m'a été volé autrefois. Quelque chose qui avait une profonde signification.",
                    "C'était une bague - pas une Rolex ou un diamant extravagant -",
                    "mais une simple bague en or blanc avec une pierre bleue. Une bague que ma",
                    "grand-mère m'avait donnée avant de disparaître quand j'avais 10 ans.",
                    "Je la chercherai toute ma vie. Ce serait le plus beau cadeau du monde.",
                ],
            },
            {
                "title": "Page 7 - Mon rituel beauté",
                "content": [
                    "Chaque matin, je me réveille et je me demande qui je veux être ce jour.",
                    "Je me recoiffe, j'ajuste mon maquillage avec soin, je sélectionne mon parfum.",
                    "C'est mon moment personnel, où je deviens vraiment moi-même.",
                    "Certains pensent que c'est superficiel, mais pour moi, c'est une forme",
                    "d'art. Je suis une toile blanche que je peins chaque jour.",
                ],
            },
            {
                "title": "Page 8 - Ma mère",
                "content": [
                    "Ma mère travaillait dans la mode. Elle m'a appris à apprécier la qualité.",
                    "Elle disait que les vêtements bon marché se voient tout de suite.",
                    "Mais aussi qu'une personne vraie brille à travers les tissus.",
                    "Parfois, je sens son parfum autour de moi, même s'il y a des années",
                    "que je ne l'ai pas vue. Je pense qu'elle serait fière de moi.",
                ],
            },
            {
                "title": "Page 9 - Mes peurs secrètes",
                "content": [
                    "Malgré tout ce que les gens voient, je suis terrifiée à l'idée",
                    "que quelqu'un découvre que je ne suis pas aussi riche qu'ils le pensent.",
                    "Je dois garder les apparences. Le luxe que j'affiche, c'est aussi",
                    "une protection, un mur entre le monde et ma véritable nature.",
                    "Parfois, j'aimerais juste être acceptée pour qui je suis, pas pour ce que j'ai.",
                ],
            },
            {
                "title": "Page 10 - L'avenir",
                "content": [
                    "Je rêve d'une vie où je n'aurai pas besoin de tout ce luxe pour me sentir",
                    "valorisée. Un jour, peut-être, je trouverai quelqu'un qui m'aimera",
                    "malgré ma façade de matérialiste. Quelqu'un qui verra au-delà des vêtements",
                    "et des bijoux. Quelqu'un qui trouvera la vraie Victoria, celle",
                    "qui existe derrière le maquillage et la fierté.",
                ],
            },
            {
                "title": "Page 11 - Réflexions récentes",
                "content": [
                    "En vieillissant, j'ai commencé à réaliser que les choses matérielles",
                    "ne remplissent jamais vraiment le vide. L'amour de ma grand-mère,",
                    "le sourire de ma mère, ces choses-là ne peuvent pas s'acheter.",
                    "Si quelqu'un avait la gentillesse de chercher cette bague perdue...",
                    "ce serait un acte d'amour plus précieux que toutes les bijouteries du monde.",
                ],
            },
            {
                "title": "Page 12 - Un dernier souhait",
                "content": [
                    "Je ferme ce carnet en espérant que personne ne le lira jamais.",
                    "Mais si quelqu'un le fait... sachez que derrière la fille superficielle",
                    "que vous voyez à l'école, il y a quelqu'un de brisée qui cherche désespérément",
                    "à se reconstruire. Peut-être qu'un jour, je trouverai le courage",
                    "de montrer ma vraie face au monde. En attendant, j'endure.",
                ],
            },
        ]

        player.carnet_current_page += 1
        if player.carnet_current_page >= len(pages):
            player.carnet_current_page = len(pages) - 1
            print("\n⚠️  Vous êtes à la dernière page du carnet.\n")
            return False

        # Display current page
        current_page = pages[player.carnet_current_page]

        print("\n" + "=" * 60)
        print("📖 CARNET DE VICTORIA - ÉDITION LUXE")
        print("=" * 60 + "\n")
        print(f"\n--- {current_page['title']} ---\n")
        for line in current_page["content"]:
            print(line)
        print()

        # Display navigation info
        print("=" * 60)
        print(f"Page {player.carnet_current_page + 1}/{len(pages)}")
        if player.carnet_current_page > 0:
            print("Utilisez 'prev' pour la page précédente")
        if player.carnet_current_page < len(pages) - 1:
            print("Utilisez 'next' pour la page suivante")
        print("=" * 60 + "\n")

        return True

    def prev_page(game, list_of_words, number_of_parameters):
        """Aller à la page précédente du carnet.
        Usage: `prev`
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player

        # Check if player is reading carnet
        if not player.is_reading_carnet:
            print("\nVous ne lisez pas le carnet en ce moment.\n")
            return False

        # Define all pages of the carnet (same as in read function)
        pages = [
            {
                "title": "Page 1 - Ma liste de souhaits",
                "content": [
                    "Voici les choses que j'aimerais recevoir:",
                    "  • Un collier de diamants étincelants",
                    "  • Des chaussures Louboutin rouge vif",
                    "  • Un sac à main Hermès Birkin",
                    "  • Une montre Rolex en or",
                    "  • Un foulard Hermès en soie pure",
                    "  • Un parfum Chanel No. 5",
                ],
            },
            {
                "title": "Page 2 - Mon enfance",
                "content": [
                    "Quand j'étais petite, ma mère m'emmenait au musée du Louvre.",
                    "Je me souviens des peintures impressionnantes, mais ce qui m'a vraiment",
                    "marquée, c'était la beauté des cadres dorés qui entouraient les œuvres.",
                    "Ma mère me disait: 'Victoria, la vraie beauté réside dans les détails.'",
                    "Je n'ai jamais oublié ces paroles.",
                ],
            },
            {
                "title": "Page 3 - Sophie",
                "content": [
                    "Sophie prétend être ma meilleure amie, mais je sais qu'elle est jalouse.",
                    "Elle n'arrête pas de vouloir s'approprier mes vêtements et mes accessoires.",
                    "L'autre jour, elle a essayé de porter ma veste Chanel en cachette.",
                    "Je n'ai pas apprécié. On ne touche pas aux affaires de quelqu'un",
                    "sans sa permission, surtout les pièces de créateurs.",
                ],
            },
            {
                "title": "Page 4 - À l'école",
                "content": [
                    "J'ai remarqué que les gens jugent les autres à première vue.",
                    "C'est la raison pour laquelle je prends soin de mon apparence.",
                    "Les bonnes chaussures, les bons accessoires... tout compte.",
                    "Quand je porte mes Louboutin, les gens me traitent différemment.",
                    "Ils sont plus respectueux. C'est malheureusement comme ça que fonctionne le monde.",
                ],
            },
            {
                "title": "Page 5 - Mon jour préféré",
                "content": [
                    "Hier, je suis allée faire du shopping aux Galeries Lafayette.",
                    "J'ai découvert une nouvelle collection de bijoux de créateurs.",
                    "Il y avait une bague en particulier... magnifique, délicate, intemporelle.",
                    "Elle coûtait trop cher pour moi, mais je pense souvent à elle.",
                    "Je la revois souvent dans mes rêves, brillant sous les lumières du magasin.",
                ],
            },
            {
                "title": "Page 6 - Mon vrai rêve secret",
                "content": [
                    "Si je devais choisir un seul cadeau au monde... ce serait quelque chose",
                    "qui m'a été volé autrefois. Quelque chose qui avait une profonde signification.",
                    "C'était une bague - pas une Rolex ou un diamant extravagant -",
                    "mais une simple bague en or blanc avec une pierre bleue. Une bague que ma",
                    "grand-mère m'avait donnée avant de disparaître quand j'avais 10 ans.",
                    "Je la chercherai toute ma vie. Ce serait le plus beau cadeau du monde.",
                ],
            },
            {
                "title": "Page 7 - Mon rituel beauté",
                "content": [
                    "Chaque matin, je me réveille et je me demande qui je veux être ce jour.",
                    "Je me recoiffe, j'ajuste mon maquillage avec soin, je sélectionne mon parfum.",
                    "C'est mon moment personnel, où je deviens vraiment moi-même.",
                    "Certains pensent que c'est superficiel, mais pour moi, c'est une forme",
                    "d'art. Je suis une toile blanche que je peins chaque jour.",
                ],
            },
            {
                "title": "Page 8 - Ma mère",
                "content": [
                    "Ma mère travaillait dans la mode. Elle m'a appris à apprécier la qualité.",
                    "Elle disait que les vêtements bon marché se voient tout de suite.",
                    "Mais aussi qu'une personne vraie brille à travers les tissus.",
                    "Parfois, je sens son parfum autour de moi, même s'il y a des années",
                    "que je ne l'ai pas vue. Je pense qu'elle serait fière de moi.",
                ],
            },
            {
                "title": "Page 9 - Mes peurs secrètes",
                "content": [
                    "Malgré tout ce que les gens voient, je suis terrifiée à l'idée",
                    "que quelqu'un découvre que je ne suis pas aussi riche qu'ils le pensent.",
                    "Je dois garder les apparences. Le luxe que j'affiche, c'est aussi",
                    "une protection, un mur entre le monde et ma véritable nature.",
                    "Parfois, j'aimerais juste être acceptée pour qui je suis, pas pour ce que j'ai.",
                ],
            },
            {
                "title": "Page 10 - L'avenir",
                "content": [
                    "Je rêve d'une vie où je n'aurai pas besoin de tout ce luxe pour me sentir",
                    "valorisée. Un jour, peut-être, je trouverai quelqu'un qui m'aimera",
                    "malgré ma façade de matérialiste. Quelqu'un qui verra au-delà des vêtements",
                    "et des bijoux. Quelqu'un qui trouvera la vraie Victoria, celle",
                    "qui existe derrière le maquillage et la fierté.",
                ],
            },
            {
                "title": "Page 11 - Réflexions récentes",
                "content": [
                    "En vieillissant, j'ai commencé à réaliser que les choses matérielles",
                    "ne remplissent jamais vraiment le vide. L'amour de ma grand-mère,",
                    "le sourire de ma mère, ces choses-là ne peuvent pas s'acheter.",
                    "Si quelqu'un avait la gentillesse de chercher cette bague perdue...",
                    "ce serait un acte d'amour plus précieux que toutes les bijouteries du monde.",
                ],
            },
            {
                "title": "Page 12 - Un dernier souhait",
                "content": [
                    "Je ferme ce carnet en espérant que personne ne le lira jamais.",
                    "Mais si quelqu'un le fait... sachez que derrière la fille superficielle",
                    "que vous voyez à l'école, il y a quelqu'un de brisée qui cherche désespérément",
                    "à se reconstruire. Peut-être qu'un jour, je trouverai le courage",
                    "de montrer ma vraie face au monde. En attendant, j'endure.",
                ],
            },
        ]

        player.carnet_current_page -= 1
        if player.carnet_current_page < 0:
            player.carnet_current_page = 0
            print("\n⚠️  Vous êtes à la première page du carnet.\n")
            return False

        # Display current page
        current_page = pages[player.carnet_current_page]

        print("\n" + "=" * 60)
        print("📖 CARNET DE VICTORIA - ÉDITION LUXE")
        print("=" * 60 + "\n")
        print(f"\n--- {current_page['title']} ---\n")
        for line in current_page["content"]:
            print(line)
        print()

        # Display navigation info
        print("=" * 60)
        print(f"Page {player.carnet_current_page + 1}/{len(pages)}")
        if player.carnet_current_page > 0:
            print("Utilisez 'prev' pour la page précédente")
        if player.carnet_current_page < len(pages) - 1:
            print("Utilisez 'next' pour la page suivante")
        print("=" * 60)

        return True

    def give(game, list_of_words, number_of_parameters):
        """Offrir un objet à un personnage.
        Usage: `give <item> <character>`
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(f"\nLa commande '{command_word}' prend 2 paramètres: <item> <character>.\n")
            return False

        item_name = list_of_words[1]
        character_name = list_of_words[2]
        player = game.player
        room = player.current_room

        # Check if the player has the item
        if item_name not in player.inventory:
            print(f"\nVous n'avez pas '{item_name}' dans votre inventaire.\n")
            return False

        # Check if the character is in the room
        if character_name not in room.inventory:
            print(f"\nIl n'y a pas de personnage nommé '{character_name}' ici.\n")
            return False

        # Special handling for giving gifts to Victoria (final quest)
        if character_name == "Victoria":
            # Check if the final quest is active
            quete_finale = None
            if player.quest_manager:
                for quest in player.quest_manager.get_all_quests():
                    if quest.title == "Le Cadeau Parfait":
                        quete_finale = quest
                        break

            if not quete_finale or not quete_finale.is_active:
                print("\nVictoria: Je n'accepte pas de cadeau de n'importe qui.")
                print("Reviens quand tu auras quelque chose de vraiment spécial.\n")
                return False

            # Check if it's the RIGHT gift (bague en or blanc avec pierre bleue)
            if item_name == "bague":
                # SUCCESS! The player found the right gift
                item = player.inventory.pop(item_name)
                
                print("\n" + "=" * 70)
                print("  ✨ MOMENT MAGIQUE ✨")
                print("=" * 70)
                print("\nVous tendez la bague en or blanc avec sa pierre bleue étincelante...")
                print("\nVictoria: *Les yeux écarquillés* C'est... c'est impossible...")
                print("Victoria: Cette bague... c'était celle de ma grand-mère !")
                print("Victoria: Je l'avais perdue il y a des années... Comment as-tu su ?")
                print("\nDes larmes coulent sur ses joues, brisant son masque de froideur.")
                print("\nVictoria: Tous ces objets de luxe... ils ne signifient rien comparé à ça.")
                print("Victoria: Tu as vraiment pris le temps de me comprendre...")
                print("Victoria: Personne ne l'avait jamais fait avant...")
                print("\n*Elle s'approche de vous et prend votre main*")
                print("\nVictoria: Tu sais... j'ai rejeté tellement de garçons.")
                print("Victoria: Parce qu'ils ne voyaient que mon apparence, mes vêtements, mon argent.")
                print("Victoria: Mais toi... tu as cherché à connaître mon cœur.")
                print("\n*Elle sourit, un vrai sourire, pas celui qu'elle montre d'habitude*")
                print("\nVictoria: Est-ce que... est-ce que tu voudrais sortir avec moi ?")
                print("Victoria: Vraiment sortir avec moi. Pas la Victoria matérialiste.")
                print("Victoria: Mais la vraie Victoria. Celle que tu viens de découvrir.")
                print("\n💝 Vous acceptez, bien sûr. Comment pourriez-vous refuser ?")
                print("\nVictoria: *rougit légèrement* Merci. Du fond du cœur, merci.")
                print("\n" + "=" * 70)
                print("\n💖 Victoria est maintenant votre petite amie !")
                print("\n Vous êtes officielement devenu son tenneur de sac à main attitré.")
                print("Vous avez réussi l'impossible : conquérir son cœur.\n")
                print("=" * 70 + "\n")

                # Complete the final quest
                if quete_finale and not quete_finale.is_completed:
                    quete_finale.complete_objective("Choisir le bon objet dans la réserve", player)
                    quete_finale.complete_objective("Offrir l'objet à Victoria", player)
                    quete_finale.is_completed = True

                return True

            # WRONG gifts - Victoria rejects with specific responses
            elif "collier" in item_name or "diamants" in item_name:
                print("\n" + "=" * 70)
                print("  💎 REFUS BRUTAL")
                print("=" * 70)
                print("\nVous tendez fièrement le collier de diamants...")
                print("\nVictoria: *Éclate de rire* Un collier ? Vraiment ?")
                print("Victoria: Tu crois que je vais m'impressionner avec des cailloux brillants ?")
                print("Victoria: J'en ai TROIS exactement comme celui-là dans mon coffre !")
                print("Victoria: C'est tellement... prévisible. Tellement basique.")
                print("Victoria: Les diamants ? Pfff, tout le monde peut en acheter.")
                print("Victoria: Je pensais que tu étais différent... Quelle déception.")
                print("\n*Elle vous tourne le dos avec mépris*")
                print("\nVictoria: Ne me reparle PLUS JAMAIS.")
                print("\n💔 Victoria refuse le collier et s'en va définitivement.")
                print("\n☠️ Vous avez perdu toute chance avec Victoria. GAME OVER.\n")
                print("=" * 70 + "\n")
                return "LOSE"

            elif "chaussures" in item_name or "louboutin" in item_name:
                print("\n" + "=" * 70)
                print("  👠 REFUS MÉPRISANT")
                print("=" * 70)
                print("\nVous présentez les chaussures Louboutin rouges...")
                print("\nVictoria: *Lève un sourcil* Des Louboutin ?")
                print("Victoria: Sérieusement ? Tu as vu mes pieds ?")
                print("Victoria: Ce sont des 36, et je fais du 37 et demi !")
                print("Victoria: Tu ne connais même pas ma pointure ? C'est pathétique.")
                print("Victoria: Et puis, le rouge ? Je déteste le rouge sur moi.")
                print("Victoria: Ça fait vulgaire. Ça manque de classe.")
                print("Victoria: Tu n'as AUCUNE idée de qui je suis vraiment.")
                print("\n*Elle repousse les chaussures avec dédain*")
                print("\nVictoria: On en reste là. Je ne veux plus te voir.")
                print("\n💔 Victoria est visiblement déçue et rompt tout contact.")
                print("\n☠️ Vous avez perdu toute chance avec Victoria. GAME OVER.\n")
                print("=" * 70 + "\n")
                return "LOSE"

            elif "sac" in item_name or "birkin" in item_name or "hermès" in item_name or "hermes" in item_name:
                print("\n" + "=" * 70)
                print("  👜 REFUS CINGLANT")
                print("=" * 70)
                print("\nVous offrez le sac Hermès Birkin avec espoir...")
                print("\nVictoria: Un Birkin ? Oh mon Dieu...")
                print("Victoria: Tu sais combien de filles rêvent d'avoir ce sac ?")
                print("Victoria: Toutes les filles superficielles et sans personnalité.")
                print("Victoria: Tu me prends pour qui ? Une influenceuse Instagram ?")
                print("Victoria: Ce sac, c'est le symbole parfait de la vacuité matérielle.")
                print("Victoria: Je pensais que tu avais compris que je cherchais quelque chose de... vrai.")
                print("Victoria: Mais non, tu es comme tous les autres. Superficiel.")
                print("\n*Elle croise les bras, glaciale*")
                print("\nVictoria: C'est terminé. Ne t'approche plus de moi.")
                print("\n💔 Victoria te regarde une dernière fois avec dégoût.")
                print("\n☠️ Vous avez perdu toute chance avec Victoria. GAME OVER.\n")
                print("=" * 70 + "\n")
                return "LOSE"

            elif "montre" in item_name or "rolex" in item_name:
                print("\n" + "=" * 70)
                print("  ⌚ REFUS CASSANT")
                print("=" * 70)
                print("\nVous tendez la montre Rolex en or...")
                print("\nVictoria: Une Rolex ? C'est une blague ?")
                print("Victoria: Mon père m'en a déjà offert DEUX pour mon anniversaire.")
                print("Victoria: Et celle-là est un modèle masculin ! Tu es aveugle ou quoi ?")
                print("Victoria: Elle est bien trop lourde pour mon poignet.")
                print("Victoria: Une Rolex, c'est le cadeau type du mec qui n'a aucune imagination.")
                print("Victoria: 'Oh, c'est cher, donc elle va forcément aimer' *imite une voix stupide*")
                print("Victoria: Pathétique. Vraiment pathétique.")
                print("\n*Elle rejette la montre d'un geste brusque*")
                print("\nVictoria: Va-t'en. Maintenant. Je ne veux plus te voir.")
                print("\n💔 Victoria semble blessée et vous chasse définitivement.")
                print("\n☠️ Vous avez perdu toute chance avec Victoria. GAME OVER.\n")
                print("=" * 70 + "\n")
                return "LOSE"

            elif "foulard" in item_name:
                print("\n" + "=" * 70)
                print("  🧣 REFUS HAUTAIN")
                print("=" * 70)
                print("\nVous offrez délicatement le foulard Hermès en soie...")
                print("\nVictoria: Un foulard ? Sérieux ?")
                print("Victoria: C'est le genre de cadeau qu'on offre à sa grand-mère !")
                print("Victoria: J'ai 17 ans, pas 70 ! Tu me prends pour qui ?")
                print("Victoria: Et puis, je suis allergique à la soie. Tu ne le savais pas ?")
                print("Victoria: Ah mais oui, bien sûr que tu ne le savais pas.")
                print("Victoria: Parce que tu ne m'as JAMAIS vraiment écoutée.")
                print("Victoria: Tu n'as fait que regarder mon apparence extérieure.")
                print("\n*Elle détourne le regard, blessée*")
                print("\nVictoria: Laisse-moi tranquille. Pour toujours.")
                print("\n💔 Victoria semble profondément blessée et vous rejette.")
                print("\n☠️ Vous avez perdu toute chance avec Victoria. GAME OVER.\n")
                print("=" * 70 + "\n")
                return "LOSE"

            elif "parfum" in item_name or "chanel" in item_name:
                print("\n" + "=" * 70)
                print("  🌸 REFUS AMER")
                print("=" * 70)
                print("\nVous présentez le flacon de Chanel No. 5...")
                print("\nVictoria: Du Chanel No. 5 ? *Soupir profond*")
                print("Victoria: C'est le parfum que ma mère portait...")
                print("Victoria: Avant qu'elle ne parte et m'abandonne.")
                print("Victoria: Tu crois vraiment que j'ai envie de sentir comme elle ?")
                print("Victoria: De me rappeler chaque jour qu'elle n'est plus là ?")
                print("Victoria: Ce parfum, c'est... c'est de la douleur en bouteille.")
                print("Victoria: Comment tu peux être aussi... aussi insensible ?")
                print("Victoria: Tu ne me connais pas du tout. Pas du tout.")
                print("\n*Des larmes de colère brillent dans ses yeux*")
                print("\nVictoria: *sanglote* Dégage ! DÉGAGE DE MA VIE !")
                print("\n💔 Victoria est effondrée. Vous l'avez profondément blessée.")
                print("\n☠️ Vous avez perdu toute chance avec Victoria. GAME OVER.\n")
                print("=" * 70 + "\n")
                return "LOSE"

            else:
                # WRONG gift - Victoria rejects it
                print("\n" + "-" * 70)
                print(f"\nVictoria regarde '{item_name}' avec confusion et déception...")
                print("\nVictoria: C'est quoi ça exactement ?")
                print("Victoria: Tu te moques de moi ? C'est ça ?")
                print("Victoria: Je pensais que tu étais sérieux, mais visiblement...")
                print("Victoria: C'est fini. Ne m'adresse plus jamais la parole.")
                print("\nVictoria refuse le cadeau et s'en va pour toujours.")
                print("\n💔 Peut-être aurais-tu dû mieux la connaître avant de choisir...")
                print("\n☠️ Vous avez perdu toute chance avec Victoria. GAME OVER.\n")
                print("-" * 70 + "\n")
                return "LOSE"

        else:
            print(f"\n{character_name} n'accepte pas les cadeaux.\n")
            return False
