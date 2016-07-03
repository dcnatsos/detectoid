all: nosetests flake8
doc: html
include docs/Makefile

env:
	python bootstrap-buildout.py -c dev.cfg
	bin/buildout -c dev.cfg

test:
	@echo "==== Running nosetests ===="
	@bin/test

flake8:
	@echo "==== Running Flake8 ===="
	@bin/flake8 detectoid/*.py
