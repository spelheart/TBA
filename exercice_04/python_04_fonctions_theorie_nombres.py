from python_03_controle_premiers import est_premier


def fermat(n:int):
    Fn = 2**(2**n) + 1
    return Fn
def main():
    for i in range (0,6):
        print(f"Fermat F({i}) = {fermat(i)}")

if __name__ == "__main__":
    main()

def first_non_prime_fermat():
    F0 = fermat(0)
    return est_premier(F0)
print(first_non_prime_fermat())


def couple_prime_after(n:int):
    p = n+1
    while not(est_premier(p) and est_premier(p+2)):
        p +=1
    return p
        

print(couple_prime_after(1000000))

def germain_prime_after(n:int):
    p = n+1
    while not(est_premier(p) and est_premier(2*p +1 )):
        p +=1
    return p

print(germain_prime_after(1000000))




















