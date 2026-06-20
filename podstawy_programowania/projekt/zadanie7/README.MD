# Zadanie 7 - Fotografik gamon

## Opis

W plikach `kopie-1.zip` i `kopie-2.zip` znajduja sie spakowane archiwa ze zdjeciami.
Celem zadania jest rozpakowanie wszystkich danych, zmiana formatu plikow graficznych na JPG,
ustawienie rozdzielczosci na 96 DPI oraz przeskalowanie wysokosci zdjec do 720 pikseli.
Wynik nalezy zapisac w jednym archiwum `zdjecia.zip`.

## Pliki

| Plik           | Opis                                      |
| -------------- | ----------------------------------------- |
| `kopie-1.zip`  | Pierwsza czesc danych wejsciowych         |
| `kopie-2.zip`  | Druga czesc danych wejsciowych            |
| `zadanie7.sh`  | Skrypt wykonujacy cale przetwarzanie      |
| `zdjecia.zip`  | Wynik koncowy - zdjecia JPG w archiwum ZIP |

## Rozwiazanie

### 1. Utworzenie katalogu tymczasowego

Do rozpakowania plikow uzywany jest katalog `tmp`, aby nie mieszac plikow roboczych
z plikami wynikowymi.

```bash
mkdir -p tmp
```

### 2. Rozpakowanie danych wejsciowych

Najpierw rozpakowywane sa dwa glowne archiwa, a potem wszystkie archiwa dzienne
znajdujace sie w katalogu tymczasowym.

```bash
unzip -o kopie-1.zip -d tmp/ && unzip -o kopie-2.zip -d tmp/

for zip in tmp/????-??-??.zip; do
    unzip -o "$zip" -d tmp/
done
```

### 3. Konwersja i skalowanie zdjec

Program `magick` ustawia rozdzielczosc na 96 DPI i zmienia wysokosc kazdego obrazu
na 720 pikseli. Szerokosc jest dobierana automatycznie, z zachowaniem proporcji.

```bash
for img in tmp/*.jpg tmp/*.png; do
    magick "$img" -density 96 -units PixelsPerInch -resize x720 "$img"
done
```

### 4. Spakowanie wyniku

Gotowe pliki JPG sa pakowane do jednego archiwum.

```bash
zip -j zdjecia.zip tmp/*.jpg
```

### 5. Usuniecie plikow tymczasowych

Po zakonczeniu pracy katalog `tmp` jest usuwany.

```bash
rm -rf tmp
```

Cale zadanie mozna wykonac jednym poleceniem:

```bash
bash zadanie7.sh
```
