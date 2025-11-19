import math as m

def est_premier(p):
    sp = m.sqrt(p)
    sps = m.ceil(sp)
    if p == 1 or p == 4:
        return False
    elif p == 2 or p == 3:
        return True
    else:
        for k in range (2, sps):
            if p%k ==0:
               return False
            
        return True

 

print(est_premier(731))
print(est_premier(733))