ifeq ($(OS), Windows_NT)
	PYTHON = python
else
	PYTHON = python3
endif

build:
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install --record install.txt

quicktest:
	$(PYTHON) -m unittest -vf

coverage:
	coverage run --branch -m test
	coverage report
	coverage html

test-release:
	$(PYTHON) setup.py register -r https://testpypi.python.org/pypi
	$(PYTHON) setup.py sdist upload -r https://testpypi.python.org/pypi

release:
	$(PYTHON) setup.py register
	$(PYTHON) setup.py sdist upload

clean:
	rm -rf build dist MANIFEST install.txt
	rm -rf .coverage htmlcov
	find . -name "__pycache__" -exec rm -r {} +
