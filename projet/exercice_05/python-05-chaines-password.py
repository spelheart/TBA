# Vos import ici
import string

def check_password(password):
    """
    Teste la robustesse d'un password

    Args:
        password: chaine de caractères

    Returns:
        True or False

    >>> check_password('A1213pokl')
    False
    >>> check_password('bAse730onE')
    True
    >>> check_password('asasasasasasasaas')
    False
    >>> check_password('QWERTYqwerty')
    False
    >>> check_password('123456123456')
    False
    >>> check_password('QwErTy911poqqqq')
    True
    """

    # Si la longueur n'est pas conforme, retourner False
    if len(password) < 10:
        return False
    # Si l'un des caractères n'est pas un chiffre, retourner False
    if not any(c.isdigit() for c in password):
        return False
    # Si l'un des caractères n'est pas une lettre minuscule, retourner False
    if not any(c.islower() for c in password):
        return False
    # Si l'un des caractères n'est pas une lettre majuscule, retourner False
    if not any(c.isupper() for c in password):
        return False
    # Si l'un des caractères n'est pas un chiffre, retourner False
    if not any(c.isdigit() for c in password):
        return False
    return True

    # Q : Où puis je trouver l'ensemble des lettres et des chiffres sans le reconstituer moi même ?
    # R : Jeter un oeil au module string
    
    return False

def main():
    # votre code de test ici...
    # Exemple :
    result = check_password('A1213pokl')
    print(result)
    

if __name__ == '__main__':
    main()