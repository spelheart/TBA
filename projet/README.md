# Nom du jeu 

**Module :** Apprentissage de la programmation avec PYTHON et C

**Auteurs :** Marvyn BAERT et Perrine JUREK

**Concept :** Jeu d'aventure textuel développé en Python

---

## Conception et univers du jeu

### Synopsis et univers

Vous incarnez un lycéen évoluant dans un établissment tout à fait normal (en apparence du moins).
Votre objectif ultime est de **séduire Victoria**, une élève du lycée. Pour gagner son coeur, vous devez accomplir diverses quêtes afin de récolter assez d'argent pour lui offrir un cadeau.

#### Les quêtes principales

Pour progresser, vous devez intéragir avec l'environnement et les personnages pour :

- Entrer en contact avec Max, un mec louche de l'école
- Mener l'enquête pour trouver le journal intime de Victoria
- Prendre des risques en volant les copies d'examen

---

### Personnages

Le jeu est peuplé de différents personnages avec lesquels vous devez intéragir :

- **Victoria :** l'intêret romantique du protagoniste
- **Sophie :** La meilleure amie de Victoria (qui ne l'apprécie pas tant que ça en réalité)
- **Max :** Un mec louche de l"école qui donne les missions au protagoniste
- **Lucas :** Le meilleur ami du protagoniste, une source précieuse d'informations
- **JP et l'autre :** Des personnages secondaires qui donnent du travail au protagoniste

---

### Environnement du jeu

Le lycée est composé de nombreux lieux explorables indispensables à l'intrigue (et d'autres un peu moins) : 

- **Zones communes :** Entrée, hall, caféteria, escaliers, toit
- **Zones de cours :** Salles de cours (1 et 2), salle de musique, salle d'art, gymnase
- **Zones spéciales :** Couloirs (en trois parties), salle des profs, pièce secrète, magasin de Max

### Conditions de victoire/défaite

#### Victoire

#### Défaite 

### Comment jouer ?

#### Installation

```bash
git clone https://github.com/spelheart/TBA.git
cd air_esiee_tba
```

#### Lancer le Jeu

**Mode terminal :**
```bash
python game.py
```

## Architecture technique et programmation

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

### Structuration

Le projet suit une architecture orientée objet avec les classes suivantes :

- `game.py` / `Game` : description de l'environnement, interface avec le joueur ;
- `room.py` / `Room` : propriétés génériques d'un lieu  ;
- `player.py` / `Player` : le joueur ;
- `command.py` / `Command` : les consignes données par le joueur ;
- `actions.py` / `Action` : les interactions entre .
- `item.py` / `Item` : .
- `character.py` / `Character` : .
- `quest.py` / `Quest` : .

### Diagramme de classes

### Diagramme de classes

``` mermaid
classDiagram
    class Game {
        +start()
        +run()
        +end()
    }
    
    class Room {
        -name: str
        -description: str
        -exits: dict
        +get_description()
        +get_exits()
    }
    
    class Player {
        -name: str
        -inventory: list
        -current_room: Room
        +take_item(item)
        +drop_item(item)
        +move(direction)
    }
    
    class Command {
        -action: str
        -parameter: str
        +parse()
        +execute()
    }
    
    class Action {
        -type: str
        +perform()
    }
    
    class Item {
        -name: str
        -description: str
    }
    
    class Character {
        -name: str
        -location: Room
        +talk_to()
        +give_quest()
    }
    
    class Quest {
        -title: str
        -description: str
        -reward: int
        +is_completed()
    }
    
    Game --> Player
    Game --> Room
    Player --> Room
    Player --> Item
    Room --> Character
    Character --> Quest
    Command --> Action
```

## Perspectives d'améliorations
## Perspectives d'améliorations




## Structuration


