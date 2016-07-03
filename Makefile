all: nosetests flake
doc: html
include docs/Makefile

go-dev:
	ln -sf dev.cfg buildout.cfg

env:go-dev
	python bootstrap-buildout.py
	bin/buildout

test:
	@echo "==== Running nosetests ===="
	@bin/test

flake:
	@echo "==== Running Flake8 ===="
	@bin/flake8 detectoid/*.py
