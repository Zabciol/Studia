# Zadanie 10 - Galeria dla grafika

## Opis

Plik `galeria.zip` zawiera szablon strony internetowej z galeria.
Celem zadania jest wygenerowanie pliku `galeria.html`, w ktorym zostana umieszczone
wpisy dla wszystkich zdjec z katalogu `zdjecia`.
Kazde zdjecie powinno byc linkiem do pelnego pliku i miec podpis z nazwa pliku.

## Pliki

| Plik            | Opis                                      |
| --------------- | ----------------------------------------- |
| `galeria.zip`   | Szablon galerii zawierajacy `index.html`  |
| `zdjecia/`      | Katalog ze zdjeciami uzywanymi w galerii  |
| `zadanie10.sh`  | Skrypt generujacy wpisy HTML              |
| `galeria.html`  | Wynik koncowy - gotowa strona galerii     |

## Rozwiazanie

### 1. Rozpakowanie szablonu

Z archiwum `galeria.zip` rozpakowywany jest plik `index.html`.

```bash
unzip -o galeria.zip index.html
```

### 2. Wygenerowanie wpisow dla zdjec

Skrypt przechodzi po wszystkich plikach JPG w katalogu `zdjecia`.
Dla kazdego pliku pobierana jest sama nazwa, bez sciezki katalogu.

```bash
for plik in zdjecia/*.jpg; do
    nazwa="${plik##*/}"
    echo "<div class=\"responsive\"><div class=\"gallery\"><a target=\"_blank\" href=\"zdjecia/$nazwa\"><img src=\"zdjecia/$nazwa\"></a><div class=\"desc\">$nazwa</div></div></div>"
done > wpisy.txt
```

Wygenerowany fragment HTML dla jednego zdjecia ma postac:

```html
<div class="responsive"><div class="gallery"><a target="_blank" href="zdjecia/blue.jpg"><img src="zdjecia/blue.jpg"></a><div class="desc">blue.jpg</div></div></div>
```

### 3. Wstawienie wpisow do szablonu

Program `awk` odszukuje w szablonie miejsce oznaczone komentarzem
`<!-- kolejne pliki galerii` i wstawia tam wygenerowane wpisy z pliku `wpisy.txt`.

```bash
awk '/<!-- kolejne pliki galerii/{while((getline line < "wpisy.txt")>0) print line; next} 1' index.html > galeria.html
```

### 4. Usuniecie plikow tymczasowych

Po utworzeniu galerii usuwane sa pliki robocze.

```bash
rm -f wpisy.txt index.html
```

Wynikiem dzialania skryptu jest plik `galeria.html`.
Cale zadanie mozna wykonac jednym poleceniem:

```bash
bash zadanie10.sh
```
