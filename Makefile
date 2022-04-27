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

check-version: pypi-info
	$(eval PUBLISHED_VERSION 	:= $(shell jq -r '.info.version' pypi-info.json))
	$(eval BUILD_VERSION 		:= $(shell python setup.py --version))
	$(eval IS_VALID_VERSION		:= $(shell python -c 'from packaging.version import Version; print(Version("${BUILD_VERSION}") > Version("${PUBLISHED_VERSION}"));'))
	@echo "version (old): ${PUBLISHED_VERSION}"
	@echo "version (new): ${BUILD_VERSION}"
	@echo "upgradable: ${IS_VALID_VERSION}"
	rm -rf pypi-info.json
	if [ "${IS_VALID_VERSION}" != "True" ]; then exit 1; fi

pypi-info:
	curl '${PYPI_URL_JSON}' -o  ./pypi-info.json

stage:
	@if [ "${GIT_BRANCH}" != "stage" ]; then echo "Abort: invalid git branch"; exit 1; fi
	twine upload  --verbose --repository testpypi dist/* -u "__token__" -p "${TEST_PYPI_API_SECRET}"

release:
	@if [ "${GIT_BRANCH}" != "release" ]; then echo "Abort: invalid git branch"; exit 1; fi
	twine upload --verbose dist/* -u "__token__" -p "${PYPI_API_SECRET}"

.PHONY: clean
clean:
	rm -rf dist pyrtkgps.egg-info
	find . -type d -name "pyrtkgps.egg-info" | xargs rm -rf
	find . -type d -name "__pycache__" | xargs rm -rf
