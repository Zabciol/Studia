# Ćwiczenie 2: zamiana liczby n na system o podstawie b.
# Ten sam algorytm zrobiony trzy razy: na tablicy, na liście i na stosie.
#
# Algorytm:
#   1. reszta = n % b
#   2. n = n // b
#   3. jeśli n != 0, wróć do punktu 1
#   4. wypisz reszty w odwrotnej kolejności

from collections import deque

CYFRY = "0123456789ABCDEF"  # CYFRY[11] == "B", więc działa do podstawy 16


def przez_tablice(n, b):
    reszty = []
    while True:
        reszty.append(n % b)  # reszta trafia na koniec tablicy
        n = n // b
        if n == 0:
            break

    wynik = ""
    for reszta in reversed(reszty):  # czytamy tablicę od końca
        wynik += CYFRY[reszta]
    return wynik


def przez_liste(n, b):
    reszty = deque()
    while True:
        reszty.appendleft(n % b)  # reszta trafia na POCZĄTEK listy
        n = n // b
        if n == 0:
            break

    wynik = ""
    for reszta in reszty:  # kolejność jest już odwrócona, czytamy normalnie
        wynik += CYFRY[reszta]
    return wynik


def przez_stos(n, b):
    stos = []  # lista używana jako stos: append = push, pop = pop
    while True:
        stos.append(n % b)
        n = n // b
        if n == 0:
            break

    wynik = ""
    while stos:  # dopóki stos nie jest pusty
        wynik += CYFRY[stos.pop()]  # pop zdejmuje resztę włożoną jako ostatnia
    return wynik


n = int(input("Podaj liczbę n (>= 0): "))
b = int(input("Podaj podstawę b (2-16): "))

if n < 0 or b < 2 or b > 16:
    print("Niepoprawne dane.")
else:
    print(f"\n{n} w systemie o podstawie {b}:")
    print(f"  tablica: {przez_tablice(n, b)}")
    print(f"  lista:   {przez_liste(n, b)}")
    print(f"  stos:    {przez_stos(n, b)}")
