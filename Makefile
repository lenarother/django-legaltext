.PHONY: tests coverage coverage-html
APP=legaltext/
OPTS=

help:
	@echo "tests - run tests"
	@echo "coverage - run tests with coverage enabled"
	@echo "coverage-html - run tests with coverage html export enabled"
	@echo "devinstall - install all packages required for development"
	@echo "clean-build - Clean build related files"

tests:
	py.test ${OPTS} ${APP}

coverage:
	py.test ${OPTS} --cov=${APP} --cov-report=term-missing

coverage-html:
	py.test ${OPTS} --cov=${APP} --cov-report=term-missing --cov-report=html

devinstall:
	pip install -e .
	pip install -e .[tests]

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info src/*.egg-info
	@rm -fr htmlcov/