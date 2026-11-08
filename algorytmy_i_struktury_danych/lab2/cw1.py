# Ćwiczenie 1: porównanie czasu inicjowania i wstawiania danych
# dla tablicy i listy.
#
# W Pythonie:
#   tablica = list   (elementy leżą w pamięci jeden za drugim, jak int tablica[n] w C++)
#   lista   = deque  (lista dwukierunkowa, odpowiednik list<int> z C++)

import time
from collections import deque

ROZMIARY = [1000, 10000, 100000]


def zmierz(funkcja, n):
    """Uruchamia funkcja(n) i zwraca czas w milisekundach."""
    start = time.perf_counter()
    funkcja(n)
    koniec = time.perf_counter()
    return (koniec - start) * 1000


# --- Inicjowanie: utworzenie struktury z liczbami 0, 1, ..., n-1 ---

def inicjuj_tablice(n):
    return list(range(n))


def inicjuj_liste(n):
    return deque(range(n))


# --- Wstawianie: dodanie n liczb na POCZĄTEK struktury ---

def wstaw_do_tablicy(n):
    tablica = []
    for i in range(n):
        tablica.insert(0, i)  # wszystkie elementy muszą przesunąć się o 1 w prawo
    return tablica


def wstaw_do_listy(n):
    lista = deque()
    for i in range(n):
        lista.appendleft(i)  # tylko podpięcie nowego elementu na początku
    return lista


def tabela(tytul, funkcja_tablica, funkcja_lista):
    print(f"\n{tytul}")
    print(f"{'rozmiar':>10} | {'tablica [ms]':>12} | {'lista [ms]':>12}")
    print("-" * 40)
    for n in ROZMIARY:
        t_tablica = zmierz(funkcja_tablica, n)
        t_lista = zmierz(funkcja_lista, n)
        print(f"{n:>10} | {t_tablica:>12.3f} | {t_lista:>12.3f}")


tabela("INICJOWANIE", inicjuj_tablice, inicjuj_liste)
tabela("WSTAWIANIE NA POCZĄTEK", wstaw_do_tablicy, wstaw_do_listy)
