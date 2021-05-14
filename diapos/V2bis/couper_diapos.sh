#!/bin/bash
# extraire des "images" du pdf généré par odt
pdfcrop --margins "-3 -45 -3 -45" ProjetDiaposExplicLabV2Base.pdf diapos_coupees.pdf

for page in {1..6}; do
    pdfjam --outfile page${page}.pdf diapos_coupees.pdf $page;
    convert page${page}.pdf page${page}.png;
    rm page${page}.pdf;
done
