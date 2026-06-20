# Zadanie 9 - Porzadki w kopiach zapasowych

## Opis

W katalogu `kopie` znajduja sie pliki ZIP z kopiami zapasowymi.
Nazwy plikow maja postac `YYYY-MM-DD.zip`, np. `2010-05-22.zip`.
Celem zadania jest uporzadkowanie kopii w katalogach wedlug roku i miesiaca.

Przykladowy wynik:

```
kopie/
  2010/
    05/
      2010-05-22.zip
      2010-05-24.zip
    06/
      2010-06-03.zip
```

## Pliki

| Plik          | Opis                                  |
| ------------- | ------------------------------------- |
| `kopie-1.zip` | Pierwsza czesc danych wejsciowych     |
| `kopie-2.zip` | Druga czesc danych wejsciowych        |
| `kopie/`      | Katalog z uporzadkowanymi kopiami     |
| `zadanie9.sh` | Skrypt porzadkujacy pliki wedlug daty |

## Rozwiazanie

### 1. Przejscie do katalogu z kopiami

Skrypt rozpoczyna prace w katalogu `kopie`.
Jesli katalog nie istnieje, skrypt konczy dzialanie.

```bash
cd kopie/ || exit
```

### 2. Iteracja po plikach ZIP

Petla przechodzi po wszystkich plikach ZIP znajdujacych sie bezposrednio w katalogu `kopie`.

```bash
for plik in *.zip; do
    if [ -f "$plik" ]; then
        ...
    fi
done
```

### 3. Odczytanie roku i miesiaca z nazwy pliku

Nazwa pliku jest dzielona po znaku `-`.
Pierwszy element to rok, drugi element to miesiac.

```bash
IFS='-' read -r rok miesiac reszta <<< "$plik"
```

### 4. Utworzenie katalogu i przeniesienie pliku

Dla kazdego pliku tworzony jest katalog w postaci `rok/miesiac`,
a nastepnie plik ZIP jest przenoszony do odpowiedniego miejsca.

```bash
mkdir -p "$rok/$miesiac"
mv "$plik" "$rok/$miesiac/"
```

Cale zadanie mozna wykonac jednym poleceniem:

```bash
bash zadanie9.sh
```
