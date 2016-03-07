all: nosetests flake8 html
test: nosetests flake8
include docs/Makefile

nosetests:
	@echo "==== Running nosetests ===="
	@bin/test

flake8:
	@echo "==== Running Flake8 ===="
	@bin/flake8 detectoid/*.py
