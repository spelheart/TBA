
# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.actions = Actions()
    
    # Setup the game
    def setup(self):
        # Initialise les directions alias
        self.actions.setup()

        # Setup commands
        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go
        back = Command("back", " : revenir à la pièce précédente", Actions.back, 0)
        self.commands["back"] = back
        
        # Setup rooms
        hall_entree = Room("Hall d'entrée", "une forêt enchantée. Vous entendez une brise légère à travers la cime des arbres.")
        self.rooms.append(hall_entree)
        couloir1 = Room("Premier couloir", "une immense tour en pierre qui s'élève au dessus des nuages.")
        self.rooms.append(couloir1)
        salle1 = Room("Salle de cours tout ce qu'il y a de plus banal", "une grotte profonde et sombre. Des voix semblent provenir des profondeurs.")
        self.rooms.append(salle1)
        salle2 = Room("Salle de cours tout ce qu'il y a de plus banal", "une grotte profonde et sombre. Des voix semblent provenir des profondeurs.")
        self.rooms.append(salle2)
        musique = Room("Salle de musique", "une grotte profonde et sombre. Des voix semblent provenir des profondeurs.")
        self.rooms.append(musique)
        art = Room("Salle d'art plastique", "une grotte profonde et sombre. Des voix semblent provenir des profondeurs.")
        self.rooms.append(art)
        couloir2 = Room("Suite du couloir", "un petit chalet pittoresque avec un toit de chaume. Une épaisse fumée verte sort de la cheminée.")
        self.rooms.append(couloir2)
        couloir3 = Room("Fin du couloir", "un marécage sombre et ténébreux. L'eau bouillonne, les abords sont vaseux.")
        self.rooms.append(couloir3)
        escalier = Room("Escalier menant au toit", "un énorme château fort avec des douves et un pont levis. Sur les tours, des flèches en or massif.")
        self.rooms.append(escalier)
        toit = Room("toit énorme de 70 m^2", "un énorme château fort avec des douves et un pont levis. Sur les tours, des flèches en or massif.")
        self.rooms.append(toit)
        entree = Room("Entrée de l'école", "un énorme château fort avec des douves et un pont levis. Sur les tours, des flèches en or massif.")
        self.rooms.append(entree)
        couloir_sport = Room("Couloir menant au gymnase", "un énorme château fort avec des douves et un pont levis. Sur les tours, des flèches en or massif.")
        self.rooms.append(couloir_sport)
        gym = Room("Castle", "un énorme château fort avec des douves et un pont levis. Sur les tours, des flèches en or massif.")
        self.rooms.append(gym)
        cafet = Room("Cafétéria", "un énorme château fort avec des douves et un pont levis. Sur les tours, des flèches en or massif.")
        self.rooms.append(cafet)
        
    
        # Create exits for rooms

        hall_entree.exits = {"N" : None, "E" : couloir1, "S" : None, "O" : entree, "M" : None, "D" : None}
        salle2.exits = {"N" : couloir2, "E" : None, "S" : None, "O" : None, "M" : None, "D" : None}
        salle1.exits = {"N" : None, "E" : None, "S" : couloir2, "O" : None, "M" : None, "D" : None}
        couloir1.exits = {"N" : cafet, "E" : couloir2, "S" : couloir_sport, "O" : hall_entree, "M" : None, "D" : None}
        couloir2.exits = {"N" : salle1, "E" : couloir3, "S" : salle2, "O" : couloir1, "M" : None, "D" : None}
        couloir3.exits = {"N" : art, "E" : escalier, "S" : musique, "O" : couloir2, "M" : None, "D" : None}
        entree.exits = {"N" : None, "E" : hall_entree, "S" : None, "O" : None, "M" : None, "D" : None}
        escalier.exits = {"N" : None, "E" : None, "S" : None, "O" : couloir3, "M" : toit, "D" : None}
        toit.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "M" : None, "D" : escalier}
        couloir_sport.exits = {"N" : couloir1, "E" : None, "S" : gym, "O" : None, "M" : None, "D" : None}
        gym.exits = {"N" : couloir_sport, "E" : None, "S" : None, "O" : None, "M" : None, "D" : None}
        art.exits = {"N" : None, "E" : None, "S" : couloir3, "O" : None, "M" : None, "D" : None}
        musique.exits = {"N" : couloir3, "E" : None, "S" : None, "O" : None, "M" : None, "D" : None}
        cafet.exits = {"N" : None, "E" : None, "S" : couloir1, "O" : None, "M" : None, "D" : None}

        # Setup player and starting room
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = entree

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print("")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description()) 
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
