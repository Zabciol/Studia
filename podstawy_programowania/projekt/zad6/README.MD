# Zadanie 6 – Marudny tłumacz

## Opis

Mamy angielską wersję językową aplikacji w pliku `en-7.2.json5`.
Celem jest przygotowanie pliku `pl-7.2.json5` z podwójnymi wpisami
(oryginał jako komentarz + linia do tłumaczenia), a następnie
obsługa nowej wersji programu (`en-7.4.json5`) przez wygenerowanie
`pl-7.4.json5` zawierającego **wyłącznie nowe frazy**.

## Pliki

| Plik           | Opis                                          |
| -------------- | --------------------------------------------- |
| `en-7.2.json5` | Angielska wersja językowa 7.2                 |
| `en-7.4.json5` | Angielska wersja językowa 7.4 (nowe klucze)   |
| `pl-7.2.json5` | Plik do tłumaczenia – wszystkie klucze z 7.2  |
| `pl-7.4.json5` | Plik do tłumaczenia – tylko nowe klucze z 7.4 |

---

## Część 1: Generowanie `pl-7.2.json5`

Każda linia z kluczem JSON jest dublowana – oryginał trafia jako komentarz `//`,
a kopia zostaje jako linia do tłumaczenia.

### Polecenie

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

### Wynik (`pl-7.2.json5`)

```json5
{
  // "401.help": "You're not authorized to access this page. You can use the button below to get back to the home page.",
  "401.help": "You're not authorized to access this page. You can use the button below to get back to the home page.",

  // "401.link.home-page": "Take me to the home page",
  "401.link.home-page": "Take me to the home page",
  ...
}
```

---

## Część 2: Generowanie `pl-7.4.json5` (tylko nowe frazy)

W wersji 7.4 pojawiły się nowe klucze nieobecne w 7.2.
Plik `pl-7.4.json5` zawiera wyłącznie te nowe frazy.

### Krok 1: Wyodrębnij klucze z wersji 7.2

dla macOs wymagany pakiet GNU Grep (rozszerzenie), użycie ggrep

```bash
ggrep -oP '"[^"]+(?=":)' en-7.2.json5 > /tmp/keys_72.txt
```

### Krok 2: Wygeneruj plik z nowymi frazami

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

### Wynik (`pl-7.4.json5`)

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
