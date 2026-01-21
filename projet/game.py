"""Module principal du jeu d'aventure."""

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item, Instrument
from character import Character
from quest import Quest, QuestManager

DEBUG = True

# pylint: disable=line-too-long


def piano_effect(game):
    """Fonction appelée quand le joueur joue du piano.
    Descend l'escalier secret de la salle de musique.
    """
    print("\n🎹 Vous jouez une magnifique mélodie au piano...\n")
    print("Soudain, un grondement résonne dans la salle !")
    print(
        "L'escalier secret commence à descendre du plafond "
        "avec un bruit sourd...\n"
    )
    print("✨ Un escalier en colimaçon apparaît maintenant dans la salle !\n")
    print(
        "Vous pouvez maintenant utiliser 'up' et 'down' "
        "pour accéder à la salle secrète.\n"
    )

    # Connecter l'escalier secret
    for room in game.rooms:
        if room.name == "Salle de musique":
            for other_room in game.rooms:
                if other_room.name == "Salle secrète":
                    room.exits["U"] = other_room
                    other_room.exits["D"] = room


class Game:
    """Classe principale du jeu."""

    def __init__(self):
        """Initialise une nouvelle partie du jeu."""
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.actions = Actions()
        self.characters = []

    def setup(self):  # pylint: disable=too-many-locals,too-many-statements
        """Configure le jeu (commandes, salles, items, personnages)."""
        # Initialise les directions alias
        self.actions.setup()

        # Setup commands
        help_cmd = Command("help", " : afficher cette aide", Actions.help, 0, "Système")
        self.commands["help"] = help_cmd
        quit_cmd = Command("quit", " : quitter le jeu", Actions.quit, 0, "Système")
        self.commands["quit"] = quit_cmd
        go_cmd = Command(
            "go",
            " <direction> : se déplacer dans une direction cardinale (N, E, S, O)",
            Actions.go,
            1,
            "Déplacement"
        )
        self.commands["go"] = go_cmd
        back_cmd = Command("back", " : revenir à la pièce précédente", Actions.back, 0, "Déplacement")
        self.commands["back"] = back_cmd
        look_cmd = Command(
            "look",
            " : afficher les items ou les personnages présents dans la pièce",
            Actions.look,
            0,
            "Visualisation"
        )
        self.commands["look"] = look_cmd
        take_cmd = Command(
            "take",
            " <item> : ramasser un item présent dans la pièce",
            Actions.take,
            1,
            "Interaction"
        )
        self.commands["take"] = take_cmd
        drop_cmd = Command(
            "drop",
            " <item> : déposer un item de votre inventaire dans la pièce",
            Actions.drop,
            1,
            "Interaction"
        )
        self.commands["drop"] = drop_cmd
        check_cmd = Command("check", " : afficher les détails de votre "
                            "inventaire", Actions.check, 0, "Visualisation")
        self.commands["check"] = check_cmd
        talk_cmd = Command("talk", " <character> : parler à un personnage",
                           Actions.talk, 1, "Interaction")
        self.commands["talk"] = talk_cmd
        quests_cmd = Command("quests", " : afficher la liste de vos quêtes",
                             Actions.show_quests, 0, "Quêtes")
        self.commands["quests"] = quests_cmd
        quest_cmd = Command("quest", " <nom> : afficher les détails "
                           "d'une quête", Actions.show_quest_details, 1, "Quêtes")
        self.commands["quest"] = quest_cmd
        play_cmd = Command("play", " <instrument> : jouer d'un instrument", Actions.play, 1, "Interaction")
        self.commands["play"] = play_cmd
        read_cmd = Command("read", " <item> : lire", Actions.read, 1, "Interaction")
        self.commands["read"] = read_cmd
        up_cmd = Command("up", " : monter l'escalier", Actions.climb, 0, "Déplacement")
        self.commands["up"] = up_cmd
        down_cmd = Command("down", " : descendre l'escalier", Actions.descend, 0, "Déplacement")
        self.commands["down"] = down_cmd

        # Setup rooms
        hall_entree = Room(
            "Hall d'entrée",
            "le hall d'entrée du lycée, où des casiers métalliques sont installés pour y "
            "ranger vos chaussures d'extérieur, ou votre parapluie, ou encore décharger "
            "une part de votre sac à dos parcequ'on est pas hulk et porter 18 manuels "
            "c'est pas un objectif de vie.",
        )
        self.rooms.append(hall_entree)
        couloir1 = Room(
            "Premier couloir",
            "la première partie du couloir qui mène à la cafétéria, au couloir menant au "
            "gymnase ou au hall d'entrée. Tu peux aussi aller plus loin dans le couloir "
            "où il y aura d'autres salles, j'espère que t'es assez intelligent pour "
            "t'en douter tout seul hein.",
        )
        self.rooms.append(couloir1)
        salle1 = Room(
            "Salle de cours tout ce qu'il y a de plus banal",
            "une salle de cours, tout ce qu'il y a de plus banal. Y'a un placard à balais "
            "dans un coin, mais sinon rien d'intéressant.",
        )
        self.rooms.append(salle1)
        salle2 = Room(
            "Salle de cours tout ce qu'il y a de plus banal",
            "une salle de cours, pas forcèment très interressante, mais bon... faut bien "
            "travailler de temps en temps.",
        )
        self.rooms.append(salle2)
        musique = Room(
            "Salle de musique",
            "la salle de musique. Vous observez au milieu de la pièce un piano, un piano à "
            "queue plus précisément. Pas n'importe quel piano à queue, un piano Steinway & "
            "Sons Model D-274, le nec plus ultra des pianos à queue. Après y'a aussi une "
            "guitare et une batterie mais bon... on s'en fout un peu non ?",
        )
        self.rooms.append(musique)
        art = Room(
            "Salle d'art plastique",
            "la salle d'art plastique. Il y a des sculptures fait avec les viex chewing gum "
            "trouvés sous les tables, des peintures dignes d'enfants de 3 ans, tu sais "
            "ceux que tu donnais à ta prof en maternelle et que tu retrouvais dans la "
            "poubelle le lendemain et une tête de biche empaillée.",
        )
        self.rooms.append(art)
        couloir2 = Room(
            "Suite du couloir",
            "la deuxième partie du couloir , celle ci mène à la salle d'art plastique, au "
            "couloir menant au gymnase ou au hall d'entrée. Ah merde, c'est la description "
            "du premier ça. Oups...",
        )
        self.rooms.append(couloir2)
        couloir3 = Room("Fin du couloir",
                        "la fin du couloir. Déso mais t'iras pas plus loin.")
        self.rooms.append(couloir3)
        escalier = Room(
            "Escalier menant au toit",
            "un grand escalier en béton menant vers le toit. C'est un accès officiel à la "
            "terrasse, contrairement à l'escalier secret de la salle de musique.",
        )
        self.rooms.append(escalier)
        toit = Room(
            "Toit énorme de 70 m²",
            "vous êtes sur le toit de l'école. La vue est magnifique, vous pouvez voir toute "
            "la région d'ici. L'escalier normal par lequel vous êtes arrivé vous permet de "
            "redescendre.",
        )
        self.rooms.append(toit)
        entree = Room("Entrée de l'école",
                      "l'entrée de l'école. Vous faites face à une grande "
                      "porte vitrée.")
        self.rooms.append(entree)
        couloir_sport = Room("couloir menant au gymnase", ".")
        self.rooms.append(couloir_sport)
        gym = Room("Gymnase", ".")
        self.rooms.append(gym)
        cafet = Room("Cafétéria", ".")
        self.rooms.append(cafet)

        salle_secrete = Room(
            "Salle secrète",
            "une salle secrète cachée au dessus de la salle de musique. La salle est relativement petite,"
            "un vieux bureau de classe y est situé, c'est peut être une sorte de débaras abandonné."
            "ou pas qui sait, le mystère de cette salle reste entier."
        )
        self.rooms.append(salle_secrete)

        # Create exits for rooms
        hall_entree.exits = {"N": None, "E": couloir1, "S": None, "O": entree}
        salle2.exits = {"N": couloir2, "E": None, "S": None, "O": None}
        salle1.exits = {"N": None, "E": None, "S": couloir2, "O": None}
        couloir1.exits = {"N": cafet, "E": couloir2, "S": couloir_sport, "O": hall_entree}
        couloir2.exits = {"N": salle1, "E": couloir3, "S": salle2, "O": couloir1}
        couloir3.exits = {"N": art, "E": escalier, "S": musique, "O": couloir2}
        entree.exits = {"N": None, "E": hall_entree, "S": None, "O": None}
        escalier.exits = {"N": None, "E": None, "S": None, "O": couloir3, "U": toit, "D": None}
        toit.exits = {"N": None, "E": None, "S": None, "O": None, "U": None, "D": escalier}
        couloir_sport.exits = {"N": couloir1, "E": None, "S": gym, "O": None}
        gym.exits = {"N": couloir_sport, "E": None, "S": None, "O": None}
        art.exits = {"N": None, "E": None, "S": couloir3, "O": None}
        musique.exits = {"N": couloir3, "E": None, "S": None, "O": None, "U": None, "D": None}
        cafet.exits = {"N": None, "E": None, "S": couloir1, "O": None}
        salle_secrete.exits = {"N": None, "E": None, "S": None, "O": None, "U": None, "D": musique}

        # Add items to the hall d'entrée
        casier = Item(
            "casier",
            "un casier métallique verrouillé, idéal pour y ranger ses affaires",
            20,
        )
        sword = Item("sword", "une épée au fil tranchant comme un rasoir", 2)
        journal = Item("journal intime de Victoria", "un vieux journal intime jauni par le temps", 1)
        copie = Item("piles de copies d'examen", "une copie d'examen avec une note de 0/20", 1)
        hall_entree.inventory[casier.name] = casier
        hall_entree.inventory[sword.name] = sword
        musique.inventory[journal.name] = journal
        salle1.inventory[copie.name] = copie

        # Add instruments to music room
        piano = Instrument(
            "piano",
            "un magnifique piano à queue Steinway & Sons Model D-274",
            500,
            piano_effect,
        )
        guitare = Instrument(
            "guitare",
            "une belle guitare acoustique",
            2,
            lambda game: print(
                "\n🎸 Vous jouez de la guitare avec style ! La musique résonne mélodieusement dans la salle.\n"
            ),
        )
        batterie = Instrument(
            "batterie",
            "une batterie complète avec cymbales",
            50,
            lambda game: print("\n🥁 Vous jouez de la batterie avec énergie ! Le rythme envahit la salle.\n"),
        )

        musique.inventory[piano.name] = piano
        musique.inventory[guitare.name] = guitare
        musique.inventory[batterie.name] = batterie

        # Add items to the secret room
        canet = Item("canet", "un petit canet rouillé, probablement très ancien", 0.1)
        salle_secrete.inventory[canet.name] = canet

        # Add characters
        joseph = Character(
            "Joseph",
            "un personnage mystérieux",
            hall_entree,
            [
                "Salut, je m'appelle Joseph. Bienvenue en enfer...",
                "Je ne suis pas très bavard aujourd'hui.",
            ],
        )
        jolyne = Character(
            "Jolyne",
            "une jeune fille aux cheveux longs et aux yeux bleus",
            hall_entree,
            [
                "Je suis Jolyne, et je suis venue pour te tuer.",
                "Yare Yare Daze...",
            ],
        )
        victoria = Character(
            "Victoria",
            "une matérialiste extrême, Elle juge les gens à la marque de leurs chaussures.",
            toit,
            [
                "C'est mignon ce que tu dis, mais est-ce que ça brille ?",
                "Désolée, je ne parle pas aux gens qui portent du polyester.",
            ],
            immobile=True
        )
        sophie = Character(
            "Sophie",
            "la meilleure amie de Victoria (en vrai elle l'aime pas)",
            couloir2,
            ["Salut.", "Je ne."],
        )
        max_char = Character("Max", "un boug pas random du jeu", gym, ["Salut.", "Je ne."], immobile=True)

        hall_entree.inventory[joseph.name] = joseph
        hall_entree.inventory[jolyne.name] = jolyne
        toit.inventory[victoria.name] = victoria
        couloir2.inventory[sophie.name] = sophie
        gym.inventory[max_char.name] = max_char
        self.characters = [joseph, jolyne, victoria, sophie, max_char]

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
            reward="Épée de braves",
        )
        self.player.quest_manager.add_quest(quete_item)
        quete_item.activate()
        self.player.quest_manager.active_quests.append(quete_item)

        # 2. Quête de déplacement : aller à la cafétéria
        quete_deplacement = Quest(
            title="Explorer la Cafétéria",
            description="Rends-toi à la cafétéria.",
            objectives=["Visiter Cafétéria"],
            reward="Bon de réduction",
        )
        self.player.quest_manager.add_quest(quete_deplacement)
        quete_deplacement.activate()
        self.player.quest_manager.active_quests.append(quete_deplacement)

        # 3. Quête d'interaction : parler à Jolyne
        quete_interaction = Quest(
            title="Parler à Jolyne",
            description="Va parler à Jolyne pour récupérer 50 dollars.",
            objectives=["parler avec Jolyne"],
            reward="50 dollars",
        )
        self.player.quest_manager.add_quest(quete_interaction)
        quete_interaction.activate()
        self.player.quest_manager.active_quests.append(quete_interaction)

    def win(self):
        """Retourne True si toutes les quêtes sont complètes."""
        if not self.player.quest_manager:
            return False
        return all(quest.is_completed for quest in self.player.quest_manager.get_all_quests())

    def loose(self):
        """Retourne True si la condition de défaite est remplie."""
        if self.player.current_room.name == "Gymnase" and "sword" not in self.player.inventory:
            print("\n💀 Vous êtes entré au gymnase sans équipement ! Vous avez perdu !\n")
            return True
        return False

    def play(self):
        """Boucle principale du jeu."""
        self.setup()
        self.print_welcome()
        while not self.finished:
            if self.win():
                print("\n🏆 Félicitations ! Vous avez complété toutes les quêtes et gagné la partie !\n")
                self.finished = True
                break
            if self.loose():
                print("\n☠️ Vous avez perdu la partie.\n")
                self.finished = True
                break
            self.process_command(input("> "))

    def process_command(self, command_string) -> None:
        """Traite la commande saisie par le joueur."""
        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]
        if command_word not in self.commands:
            print("")
        else:
            command = self.commands[command_word]
            success = command.action(self, list_of_words, command.number_of_parameters)
            if success and command_word in ["go", "back"]:
                for character in self.characters:
                    character.move()

    def print_welcome(self):
        """Affiche le message de bienvenue et la description de départ."""
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        print(self.player.current_room.get_long_description())


def main():
    """Point d'entrée du jeu."""
    Game().play()


if __name__ == "__main__":
    main()
