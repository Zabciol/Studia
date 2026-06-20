#!/bin/bash

mkdir -p tmp

unzip -o kopie-1.zip -d tmp/ && unzip -o kopie-2.zip -d tmp/

for zip in tmp/????-??-??.zip; do unzip -o "$zip" -d tmp/; done

for img in tmp/*.jpg tmp/*.png; do
    magick "$img" -density 96 -units PixelsPerInch -resize x720 "$img"
done

zip -j zdjecia.zip tmp/*.jpg

rm -rf tmp