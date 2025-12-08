def remove_vowels_it(s):
    """Retire les voyelles de la chaîne de caractère passée en paramètre

    Args:
        s (str): chaine de caractère à traiter

    Returns:
        str: chaine de caractère privée de ses voyelles

    >>> s = "elephant"
    >>> remove_vowels_it(s)
    'lphnt'
    >>> s = "crocodile"
    >>> remove_vowels_it(s)
    'crcdl'
    >>> s = "girafe"
    >>> remove_vowels_it(s)
    'grf'
    >>> s = "phacochere"
    >>> remove_vowels_it(s)
    'phcchr'
    >>> s = "ornithorynque"
    >>> remove_vowels_it(s)
    'rnthrnq'
    """
    out = ""
    for c in s:
        if c in "aeiouy": continue
        out += c
    return out

def remove_vowels_rec(s):
    """Retire les voyelles de la chaîne de caractère passée en paramètre

    Args:
        s (str): chaine de caractère à traiter

    Returns:
        str: chaine de caractère privée de ses voyelles

    >>> s = "elephant"
    >>> remove_vowels_rec(s)
    'lphnt'
    >>> s = "crocodile"
    >>> remove_vowels_rec(s)
    'crcdl'
    >>> s = "girafe"
    >>> remove_vowels_rec(s)
    'grf'
    >>> s = "phacochere"
    >>> remove_vowels_rec(s)
    'phcchr'
    >>> s = "ornithorynque"
    >>> remove_vowels_rec(s)
    'rnthrnq'
    """
    if not s: 
        return ""
    # base case
    if s[0] in "aeiouy":
        return remove_vowels_rec(s[1:])
    # recursive call si s starts with a vowel
    # recursive call if s starts with a consonant
    return s[0] + remove_vowels_rec(s[1:])

def main():
    pass
    s = "elephant"
    print(remove_vowels_it(s))

if __name__ == "__main__":
    main()