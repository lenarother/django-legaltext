.PHONY: tests coverage coverage-html
APP=legaltext/
OPTS=

help:
	@echo "tests - run tests"
	@echo "coverage - run tests with coverage enabled"
	@echo "coverage-html - run tests with coverage html export enabled"

tests:
	py.test ${OPTS} ${APP}


coverage:
	py.test ${OPTS} --cov=${APP} --cov-report=term-missing


coverage-html:
	py.test ${OPTS} --cov=${APP} --cov-report=term-missing --cov-report=html
