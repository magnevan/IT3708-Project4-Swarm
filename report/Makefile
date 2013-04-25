LATEX     = pdflatex
LATEXARGS = -halt-on-error
BIBTEX    = bibtex

TEXFILE = report.tex 
REFFILE = refs.bib
AUXFILE = report.aux
TARGET  = report.pdf

$(TARGET): $(TEXFILE) $(REFFILE)
	$(LATEX) $(LATEXARGS) $(TEXFILE)
	$(BIBTEX) $(AUXFILE)
	$(LATEX) $(LATEXARGS) $(TEXFILE)
	$(LATEX) $(LATEXARGS) $(TEXFILE)

.PHONY: clean
clean:
	$(RM) *.aux *.pdf *.blg *.bbl *.log *.out

