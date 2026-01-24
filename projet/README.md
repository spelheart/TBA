# Victoria's Secret Love

**Module :** Apprentissage de la programmation avec PYTHON et C

**Auteurs :** Marvyn BAERT et Perrine JUREK

**Concept :** Jeu d'aventure textuel développé en Python

---

**Lien de la vidéo de présentation :**

---

## 📚 Table des matières

1. [Le guide Utilisateur](#guide-utilisateur)
2. [Le guide Développeur](#guide-développeur)
3. [Les perspectives de développement](#perspectives-de-développement)

## Le guide utilisateur

### 🧩 Synopsis et univers

Vous incarnez un lycéen évoluant dans un établissment tout à fait normal (en apparence du moins).
Votre objectif ultime est de **séduire Victoria**, une élève du lycée. Pour gagner son coeur, vous devez accomplir diverses quêtes afin de récolter assez d'argent pour lui offrir un cadeau.

#### Les quêtes principales

Pour progresser, vous devez intéragir avec l'environnement et les personnages pour :

- Entrer en contact avec Maxou, un mec louche de l'école
- Mener l'enquête pour trouver le journal intime de Victoria
- Prendre des risques en volant les copies d'examen

### 🧑 Personnages

Le jeu est peuplé de différents personnages avec lesquels vous devez intéragir :

- **Victoria :** L'intêret romantique du protagoniste
- **Sophie :** La meilleure amie de Victoria (qui ne l'apprécie pas tant que ça en réalité)
- **Maxou :** Un mec louche de l'école qui donne les missions au protagoniste
- **Lucas :** Le meilleur ami du protagoniste, une source précieuse d'informations
- **JP et Patoche :** Des personnages secondaires qui donnent du travail au protagoniste
- **Proviseur :** Le proviseur du lycée 
- **professeur Koro :** Un professeur de l'école
- **Tunnel :** Un boug qui aide le protagoniste à passer de l'autre coté du terrain pour pas se prendre une balle

### 🧩 Environnement du jeu

Le lycée est composé de nombreux lieux explorables indispensables à l'intrigue (et d'autres un peu moins) : 

- **Zones communes :** Entrée, hall, caféteria, escaliers, toit
- **Zones de cours :** Salles de cours (1 et 2), salle de musique, gymnase
- **Zones spéciales :** Couloirs (en trois parties), salle des profs, pièce secrète, magasin de Maxou, comptoir de la caféteria 

### 🎲 Conditions de victoire/défaite

#### Victoire

- Conquérir Victoria

#### Défaite 

- Perdre le mini-jeu de Jolyne ou Joseph
- Se faire recaler par Victoria 
- Voler les copies devant le prof ou un élève
- Traverser le milieu du terrain pour rejoindre Max
- Manger le sandwich
- Prendre plus d'un objet dans la salle de Max

### 💻 Comment jouer ?

#### Installation

```bash
git clone https://github.com/spelheart/TBA.git
cd TBA
```

#### Lancer le Jeu

**Mode terminal :**
```bash
python game.py
```
---

## Le guide développeur

### Commandes et Gameplay 

Le jeu se contrôle via une série de commandes textuelles simples : 

| Commande | Paramètre | Description |
|----------|-----------|-------------|
| `look` | — | Observer l'environnement actuel |
| `go` | `<direction>` | Se déplacer dans une direction |
| `take` | `<objet>` | Prendre un objet |
| `drop` | `<objet>` | Poser un objet |
| `check` | — | Voir l'inventaire |
| `talk` | `<pnj>` | Parler à un personnage |
| `back` | — | Revenir à la salle précédente |
| `help` | — | Liste complète des commandes |
| `quit` | — | Quitter le jeu |
| `help_help` | — | Aider le protagoniste |
| `buy` | `<objet>` | Acheter |
| `eat` | `<objet>` | Manger |
| `up` | — | Se déplacer vers le haut |
| `down` | — | Se déplacer vers le bas |
| `open` | — | Ouvrir (un coffre fort par hasard) |
| `play` | — | Jouer d'un instrument |
| `give` | — | Offrir un objet à un personnage |
| `read` | — | Lire |
| `quests` | — | Afficher la liste des quêtes |
| `quest` | `<name>` | Afficher les détails d'une quête |

#### Exemples

```bash
> go E -

Voici les pièces que vous avez visitées :
- Entrée de l'école

Vous êtes dans le hall d'entrée du lycée, où des casiers métalliques sont installés pour y ranger vos chaussures d'extérieur, ou votre parapluie, ou encore décharger une part de votre sac à dos parcequ'on est pas hulk et porter 18 manuels c'est pas un objectif de vie.

> look
La pièce contient :
    - Joseph : un personnage mystérieux 

> talk Joseph

⚠️ Joseph: Tu aurais pas dû faire ça...
Il te prend en chasse!
Salut, je m'appelle Joseph. Bienvenue en enfer...
```

### Structuration

Le projet suit une architecture orientée objet avec les classes suivantes :

- `game.py` / `Game` : Description de l'environnement, interface avec le joueur ;
- `room.py` / `Room` : Structure des lieux et des sorties ;
- `player.py` / `Player` : Caractéristiques et inventaire joueur ;
- `command.py` / `Command` : Consignes données par le joueur ;
- `actions.py` / `Action` : Exécution logique des commandes ;
- `item.py` / `Item`, `Instrument` : Objets et instruments de musique ;
- `character.py` / `Character` : Comportements et déplacement des PNJ ;
- `quest.py` / `Quest`, `QuestManager` : Système complet de missions narratives ;

### Diagramme de classes

``` mermaid

classDiagram

    class Game {
        - finished : bool
        - rooms : list
        - commands : dict
        - player : Player
        - actions : Actions
        - characters : list
        + __init__(self) -> None
        + setup(self) -> None
        + play(self) -> None
        + win(self) -> bool
        + loose(self) -> bool
        + print_welcome(self) -> None
    }
    
    class Room {
        - name : str
        - description : str
        - exits : dict
        - inventory : dict
        - characters : dict
        + __init__(name,description) -> None
        + get_exit(direction) -> Room
        + get_exit_string() -> str
        + get_long_description() -> str
        + get_inventory() -> str
    }
    
    class Player {
        - name : str
        - inventory : dict
        - current_room : Room
        - max_weight : float
        - money : int
        - history : list
        - talked_to_max : bool
        - maxou_room_unlocked : bool
        - casier_opened : bool
        - hunted_by_joseph/jolyne : bool
        - quest_manager : QuestManager
        + __init__(name,max_weight) -> None
        + get_current_weight() -> float
        + move(direction) -> bool
        + get_history() -> str
        + get_inventory() -> str
        + add_reward(reward_text) -> bool
    }
    
    class Command {
        - command_word : str
        - help_string : str
        - action : function
        - number_of_parameters : int
        - category : str
        + __init(command_word,help_string,action,number_of_parameters,category) -> None
        + __str__() -> str
    }
    
    class Action {
        - aliases : dict
        + setup(self) -> None
        + go(game,list_of_words,num_params) -> bool/str
        + talk(game,list_of_words,num_params) -> bool/str
        + take(game,list_of_words,num_params) -> bool/str
        + drop(game,list_of_words,num_params) -> bool
        + look(game,list_of_words,num_params) -> bool
        + check(game,list_of_words,num_params) -> bool
        + back(game,list_of_words,num_params) -> bool
        + help_help(game,list_of_words,num_params) -> bool
        + quit(game,list_of_words,num_params) -> bool
        + eat(game,list_of_words,num_params) -> bool
        + give(game,list_of_words,num_params) -> bool
    }
    
    class Item {
        - name : str
        - description : str
        - weight : float
        + __init__(name,description,weight) -> None
        + __str__() -> str
    }

    class Instrument {
        - effect : str
        + __init__(name,desc,weight,effect) -> None
        + __str__() -> str
    }

    
    class Character {
        - name : str
        - description : str
        - current_room : Room
        - msgs : list
        - immobile : bool
        - patrol_rooms : list
        - is_patrolling : bool
        - escape_phrases : list 
        + __init__(arguments) -> None
        + __str__() -> str
        + get_msg() -> str
        + move() -> bool
    }
    
    class Quest {
        - title : str
        - objectives : list
        - is_completed : bool
        - reward : str
        + activate() -> None
        + complete_objective(objective,player) -> bool
        + get_status() -> str
    }

    class QuestManager {
        - quests : list
        - active_quests : list
        + add_quest(quest) -> None
        + check_room_objectives(room_mane) -> None
        + show_quests() -> None
    }
    
    Game *-- Player
    Game *-- Room
    Game *-- Action
    Game *-- Command
    Room *-- Character
    Room *-- Item
    Player *-- Room
    Player *-- Item
    Game *-- Quest
    Game *-- QuestManager
    Instrument `-- Item
    

```

---

## Les perspectives de développement

### 🌍 Accessibilité et Localisation

- Francisation complète : Uniformiser l'expérience utilisateur en passant l'intégralité des commandes et des interactions en français.

- Internationalisation (i18n) : Traduire le jeu en plusieurs langues (anglais, espagnol, etc.) pour toucher une audience mondiale

### 🖥️ Interface et Expérience Utilisateur (UX/UI)

- Interface Graphique (GUI) : Passer d'une version textuelle à une véritable interface visuelle (avec des boutons, des barres de progression pour la relation avec Vic, et des visuels pour les mini-jeux).

### 🎮 Enrichissement du Gameplay

- Système de sauvegarde : Permettre au joueur de reprendre sa partie après une défaite (particulièrement utile après avoir mangé ce fameux sandwich !).

- Arborescence narrative : Développer davantage de conséquences pour chaque défaite afin que le jeu ait une plus grande rejouabilité.



