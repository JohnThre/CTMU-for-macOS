.PHONY: install test test-cov clean build

install:
	pip install -e .

test:
	python -m pytest tests/ -v

test-cov:
	python -m pytest tests/ --cov=src/ctmu --cov-report=html --cov-report=term

clean:
	rm -rf build/ dist/ *.egg-info/ htmlcov/ .coverage
	find . -type d -name __pycache__ -delete

build:
	python setup.py sdist bdist_wheel