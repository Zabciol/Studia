# Zadanie 3 – Niesforne dane

## Opis

Plik `dane.txt` zawiera dane liczbowe w jednej kolumnie.
Celem jest przekształcenie go do pliku z trzema kolumnami i nagłówkiem (`x`, `y`, `z`).

## Pliki

| Plik                  | Opis                                        |
| --------------------- | ------------------------------------------- |
| `dane.txt`            | Dane wejściowe – jedna kolumna, format CRLF |
| `dane_col.txt`        | Trzy kolumny (bez nagłówka), wynik `paste`  |
| `dane_col_header.txt` | Wynik końcowy – nagłówek + trzy kolumny     |

## Rozwiązanie

### 1. Konwersja znaków końca linii (CRLF → LF)

Windows używa sekwencji `CR LF` (`\r\n`), a Unix/macOS używa `LF` (`\n`).
Narzędzia takie jak `paste`, `awk`, `sed`, `grep` na systemach uniksowych mogą błędnie
interpretować `\r` jako część danych, co psuje wynik operacji.

```bash
dos2unix dane.txt
```

### 2. Podzielenie jednej kolumny na trzy

Komenda `paste - - -` czyta dane ze stdin i łączy kolejne trzy linie w jeden wiersz
z separatorem tabulatora:

```bash
paste - - - < dane.txt > dane_col.txt
```

### 3. Dodanie nagłówka kolumn

```bash
echo -e "x\ty\tz" | cat - dane_col.txt > dane_col_header.txt
```

Wynikowy plik `dane_col_header.txt` ma postać:

```
x       y                       z
00      0                       0
0,001   0,000999999833333342    0,000159235589171981
...
```

Plik można bezpośrednio zaimportować do arkusza kalkulacyjnego (Excel, LibreOffice Calc).
