import math
from sympy import symbols, diff, lambdify, sympify

def regula_falsi(f, a, b, epsilon=1e-5, max_iter=100):
    for _ in range(max_iter):
        c = (a * f(b) - b * f(a)) / (f(b) - f(a))
        if f(c) == 0 or abs(f(c)) < epsilon:
            break
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
    return c

def newtonova_metoda(f, df, x0, epsilon=1e-5, max_iter=100):
    x = x0
    for _ in range(max_iter):
        x = x - f(x) / df(x)
        if abs(f(x)) < epsilon:
            break
    return x

def modifikovana_newtonova_metoda(f, df, ddf, x0, epsilon=1e-5, max_iter=100):
    x = x0
    for _ in range(max_iter):
        x = x - (f(x) * df(x)) / (df(x)**2 - f(x) * ddf(x))
        if abs(f(x)) < epsilon:
            break
    return x

def metoda_polovljenja(f, a, b, epsilon=1e-5, max_iter=100):
    if f(a) * f(b) > 0:
        print("Nije moguće garantovati konvergenciju metode polovljenja.")
        return None
    for _ in range(max_iter):
        c = (a + b) / 2
        if f(c) == 0 or abs(b - a) / 2 < epsilon:
            break
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
    return c

def sekantna_metoda(f, x0, x1, epsilon=1e-5, max_iter=100):
    for _ in range(max_iter):
        if f(x1) == f(x0):
            print("Dijeljenje s nulom u sekantnoj metodi.")
            return None
        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        if abs(x2 - x1) < epsilon:
            break
        x0, x1 = x1, x2
    return x2

# Korisnički unos
metoda = input("Izaberite metodu (1 za Regula Falsi, 2 za Newtonovu metodu, 3 za Modifikovanu Newtonovu metodu, 4 za Metodu polovljenja, 5 za Sekantnu metodu): ")
funkcija_str = input("Unesite funkciju (u Python sintaksi, koristite 'x' kao varijablu): ")
a = float(input("Unesite početnu tačku intervala: "))
b = float(input("Unesite krajnju tačku intervala: "))

# Priprema funkcije i njenih izvoda
x = symbols('x')
try:
    funkcija_sym = sympify(funkcija_str)
except Exception as e:
    print("Greška u unosu funkcije:", e)
    exit(1)
f = lambdify(x, funkcija_sym, modules=['math'])

if metoda == '1':
    rezultat = regula_falsi(f, a, b)
    print("Rezultat (Regula Falsi):", rezultat)
elif metoda == '2':
    df_sym = diff(funkcija_sym, x)
    df = lambdify(x, df_sym, modules=['math'])
    x0 = float(input("Unesite početnu tačku za Newtonovu metodu: "))
    rezultat = newtonova_metoda(f, df, x0)
    print("Rezultat (Newtonova metoda):", rezultat)
elif metoda == '3':
    df_sym = diff(funkcija_sym, x)
    ddf_sym = diff(df_sym, x)
    df = lambdify(x, df_sym, modules=['math'])
    ddf = lambdify(x, ddf_sym, modules=['math'])
    x0 = float(input("Unesite početnu tačku za Modifikovanu Newtonovu metodu: "))
    rezultat = modifikovana_newtonova_metoda(f, df, ddf, x0)
    print("Rezultat (Modifikovana Newtonova metoda):", rezultat)
elif metoda == '4':
    rezultat = metoda_polovljenja(f, a, b)
    print("Rezultat (Metoda polovljenja):", rezultat)
elif metoda == '5':
    x0 = float(input("Unesite prvu tačku za Sekantnu metodu: "))
    rezultat = sekantna_metoda(f, x0, b)
    print("Rezultat (Sekantna metoda):", rezultat)
else:
    print("Nepoznata metoda. Molim vas izaberite od 1 do 5.")