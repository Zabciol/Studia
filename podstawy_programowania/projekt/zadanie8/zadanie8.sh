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