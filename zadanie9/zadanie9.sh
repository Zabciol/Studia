#!/bin/bash

cd kopie/ || exit

for plik in *.zip; do
    if [ -f "$plik" ]; then
        IFS='-' read -r rok miesiac reszta <<< "$plik"
        mkdir -p "$rok/$miesiac"
        mv "$plik" "$rok/$miesiac/"
    fi
done
