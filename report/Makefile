LATEX     = pdflatex
LATEXARGS = -halt-on-error

TEXFILE = report.tex 
TARGET = report.pdf

$(TARGET): $(TEXFILE) *.png
	$(LATEX) $(LATEXARGS) $(TEXFILE)
	$(LATEX) $(LATEXARGS) $(TEXFILE)
