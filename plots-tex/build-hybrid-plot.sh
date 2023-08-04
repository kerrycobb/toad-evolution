#!/bin/bash

set -e

tex_path=hybrid-main.tex
pdf_path="${tex_path%.*}.pdf"
cropped_pdf_path="$(dirname $pdf_path)/cropped-$(basename $pdf_path)"
latexmk -C "$tex_path"
latexmk -pdf "$tex_path"
pdfcrop "$pdf_path" "$cropped_pdf_path"
latexmk -C "$tex_path"
