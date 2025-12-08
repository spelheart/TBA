#### Fonction secondaire


def ispalindrome(p:str) -> bool:

    # Vérifie si la chaîne est égale à son inverse
   
    if p == p[::-1]:
        return True
    
    return False

#### Fonction principale


def main():

    # vos appels à la fonction secondaire ici

    for s in ["radar", "kayak", "level", "rotor", "civique", "deifie"]:
        print(s, ispalindrome(s))


if __name__ == "__main__":
    main()