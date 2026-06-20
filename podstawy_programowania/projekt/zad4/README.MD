# Zadanie 4 – Dodawanie poprawek

## Opis

Mamy dwie wersje listy słów:

- `lista.txt` – oryginalna lista (format CRLF)
- `lista-pop.txt` – poprawiona wersja

Celem jest: sprawdzenie różnic, przygotowanie łatki (`patch`) i weryfikacja poprawności przez MD5.

## Pliki

| Plik            | Opis                                      |
| --------------- | ----------------------------------------- |
| `lista.txt`     | Oryginalna lista słów (9995 linii, CRLF)  |
| `lista-pop.txt` | Poprawiona lista słów (10002 linie, CRLF) |
| `changes.patch` | Łatka w formacie unified diff             |

## Rozwiązanie

### 1. Sprawdzenie różnic między plikami

```bash
diff -u lista.txt lista-pop.txt
```

Różnice: 7 dodanych słów w różnych miejscach listy.

### 2. Generowanie łatki

Oba pliki mają znaki końca linii CRLF (Windows). Przed wygenerowaniem łatki należy
przekonwertować je do LF, żeby patch był kompatybilny między platformami:

```bash
dos2unix lista.txt
dos2unix lista-pop.txt
diff -u --label lista.txt --label lista-pop.txt lista.txt lista-pop.txt > changes.patch
```

> Plik `changes.patch` w repozytorium został wygenerowany w ten sposób.

### 3. Aplikowanie łatki

Patch należy stosować na wersji pliku z LF:

```bash
cp lista.txt lista_merged.txt
patch lista_merged.txt < changes.patch
```

### 4. Weryfikacja przez MD5

Po zastosowaniu poprawek sumy MD5 obu plików (w wersji LF) powinny być identyczne:

```bash
md5sum lista_merged.txt
md5sum lista-pop.txt
```

Wynik (obie wartości są identyczne):

```
683c1c85343c7337adfb13acb7598237
683c1c85343c7337adfb13acb7598237
```

> **Uwaga:** Bezpośrednie porównanie MD5 plików CRLF da różne sumy, bo pliki różnią
> się liczbą linii (każda linia ma dodatkowy `\r`). Porównanie zawsze robimy po
> ujednoliceniu końców linii do LF.
