def syracuse(n: int) -> tuple[int, int, int]:
    """Calcule la suite de Syracuse à partir de n et retourne :"""

    tv = 0
    tva = 0
    am = n

    while n != 1 :
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1

        tv += 1

        if n > 1:
            tva += 1

        if n > am:
            am = n

    return tv, tva, am















    # initialisation des variables

    # tant que la suite n'est pas terminée :
    #   - calcul du n suivant
    #   - mise à jour du temps de vol (tv)
    #   - mise à jour du temps de vol en altitude (tva) si nécessaire
    #   - mise à jour de l'altitude maximale (am)

    # retour de tv, tva, am


def main():
    # exemple d'exécution
    n = 15
    tv, tva, am = syracuse(n)
    print(n, tv, tva, am)

if __name__ == "__main__":
    main()