#!/bin/bash
# Compile LaTeX paper to PDF

set -e

echo "================================"
echo "Compiling LaTeX Paper"
echo "================================"
echo ""

cd paper

# First pass
echo "Running pdflatex (1st pass)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

# BibTeX
echo "Running bibtex..."
bibtex main > /dev/null 2>&1 || true

# Second pass
echo "Running pdflatex (2nd pass)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

# Third pass
echo "Running pdflatex (3rd pass)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

echo ""
echo "Compilation complete!"
echo ""
echo "Output: paper/main.pdf"

# Open PDF (macOS)
if [[ "" == "darwin"* ]]; then
    open main.pdf
fi

# Open PDF (Linux)
if [[ "" == "linux-gnu"* ]]; then
    xdg-open main.pdf
fi