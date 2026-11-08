# Ćwiczenie 3: dobieranie par do tańca z dwóch kolejek (kobiety i mężczyźni).
# Na parkiecie mogą być jednocześnie najwyżej 4 pary.
#
# Kolejka = deque: append dodaje osobę na koniec, popleft zabiera osobę z początku.
# (Zwykła lista też ma pop(0), ale musi wtedy przesunąć wszystkie pozostałe elementy.)

from collections import deque
from pathlib import Path

MAKS_PAR = 4
PLIK = Path(__file__).parent / "osoby.txt"  # plik obok skryptu, niezależnie skąd go uruchomisz

kobiety = deque()
mezczyzni = deque()

# Wczytanie osób z pliku, np. linia "F Jennifer Ingram"
with open(PLIK, encoding="utf-8") as plik:
    for linia in plik:
        linia = linia.strip()
        if linia == "":
            continue
        plec, osoba = linia.split(" ", 1)  # dzielimy tylko na pierwszej spacji
        if plec == "F":
            kobiety.append(osoba)
        else:
            mezczyzni.append(osoba)

print("Kolejka kobiet:     ", ", ".join(kobiety))
print("Kolejka mężczyzn:   ", ", ".join(mezczyzni))

taniec = 1
while kobiety and mezczyzni:  # dopóki obie kolejki nie są puste
    print(f"\nTaniec {taniec} - na parkiecie:")
    for _ in range(MAKS_PAR):
        if not kobiety or not mezczyzni:
            break
        kobieta = kobiety.popleft()
        mezczyzna = mezczyzni.popleft()
        print(f"  {mezczyzna:<20} + {kobieta}")
    taniec += 1

print("\nCzekają bez pary:")
if not kobiety and not mezczyzni:
    print("  nikt")
for osoba in kobiety:
    print(f"  {osoba} (F)")
for osoba in mezczyzni:
    print(f"  {osoba} (M)")
