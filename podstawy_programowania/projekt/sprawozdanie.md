# Sprawozdanie — Podstawy programowania (zadania projektowe)

**Przedmiot:** Podstawy programowania
**Zakres:** Zadania 3–10
**Środowisko:** powłoka `bash`, narzędzia kolekcji GNU (`cat`, `grep`, `sed`, `awk`, `diff`, `patch`, `paste`, `md5sum`, `tr`, `dos2unix`) oraz `magick` (ImageMagick); w systemie Windows uruchamiane w MSYS2.

> **Uwaga o końcach linii.** Pliki tekstowe pochodzące z Windows mają końce linii w formacie **CRLF** (`\r\n`), a systemy uniksowe używają **LF** (`\n`). Znak `\r` potrafi psuć wynik działania narzędzi takich jak `paste`, `awk`, `sed`, `patch` czy `md5sum`, dlatego w kilku zadaniach pierwszym krokiem jest ujednolicenie końców linii do LF (`dos2unix` lub `tr -d '\r'`).

---

## Zadanie 3 — Niesforne dane

### Cel
Plik `dane.txt` zawiera kolumnę liczb (jedna wartość w wierszu). Trzeba przekształcić go do pliku z **trzema kolumnami** i **nagłówkiem** (`x`, `y`, `z`), aby dało się go wczytać do arkusza kalkulacyjnego i naszkicować wykresy.

### Pliki
| Plik | Opis |
| --- | --- |
| `dane.txt` | Dane wejściowe — jedna kolumna, format CRLF (18 843 wierszy) |
| `dane_col.txt` | Trzy kolumny bez nagłówka (wynik `paste`) |
| `dane_col_header.txt` | Wynik końcowy — nagłówek + trzy kolumny (6 282 wiersze) |

### Rozwiązanie

**Krok 1 — konwersja końców linii (CRLF → LF).**
Bez tego `paste` dokleja `\r` do wartości i psuje kolumny.

```bash
dos2unix dane.txt
```

**Krok 2 — podział jednej kolumny na trzy.**
`paste - - -` czyta dane ze standardowego wejścia i skleja **kolejne trzy wiersze** w jeden, rozdzielając je tabulatorem. Każdy myślnik `-` to jedno „pole" pobierane z kolejnej linii.

```bash
paste - - - < dane.txt > dane_col.txt
```

**Krok 3 — dodanie nagłówka.**
`echo -e "x\ty\tz"` tworzy wiersz nagłówka rozdzielony tabulatorami, a `cat -` skleja go z danymi (`-` oznacza standardowe wejście, czyli wynik `echo`).

```bash
echo -e "x\ty\tz" | cat - dane_col.txt > dane_col_header.txt
```

### Wynik
```
x       y                       z
0       0                       0
0,001   0,000999999833333342    0,000159235589171981
...
```
Plik można bezpośrednio zaimportować do Excela lub LibreOffice Calc (separator: tabulator).

---

## Zadanie 4 — Dodawanie poprawek

### Cel
Istnieją dwie wersje listy słów: oryginał `lista.txt` (9 995 wierszy) i poprawiona `lista-pop.txt` (10 002 wiersze). Trzeba **wskazać różnice**, przygotować **łatkę (patch)** umożliwiającą aktualizację oryginału oraz **zweryfikować poprawność przez sumy MD5**.

### Pliki
| Plik | Opis |
| --- | --- |
| `lista.txt` | Oryginalna lista słów (9 995 wierszy, CRLF) |
| `lista-pop.txt` | Poprawiona lista (10 002 wiersze, CRLF) |
| `changes.patch` | Łatka w formacie unified diff |
| `lista_merged.txt` | Oryginał po nałożeniu łatki |

### Rozwiązanie

**Krok 1 — sprawdzenie różnic.**
`diff -u` pokazuje różnice w formacie *unified* (czytelnym dla `patch`). Różnice: **7 dodanych słów** w różnych miejscach listy.

```bash
diff -u lista.txt lista-pop.txt
```

**Krok 2 — wygenerowanie łatki.**
Najpierw oba pliki sprowadzamy do LF, żeby łatka była przenośna między systemami, potem zapisujemy różnice do pliku.

```bash
dos2unix lista.txt
dos2unix lista-pop.txt
diff -u --label lista.txt --label lista-pop.txt lista.txt lista-pop.txt > changes.patch
```

**Krok 3 — nałożenie łatki.**
Kopię oryginału aktualizujemy łatką — `patch` wczytuje różnice ze standardowego wejścia.

```bash
cp lista.txt lista_merged.txt
patch lista_merged.txt < changes.patch
```

**Krok 4 — weryfikacja przez MD5.**
Jeśli łatka nałożyła się poprawnie, suma kontrolna pliku po aktualizacji jest **identyczna** z sumą pliku docelowego.

```bash
md5sum lista_merged.txt
md5sum lista-pop.txt
```
```
683c1c85343c7337adfb13acb7598237  lista_merged.txt
683c1c85343c7337adfb13acb7598237  lista-pop.txt
```

> **Ważne:** porównanie MD5 plików w wersji CRLF dałoby **różne** sumy, bo każdy wiersz ma dodatkowy znak `\r`. Sumy porównujemy zawsze po ujednoliceniu końców linii do LF.

---

## Zadanie 5 — Z CSV do SQL i z powrotem

### Cel
Dwie konwersje formatów danych pomiarowych:
1. **CSV → SQL** — `steps-2sql.csv` (separator `;`) zamienić na instrukcje `INSERT INTO`.
2. **SQL → CSV** — `steps-2csv.sql` (instrukcje INSERT) zamienić na CSV, przy czym stempel czasu trzeba przeliczyć z **milisekund na sekundy** (usunięcie trzech ostatnich zer).

### Pliki
| Plik | Opis |
| --- | --- |
| `steps-2sql.csv` | Dane wejściowe CSV (czas w sekundach) |
| `steps-2sql.sql` | Wynik konwersji CSV → SQL |
| `steps-2csv.sql` | Dane wejściowe SQL (czas w milisekundach) |
| `steps-2csv.csv` | Wynik konwersji SQL → CSV (czas w sekundach) |

### Część 1: CSV → SQL

Dane wejściowe:
```
time;intensity;steps
1562001120;19;0
1562001180;23;0
```

Polecenie:
```bash
tr -d '\r' < steps-2sql.csv | \
awk -F';' 'NR>1 {printf "INSERT INTO stepsData (time, intensity, steps) VALUES (%s, %s, %s);\n", $1, $2, $3}' > steps-2sql.sql
```

- `tr -d '\r'` usuwa znaki `\r` (CRLF → LF), żeby ostatnia kolumna i średnik nie „uciekły" do nowej linii.
- `awk -F';'` ustawia średnik jako separator pól.
- `NR>1` pomija wiersz nagłówkowy.
- `printf` buduje gotową instrukcję SQL z trzech pól (`$1`, `$2`, `$3`).

Wynik:
```sql
INSERT INTO stepsData (time, intensity, steps) VALUES (1562001120, 19, 0);
INSERT INTO stepsData (time, intensity, steps) VALUES (1562001180, 23, 0);
```

### Część 2: SQL → CSV

Dane wejściowe (uwaga — `dateTime` w **milisekundach**, końcówka `000`):
```sql
INSERT INTO stepsData (dateTime, steps, synced) VALUES (1562004600000, 41, 0);
INSERT INTO stepsData (dateTime, steps, synced) VALUES (1562005200000, 65, 0);
```

Polecenie:
```bash
echo "dateTime;steps;synced" > steps-2csv.csv
sed 's/INSERT INTO stepsData (dateTime, steps, synced) VALUES (\(.*\)000, \(.*\), \(.*\));/\1;\2;\3/' \
  steps-2csv.sql >> steps-2csv.csv
```

- Najpierw zapisujemy wiersz nagłówka.
- Wyrażenie `sed` przechwytuje trzy grupy (`\(.*\)`): wartość czasu **bez** trzech końcowych zer, liczbę kroków i flagę `synced`, po czym składa je z separatorem `;`. Usunięcie `000` to właśnie konwersja milisekund na sekundy.

Wynik:
```
dateTime;steps;synced
1562004600;41;0
1562005200;65;0
```

---

## Zadanie 6 — Marudny tłumacz

### Cel
Mamy angielski plik językowy aplikacji `en-7.2.json5`. Trzeba:
1. Przygotować `pl-7.2.json5` z **podwojonymi liniami** — oryginał zostaje jako komentarz `//`, a kopia poniżej jest linią do przetłumaczenia (klucze muszą pozostać unikatowe, dlatego oryginał komentujemy).
2. Po wydaniu nowej wersji `en-7.4.json5` przygotować `pl-7.4.json5` zawierający **wyłącznie nowe frazy**, których nie było w 7.2.

### Pliki
| Plik | Opis |
| --- | --- |
| `en-7.2.json5` | Angielska wersja językowa 7.2 |
| `en-7.4.json5` | Angielska wersja językowa 7.4 (nowe klucze) |
| `pl-7.2.json5` | Plik do tłumaczenia — wszystkie klucze z 7.2 |
| `pl-7.4.json5` | Plik do tłumaczenia — tylko nowe klucze z 7.4 |

### Część 1: Generowanie `pl-7.2.json5`

```bash
awk '
  /^[[:space:]]*"/ {
    line = $0
    comment = line
    sub(/^([[:space:]]*)/, "// ", comment)
    print comment
    print line
    next
  }
  { print }
' en-7.2.json5 > pl-7.2.json5
```

Działanie: dla każdej linii zaczynającej się od cudzysłowu (czyli linii z kluczem JSON) `awk` tworzy kopię, zamienia wcięcie na `// ` i wypisuje **najpierw komentarz, potem oryginał**. Pozostałe linie (nawiasy, puste) przepisuje bez zmian (`{ print }`).

Wynik:
```json5
{
  // "401.help": "You're not authorized to access this page. ...",
  "401.help": "You're not authorized to access this page. ...",

  // "401.link.home-page": "Take me to the home page",
  "401.link.home-page": "Take me to the home page",
}
```

### Część 2: Generowanie `pl-7.4.json5` (tylko nowe frazy)

W systemie macOS potrzebny jest GNU grep (`ggrep`) ze względu na flagę `-P` (wyrażenia w stylu Perl).

**Krok 1 — wyodrębnienie kluczy z wersji 7.2:**
```bash
ggrep -oP '"[^"]+(?=":)' en-7.2.json5 > /tmp/keys_72.txt
```

**Krok 2 — wygenerowanie pliku tylko z nowymi frazami:**
```bash
{
  echo "{"
  ggrep -oP '"[^"]+(?=":)' en-7.4.json5 \
  | ggrep -vF -f /tmp/keys_72.txt \
  | while read key; do
      line=$(grep "${key}\":" en-7.4.json5 | head -1)
      stripped=$(echo "$line" | sed 's/^[[:space:]]*//')
      echo "// \"${stripped#\"}"
      echo "  \"${stripped#\"}"
    done
  echo "}"
} > pl-7.4.json5
```

Działanie:
- `ggrep -oP '"[^"]+(?=":)'` wyciąga same nazwy kluczy (tekst w cudzysłowie stojący przed `":`).
- `ggrep -vF -f /tmp/keys_72.txt` odfiltrowuje (`-v`) klucze, które już były w 7.2 — zostają tylko **nowe**.
- pętla `while` dla każdego nowego klucza odnajduje pełną linię w `en-7.4.json5` i wypisuje ją podwójnie (komentarz + linia do tłumaczenia), tak jak w części 1.

Wynik:
```json5
{
  // "form.upload": "Upload",
  "form.upload": "Upload",
  // "form.download": "Download",
  "form.download": "Download",
  // "nav.profile": "Profile",
  "nav.profile": "Profile",
  // "nav.help": "Help",
  "nav.help": "Help",
}
```

---

## Zadanie 7 — Fotografik gamoń

### Cel
Zdjęcia są spakowane w dwóch archiwach (`kopie-1.zip`, `kopie-2.zip`), a w środku znajdują się kolejne, dzienne archiwa ZIP. Trzeba wszystko rozpakować, **zmienić format na JPG**, ustawić rozdzielczość na **96 DPI** i przeskalować **wysokość do 720 pikseli** (szerokość proporcjonalnie). Wynik spakować do jednego `zdjecia.zip`.

### Skrypt `zadanie7.sh`
```bash
#!/bin/bash

mkdir -p tmp

unzip -o kopie-1.zip -d tmp/ && unzip -o kopie-2.zip -d tmp/

for zip in tmp/????-??-??.zip; do unzip -o "$zip" -d tmp/; done

for img in tmp/*.jpg tmp/*.png; do
    magick "$img" -density 96 -units PixelsPerInch -resize x720 "$img"
done

zip -j zdjecia.zip tmp/*.jpg

rm -rf tmp
```

### Omówienie kolejnych kroków
1. **`mkdir -p tmp`** — katalog roboczy, żeby nie mieszać plików tymczasowych z wynikowymi.
2. **Rozpakowanie** — najpierw dwa główne archiwa, potem pętla rozpakowuje wszystkie dzienne archiwa o nazwach `RRRR-MM-DD.zip` (maska `????-??-??.zip`).
3. **Konwersja i skalowanie** — `magick` ustawia gęstość 96 px/cal (`-density 96 -units PixelsPerInch`) i skaluje obraz do wysokości 720 px (`-resize x720`); pusta szerokość przed `x` oznacza dobranie jej automatycznie z zachowaniem proporcji.
4. **Pakowanie** — `zip -j` pakuje same pliki JPG bez ścieżek katalogów (flaga `-j` = *junk paths*).
5. **Sprzątanie** — `rm -rf tmp` usuwa katalog roboczy.

Uruchomienie: `bash zadanie7.sh`. Wynik: `zdjecia.zip`.

---

## Zadanie 8 — Wszędzie te PDF-y

### Cel
Z przygotowanych w zadaniu 7 zdjęć wygenerować **portfolio PDF** gotowe do druku. Na każdej stronie A4 ma być **8 fotografii** (2 kolumny × 4 wiersze), a pod każdym zdjęciem — nazwa pliku.

### Skrypt `zadanie8.sh`
```bash
#!/bin/bash

unzip -o zdjecia.zip -d zdjecia/

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

rm -rf zdjecia/
```

### Omówienie
- **`unzip`** rozpakowuje zdjęcia do katalogu `zdjecia/`.
- **`magick montage`** układa wiele obrazów w siatkę:
  - `-label '%f'` — pod każdym zdjęciem wstawia jego nazwę pliku (`%f`),
  - `-tile 2x4` — 2 kolumny na 4 wiersze, czyli 8 zdjęć na stronie,
  - `-geometry 370x260+5+10` — rozmiar każdej miniatury i odstępy,
  - `-page A4` — rozmiar strony dokumentu,
  - `-background white -fill black -pointsize 12` — białe tło i czarny podpis o rozmiarze 12 pt.
  - maska `*.[jJ][pP][gG]` łapie rozszerzenie `.jpg` niezależnie od wielkości liter.
- **`rm -rf zdjecia/`** sprząta katalog roboczy.

Uruchomienie: `bash zadanie8.sh`. Wynik: `portfolio.pdf`.

---

## Zadanie 9 — Porządki w kopiach zapasowych

### Cel
Otrzymaliśmy zbiór kopii zapasowych o nazwach `RRRR-MM-DD.zip` zrzuconych do jednego katalogu (**270 plików**, lata 2010–2024). Trzeba je **uporządkować w katalogi rok/miesiąc**, np. `2010/05/2010-05-22.zip`.

### Skrypt `zadanie9.sh`
```bash
#!/bin/bash

cd kopie/ || exit

for plik in *.zip; do
    if [ -f "$plik" ]; then
        IFS='-' read -r rok miesiac reszta <<< "$plik"
        mkdir -p "$rok/$miesiac"
        mv "$plik" "$rok/$miesiac/"
    fi
done
```

### Omówienie
- **`cd kopie/ || exit`** — wejście do katalogu z kopiami; jeśli się nie uda, skrypt kończy działanie.
- **`for plik in *.zip`** — pętla po wszystkich plikach ZIP leżących bezpośrednio w katalogu; `if [ -f "$plik" ]` upewnia się, że to plik.
- **`IFS='-' read -r rok miesiac reszta`** — rozdziela nazwę pliku po znaku `-`: pierwszy fragment to rok, drugi to miesiąc, reszta (dzień + `.zip`) trafia do zmiennej `reszta`.
- **`mkdir -p "$rok/$miesiac"`** tworzy katalog docelowy (`-p` nie zgłasza błędu, jeśli już istnieje), a **`mv`** przenosi do niego plik.

Struktura wynikowa:
```
kopie/
  2010/
    05/
      2010-05-22.zip
      2010-05-24.zip
    06/
      2010-06-03.zip
```

Uruchomienie: `bash zadanie9.sh`.

---

## Zadanie 10 — Galeria dla grafika

### Cel
Z szablonu strony (`galeria.zip`) wygenerować gotowy plik `galeria.html`, wstawiając wpisy dla **wszystkich zdjęć** z katalogu `zdjecia/` (266 plików JPG). Każde zdjęcie ma być linkiem do pełnego pliku i mieć podpis z nazwą.

### Skrypt `zadanie10.sh`
```bash
#!/bin/bash

unzip -o galeria.zip index.html

for plik in zdjecia/*.jpg; do
    nazwa="${plik##*/}"
    echo "<div class=\"responsive\"><div class=\"gallery\"><a target=\"_blank\" href=\"zdjecia/$nazwa\"><img src=\"zdjecia/$nazwa\"></a><div class=\"desc\">$nazwa</div></div></div>"
done > wpisy.txt

awk '/<!-- kolejne pliki galerii/{while((getline line < "wpisy.txt")>0) print line; next} 1' index.html > galeria.html

rm -f wpisy.txt index.html
```

### Omówienie
1. **`unzip -o galeria.zip index.html`** — wypakowuje z archiwum tylko szablon `index.html`.
2. **Pętla generująca wpisy** — dla każdego zdjęcia `${plik##*/}` obcina ścieżkę katalogu i zostawia samą nazwę pliku, a `echo` wypisuje gotowy blok HTML (link `<a>` + miniatura `<img>` + podpis `<div class="desc">`). Całość trafia do `wpisy.txt`.
3. **Wstawienie do szablonu** — `awk` szuka w szablonie komentarza-znacznika `<!-- kolejne pliki galerii` i w tym miejscu wkleja zawartość `wpisy.txt` (`getline` czyta plik linia po linii); końcowa `1` to skrót oznaczający „wypisz każdą pozostałą linię bez zmian".
4. **`rm -f wpisy.txt index.html`** — usuwa pliki robocze.

Uruchomienie: `bash zadanie10.sh`. Wynik: `galeria.html`.

---

## Podsumowanie

| Zadanie | Główne narzędzia | Efekt |
| --- | --- | --- |
| 3. Niesforne dane | `dos2unix`, `paste`, `cat`, `echo` | 1 kolumna → 3 kolumny z nagłówkiem |
| 4. Dodawanie poprawek | `diff`, `patch`, `dos2unix`, `md5sum` | Łatka + weryfikacja MD5 |
| 5. CSV ↔ SQL | `tr`, `awk`, `sed` | Konwersja w obie strony + przeliczenie czasu |
| 6. Marudny tłumacz | `awk`, `grep` (`ggrep`) | Plik z podwojonymi liniami + tylko nowe frazy |
| 7. Fotografik gamoń | `unzip`, `magick`, `zip` | JPG 96 DPI, wysokość 720 px |
| 8. Wszędzie te PDF-y | `magick montage` | Portfolio A4, 2×4 zdjęcia na stronie |
| 9. Porządki w kopiach | `bash`, `read`, `mkdir`, `mv` | 270 kopii w katalogach rok/miesiąc |
| 10. Galeria dla grafika | `bash`, `awk`, `unzip` | Strona HTML z 266 zdjęciami |

**Powtarzające się motywy projektu:**
- **Końce linii (CRLF vs LF)** — w zadaniach 3, 4 i 5 ujednolicenie do LF było warunkiem poprawnego działania narzędzi.
- **Filozofia strumieni i potoków** — operatory `|`, `<`, `>`, `>>` łączą małe narzędzia (`tr`, `awk`, `sed`, `grep`) w gotowe „linie produkcyjne" przetwarzania danych.
- **Automatyzacja przez skrypty** — zadania 7–10 to skrypty `bash` iterujące po plikach w katalogu, uruchamiane jednym poleceniem.
