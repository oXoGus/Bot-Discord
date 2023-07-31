from math import sqrt
import turtle
import time


screen = turtle.Screen() #on crée la fenetre ou il y aura le dessin

tortue = turtle.Turtle() # on crée une tortue pour dessiner 


tortue.speed(10)



def facto(a, b, c):
    delta = int(b)**2 - 4*int(a)*int(c)
    if delta > 0 :
        x1 = (-b - sqrt(int(delta)))/(2*a)
        x2 = (-b + sqrt(int(delta)))/(2*a)
        x1 = int(x1)
        x2 = int(x2)
        return f"{a}(x{'-' if x1 > 0 else '+'}{abs(x1)})(x{'-' if x2 > 0 else '+'}{abs(x2)})"
    elif delta == 0:
        x0 = -b/(2*c)
        return f"f(x)={a}(x{'-' if x0 > 0 else '+'}{abs(x0)})²"
    else:
        return"il n'y a pas de forme facto"



def AGADADAGA(n):
    motInitial = input("Entrer le mot initial ?\n")
    while motInitial.isupper != True and not all(caractere in ['A', 'D', 'G'] for caractere in motInitial): 
        print('vous devez écrire un mot uniquement constituer de A, D ou G')
        motInitial = input("Entrer le mot initial ?\n")
    for i in range(n):
        motInitial = motInitial.replace("A", "GADADAGA")
    print(motInitial)
    for caractere in motInitial:
        if caractere == 'A':
            tortue.forward(10)
        elif caractere == 'D':
            tortue.right(90)
        elif caractere == 'G':
            tortue.left(90)
    

AGADADAGA(3)
turtle.done()