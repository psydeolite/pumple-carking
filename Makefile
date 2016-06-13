example: try.mdl lex.py main.py matrix.py mdl.py script.py yacc.py
	python main.py try.mdl

clean:
	rm *pyc *out parsetab.py

clear:
	rm *pyc *out parsetab.py *ppm
