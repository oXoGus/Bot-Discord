from math import sqrt


def facto(a, b, c):
    delta = int(b)**2 - 4*int(a)*int(c)
    if delta > 0 :
        x1 = (-b - sqrt(int(delta)))/(2*a)
        x2 = (-b + sqrt(int(delta)))/(2*a)
        x1 = int(x1)
        x2 = int(x2)
        print(f"{a}(x{'-' if x1 > 0 else '+'}{abs(x1)})(x{'-' if x2 > 0 else '+'}{abs(x2)})")
    elif delta == 0:
        x0 = -b/(2*c)
        print(f"f(x)={a}(x{'-' if x0 > 0 else '+'}{abs(x0)})²")
    else:
        print("il n'y a pas de forme facto")

facto(1,3,-4)