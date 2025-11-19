def is_magic(n):
    """retourne la vérité de "n est un nombre magique"

    Args:
        n (int): nombre entier à tester

    Returns:
        bool: True si "n est un nombre magique". False sinon

    
    >>> n = 1089
    >>> is_magic(n)
    True
    >>> n = 8019
    >>> is_magic(n)
    False
    >>> n = 10989
    >>> is_magic(n)
    True
    >>> n = 10898
    >>> is_magic(n)
    False
    >>> n = 109989
    >>> is_magic(n)
    True
    >>> n = 108898
    >>> is_magic(n)
    False
    >>> n = 1099989
    >>> is_magic(n)
    True
    >>> n = 1088898
    >>> is_magic(n)
    False
    >>> n = 10891089
    >>> is_magic(n)
    True
    >>> n = 10981089
    >>> is_magic(n)
    False
    >>> n = 10999989
    >>> is_magic(n)
    True
    >>> n = 10999898
    >>> is_magic(n)
    False
    """
    str_n = str(n)
    if n * 9 == int(str_n[::-1]):
        return True
    return False


def next_magic(n):
    """Retourne le plus petit nombre magique supérieur à n

    Args:
        n (int): nombre entier

    Returns:
        int: le plus petit nombre magique supérieur à n
    """
    n += 1
    while not is_magic(n):
        n += 1
    return n

def main():
    for i in range(100000):
        if is_magic(i):
            print(i)
    print(is_magic(1089))
    print(is_magic(8019))
    print(is_magic(10989))
    print(next_magic(1089))


if __name__ == "__main__":
    main()