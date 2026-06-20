# Zadanie 8 - Wszedzie te PDF-y

## Opis

Plik `zdjecia.zip` zawiera zdjecia przygotowane w zadaniu 7.
Celem zadania jest wygenerowanie portfolio w formacie PDF, gotowego do wydruku.
Na kazdej stronie A4 powinno znalezc sie osiem fotografii: dwie kolumny i cztery wiersze.
Pod kazdym zdjeciem powinna byc widoczna nazwa pliku.

## Pliki

| Plik            | Opis                                      |
| --------------- | ----------------------------------------- |
| `zdjecia.zip`   | Dane wejsciowe - zdjecia z zadania 7      |
| `zadanie8.sh`   | Skrypt generujacy portfolio PDF           |
| `portfolio.pdf` | Wynik koncowy - dokument PDF ze zdjeciami |

## Rozwiazanie

### 1. Rozpakowanie zdjec

Zdjecia sa rozpakowywane do katalogu `zdjecia`.

```bash
unzip -o zdjecia.zip -d zdjecia/
```

### 2. Utworzenie portfolio

Do wygenerowania dokumentu PDF uzywany jest program `magick montage`.
Opcja `-label '%f'` dodaje pod zdjeciem nazwe pliku, a `-tile 2x4` uklada
osiem fotografii na stronie w dwoch kolumnach i czterech wierszach.

```bash
magick montage \
    -label '%f' \
    -pointsize 12 \
    -background white \
    -fill black \
    zdjecia/*.[jJ][pP][gG] \
    -tile 2x4 \
    -geometry 370x260+5+10 \
    -page A4 \
    portfolio.pdf
```

### 3. Usuniecie katalogu roboczego

Po utworzeniu pliku PDF katalog ze zdjeciami zostaje usuniety.

```bash
rm -rf zdjecia/
```

Wynikiem dzialania skryptu jest plik `portfolio.pdf`.
Cale zadanie mozna wykonac jednym poleceniem:

```bash
bash zadanie8.sh
```
