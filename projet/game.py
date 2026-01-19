
# Description: Game class

# Import modules

DEBUG = True

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from quest import Quest, QuestManager

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.actions = Actions()
        self.characters = []
    
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
        look = Command("look", " : afficher les items présents dans la pièce courante", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " <item> : ramasser un item présent dans la pièce", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <item> : déposer un item de votre inventaire dans la pièce", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : afficher votre inventaire", Actions.check, 0)
        self.commands["check"] = check
        talk = Command("talk", " <character> : parler à un personnage", Actions.talk, 1)
        self.commands["talk"] = talk
        quests = Command("quests", " : afficher la liste de vos quêtes", Actions.show_quests, 0)
        self.commands["quests"] = quests
        quest = Command("quest", " <nom> : afficher les détails d'une quête", Actions.show_quest_details, 1)
        self.commands["quest"] = quest
        
        # Setup rooms
        hall_entree = Room("Hall d'entrée", "le hall d'entrée du lycée, où des casiers métalliques sont installés pour y ranger vos chaussures d’extérieur. ")
        self.rooms.append(hall_entree)
        couloir1 = Room("Premier couloir", "la première parite du couloir qui mène à la cafétéria, au couloir menant au gymnase ou au hall d'entrée. Tu peux aussi plus loin dans le couloir et il y aura d'autres salles, j'espère que t'es assez intelligent pour t'en douter tout seul hein.")
        self.rooms.append(couloir1)
        salle1 = Room("Salle de cours tout ce qu'il y a de plus banal", "une salle de cours, tout ce qu'il y a de plus banal. Y'a un placard à balais dans un coin, mais sinon rien d'intéressant.")
        self.rooms.append(salle1)
        salle2 = Room("Salle de cours tout ce qu'il y a de plus banal", "une salle de cours, pas forcèment très interressante, mais bon... faut bien travailler de temps en temps.")
        self.rooms.append(salle2)
        musique = Room("Salle de musique", "la salle de musique. Vous observez au milieu de la pièce un piano, un piano à queue plus précisément. Pas n'importe quel piano à queue, un piano Steinway & Sons Model D-274, le nec plus ultra des pianos à queue. Après y'a aussi une guitare et une batterie mais bon... on s'en fout un peu non ?")
        self.rooms.append(musique)
        art = Room("Salle d'art plastique", "la salle d'art plastique. Il y a des sculptures fait avec les viex chewing gum trouvés sous les tables, des peintures dignes d'enfants de 3 ans, tu sais ceux que tu donnais à ta prof en maternelle et que tu retrouvais dans la poubelle le lendemain et une tête de biche empaillée.")
        self.rooms.append(art)
        couloir2 = Room("Suite du couloir", "la deuxième partie du couloir qui mène à la salle d'art plastique, au couloir menant au gymnase ou au hall d'entrée. Ah merde, c'est la description du premier ça. Oups...")
        self.rooms.append(couloir2)
        couloir3 = Room("Fin du couloir", "la fin du couloir. Déso mais t'iras pas plus loin.")
        self.rooms.append(couloir3)
        escalier = Room("Escalier menant au toit", ".")
        self.rooms.append(escalier)
        toit = Room("toit énorme de 70 m^2", ".")
        self.rooms.append(toit)
        entree = Room("Entrée de l'école", "l'entrée de l'école. Vous faites face à une grande porte vitrée.")
        self.rooms.append(entree)
        couloir_sport = Room("couloir menant au gymnase", ".")
        self.rooms.append(couloir_sport)
        gym = Room("Gymnase", ".")
        self.rooms.append(gym)
        cafet = Room("Cafétéria", ".")
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

        # Add items to the hall d'entrée so they are visible via Room.get_inventory()
        casier = Item("casier", "un casier métallique verrouillé, idéal pour y ranger ses affaires", 20)
        sword = Item("sword", "une épée au fil tranchant comme un rasoir", 2)
        # store items by name in the room inventory dict
        hall_entree.inventory[casier.name] = casier
        hall_entree.inventory[sword.name] = sword

        # Add characters to the hall d'entrée so they are visible via Room.get_inventory()
        Joseph = Character("Joseph", "un personnage mystérieux", hall_entree, ["Salut, je m'appelle Joseph. Bienvenue en enfer...", "Je ne suis pas très bavard aujourd'hui."])
        Jolyne = Character("Jolyne", "une jeune fille aux cheveux longs et aux yeux bleus", hall_entree, ["Je suis Jolyne, et je suis venue pour te tuer.", "Yare Yare Daze..."])
        Victoria = Character("Victoria", "matérialiste extrême, Elle juge les gens à la marque de leurs chaussures.", entree, ["C'est mignon ce que tu dis, mais est-ce que ça brille ?", "Désolée, je ne parle pas aux gens qui portent du polyester."])
        
        # store items
        # Store characters by name in the room inventory dict
        hall_entree.inventory[Joseph.name] = Joseph
        hall_entree.inventory[Jolyne.name] = Jolyne
        entree.inventory[Victoria.name] = Victoria
        self.characters = [Joseph, Jolyne, Victoria]

        # Setup player and starting room
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = entree

        # Setup quest manager
        self.player.quest_manager = QuestManager(self.player)

        # 1. Quête d'item : récupérer l'épée dans le hall
        quete_item = Quest(
            title="L'Épée Légendaire",
            description="Récupère l'épée qui se trouve dans le hall d'entrée.",
            objectives=["Récupérer sword"],
            reward="Épée de braves"
        )
        self.player.quest_manager.add_quest(quete_item)
        quete_item.activate()
        self.player.quest_manager.active_quests.append(quete_item)

        # 2. Quête de déplacement : aller à la cafétéria
        quete_deplacement = Quest(
            title="Explorer la Cafétéria",
            description="Rends-toi à la cafétéria.",
            objectives=["Visiter Cafétéria"],
            reward="Bon de réduction"
        )
        self.player.quest_manager.add_quest(quete_deplacement)
        quete_deplacement.activate()
        self.player.quest_manager.active_quests.append(quete_deplacement)

        # 3. Quête d'interaction : parler à Jolyne
        quete_interaction = Quest(
            title="Parler à Jolyne",
            description="Va parler à Jolyne pour récupérer 50 dollars.",
            objectives=["parler avec Jolyne"],
            reward="50 dollars"
        )
        self.player.quest_manager.add_quest(quete_interaction)
        quete_interaction.activate()
        self.player.quest_manager.active_quests.append(quete_interaction)

    # Check if player has won
    def win(self):
        """
        Returns True if all quests are completed, False otherwise.
        """
        if not self.player.quest_manager:
            return False
        
        # Check if all quests are completed
        all_completed = all(quest.is_completed for quest in self.player.quest_manager.get_all_quests())
        return all_completed

    # Check if player has lost
    def loose(self):
        """
        Returns True if losing condition is met, False otherwise.
        Losing condition: entering a specific room without having a specific item.
        Example: entering the gym without the sword would be a losing condition.
        """
        # Example: If player enters gym without sword, they lose
        if self.player.current_room.name == "Gymnase" and "sword" not in self.player.inventory:
            print("\n💀 Vous êtes entré au gymnase sans équipement ! Vous avez perdu !\n")
            return True
        
        return False

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Check winning condition
            if self.win():
                print("\n🏆 Félicitations ! Vous avez complété toutes les quêtes et gagné la partie !\n")
                self.finished = True
                break
            
            # Check losing condition
            if self.loose():
                print("\n☠️ Vous avez perdu la partie.\n")
                self.finished = True
                break
            
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
            
            # Move NPCs only if the command is 'go' or 'back'
            if command_word in ["go", "back"]:
                for character in self.characters:
                    character.move()

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description()) 
    
def _setup_quests(self):
        """Initialize all quests."""
        exploration_quest = Quest(
            title="Grand Explorateur",
            description="Explorez tous les lieux de ce monde mystérieux.",
            objectives=["Visiter Forest"
                        , "Visiter Tower"
                        , "Visiter Cave"
                        , "Visiter Cottage"
                        , "Visiter Castle"],
            reward="Titre de Grand Explorateur"
        )

        travel_quest = Quest(
            title="Grand Voyageur",
            description="Déplacez-vous 10 fois entre les lieux.",
            objectives=["Se déplacer 10 fois"],
            reward="Bottes de voyageur"
        )

        discovery_quest = Quest(
            title="Découvreur de Secrets",
            description="Découvrez les trois lieux les plus mystérieux.",
            objectives=["Visiter Cave"
                        , "Visiter Tower"
                        , "Visiter Castle"],
            reward="Clé dorée"
        )

        # Add quests to player's quest manager
        self.player.quest_manager.add_quest(exploration_quest)
        self.player.quest_manager.add_quest(travel_quest)
        self.player.quest_manager.add_quest(discovery_quest)

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
