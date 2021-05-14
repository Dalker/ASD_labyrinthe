#!/bin/bash
# extraire des "images" du pdf généré par odt
pdfcrop --margins "-3 -45 -3 -45" $1 diapos_coupees.pdf

for page in {1..48}; do
    pdfjam --outfile page${page}.png diapos_coupees.pdf $page;
    convert page${page}.pdf page${page}.png;
    rm page${page}.pdf;
done
