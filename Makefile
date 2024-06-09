.PHONY: install lint black mypy flake8 pylint pre-commit

install:
	pip install -r requirementsdev.txt
	pre-commit install

black:
	black *.py 

mypy:
	mypy *.py

flake8:
	pflake8 *.py

pylint:
	pylint **/*.py

isort:
	isort *.py
pre-commit:
	pre-commit run --all-files

lint: black mypy flake8 pylint isort
