GIT_BRANCH=$(shell git branch --show-current)

requirements:
	pip install -r requirements.txt

lint:
	@echo "linting setup.py:"
	autopep8 --in-place setup.py
	pylint setup.py

	@echo "linting pyrtkgps:"
	autopep8 --in-place --recursive ./pyrtkgps
	find ./pyrtkgps -type f -name "*.py" | xargs pylint

build:
	rm -rf dist/*
	pip install --upgrade build
	python -m build

stage:
	@if [[ "${GIT_BRANCH}" != "stage" ]]; then echo "Abort: invalid git branch"; exit 1; fi
	twine upload  --verbose --repository testpypi dist/* -u "__token__" -p "${TEST_PYPI_API_SECRET}"

deploy:
	@if [[ "${GIT_BRANCH}" != "deploy" ]]; then echo "Abort: invalid git branch"; exit 1; fi
	twine upload --verbose dist/* -u "__token__" -p "${PYPI_API_SECRET}"

.PHONY: clean
clean:
	rm -rf dist pyrtkgps.egg-info
	find . -type d -name "pyrtkgps.egg-info" | xargs rm -rf
	find . -type d -name "__pycache__" | xargs rm -rf
