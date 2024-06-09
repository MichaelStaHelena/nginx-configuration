.PHONY: install lint black mypy flake8 pylint

install:
	pip install -r requirementsdev.txt

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

lint: black mypy flake8 pylint isort
