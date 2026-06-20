# Zadanie 5 – Z CSV do SQL i z powrotem

## Opis

Dwie konwersje formatów danych:

1. **CSV → SQL**: plik `steps-2sql.csv` (separator `;`) → instrukcje `INSERT INTO`
2. **SQL → CSV**: plik `steps-2csv.sql` (instrukcje INSERT) → plik CSV z konwersją czasu z milisekund na sekundy

## Pliki

| Plik             | Opis                                         |
| ---------------- | -------------------------------------------- |
| `steps-2sql.csv` | Dane wejściowe CSV (czas w sekundach)        |
| `steps-2sql.sql` | Wynik konwersji CSV → SQL                    |
| `steps-2csv.sql` | Dane wejściowe SQL (czas w milisekundach)    |
| `steps-2csv.csv` | Wynik konwersji SQL → CSV (czas w sekundach) |

---

## Część 1: CSV → SQL

### Dane wejściowe (`steps-2sql.csv`)

```
time;intensity;steps
1562001120;19;0
1562001180;23;0
...
```

### Polecenie

```bash
tr -d '\r' < steps-2sql.csv | \
awk -F';' 'NR>1 {printf "INSERT INTO stepsData (time, intensity, steps) VALUES (%s, %s, %s);\n", $1,  $2, $3}' > steps-2sql.sql
```

`tr -d '\r' < steps-2sql.csv` czyta dane i usuwa końce linii co pozawala zachować nawias zamykający w tej samej linii
`NR>1` pomija wiersz nagłówkowy. `-F';'` ustawia separator pola na średnik.

### Wynik (`steps-2sql.sql`)

```sql
INSERT INTO stepsData (time, intensity, steps) VALUES (1562001120, 19, 0);
INSERT INTO stepsData (time, intensity, steps) VALUES (1562001180, 23, 0);
...
```

---

## Część 2: SQL → CSV

### Dane wejściowe (`steps-2csv.sql`)

```sql
INSERT INTO stepsData (dateTime, steps, synced) VALUES (1562004600000, 41, 0);
INSERT INTO stepsData (dateTime, steps, synced) VALUES (1562005200000, 65, 0);
...
```

Uwaga: znacznik czasu jest w **milisekundach** – wartości `dateTime` kończą się na `000`.

### Polecenie

```bash
echo "dateTime;steps;synced" > steps-2csv.csv
sed 's/INSERT INTO stepsData (dateTime, steps, synced) VALUES (\(.*\)000, \(.*\), \(.*\));/\1;\2;\3/' \
  steps-2csv.sql >> steps-2csv.csv
```

Wyrażenie regularne `sed` przechwytuje trzy grupy i usuwa trzy ostatnie zera z `dateTime`,
konwertując milisekundy na sekundy.

### Wynik (`steps-2csv.csv`)

```
dateTime;steps;synced
1562004600;41;0
1562005200;65;0
...
```
