SHELL=/bin/bash
NAME=presentation

.PHONY: presentation, clean

presentation: ${NAME}.pdf

clean:
	-rm ${NAME}.pdf

${NAME}.pdf: ${NAME}.tex
	pdflatex --shell-escape ${NAME}.tex
	-rm ${NAME}.{aux,log,nav,out,snm,toc}

