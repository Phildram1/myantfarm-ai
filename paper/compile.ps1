# Compile LaTeX paper to PDF (PowerShell)

Write-Host "================================"
Write-Host "Compiling LaTeX Paper"
Write-Host "================================"
Write-Host ""

Set-Location paper

# First pass
Write-Host "Running pdflatex (1st pass)..."
pdflatex -interaction=nonstopmode main.tex | Out-Null

# BibTeX
Write-Host "Running bibtex..."
bibtex main 2>&1 | Out-Null

# Second pass
Write-Host "Running pdflatex (2nd pass)..."
pdflatex -interaction=nonstopmode main.tex | Out-Null

# Third pass
Write-Host "Running pdflatex (3rd pass)..."
pdflatex -interaction=nonstopmode main.tex | Out-Null

Write-Host ""
Write-Host "✓ Compilation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Output: paper/main.pdf"

# Open PDF (Windows)
Start-Process main.pdf