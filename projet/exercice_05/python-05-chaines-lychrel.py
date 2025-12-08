def lychrel(n):
    """Retourne le nombre d'itérations nécessaires pour obtenir un nombre palindrome

    Args:
        n (int): nombre entier soumis au processus de Lychrel

    Returns:
        int: le nombre d'itérations nécessaires pour obtenir un nombre palindrome

    >>> n = 50
    >>> lychrel(n)
    1
    >>> n = 55
    >>> lychrel(n)
    2
    >>> n = 59
    >>> lychrel(n)
    3
    >>> n = 69
    >>> lychrel(n)
    4
    >>> n = 79
    >>> lychrel(n)
    6
    >>> n = 89
    >>> lychrel(n)
    24
    >>> n = 107
    >>> lychrel(n)
    1
    >>> n = 108
    >>> lychrel(n)
    1
    >>> n = 109
    >>> lychrel(n)
    2
    """
    k = 0
    str_n = str(n)
    if str_n in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        return 0
    if str_n == str_n[::-1]:
        str_n = str(n) + str(n)[::-1]
        n = int(str_n)
        k += 2
    while str_n != str_n[::-1]:
        n += int(str_n[::-1])
        str_n = str(n)
        k += 1
    return k

def main():
    # liste de nombres suspectés d'être des nombres de Lychrel
    x = [196, 295, 394, 493, 592, 689, 691, 788, 790, 879, 887, 978, 986]
    l = [ lychrel(i) for i in range(1,200) if i not in x ]
    print(l)
    p =[50, 55, 59, 69, 79, 89, 107, 108, 109]
    print([lychrel(i) for i in p])
    print(lychrel(1186060307891929990))
    

if __name__ == "__main__":
    main()
