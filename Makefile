init:
	pip install -r requirements.txt

test:
	nose2 -v tests -s .
