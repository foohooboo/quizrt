.git:
	git init

VENV = .venv
export VIRTUAL_ENV := $(abspath ${VENV})
export PATH := ${VIRTUAL_ENV}/bin:${PATH}

${VENV}:
	python3 -m venv $@

python-reqs: requirements | ${VENV}
	pip install --upgrade -r requirements/local.txt

setup: ${VENV} python-reqs | .git

.env:
	cp env.example .env

setup-local: setup | .env

CLEANUP = *.pyc

clean:
	rm -rf ${CLEANUP}

.PHONY: help python-reqs setup setup-local clean
