#!/bin/bash

unzip -o galeria.zip index.html

for plik in zdjecia/*.jpg; do
    nazwa="${plik##*/}"
    echo "<div class=\"responsive\"><div class=\"gallery\"><a target=\"_blank\" href=\"zdjecia/$nazwa\"><img src=\"zdjecia/$nazwa\"></a><div class=\"desc\">$nazwa</div></div></div>"
done > wpisy.txt

awk '/<!-- kolejne pliki galerii/{while((getline line < "wpisy.txt")>0) print line; next} 1' index.html > galeria.html

rm -f wpisy.txt index.html
