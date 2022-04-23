lint:
	@echo "linting setup.py:"
	autopep8 --in-place setup.py
	pylint setup.py

	@echo "linting pyrtkgps:"
	autopep8 --in-place --recursive ./pyrtkgps
	find ./pyrtkgps -type f -name "*.py" | xargs pylint

.PHONY: clean
clean:
	rm -rf dist pyrtkgps.egg-info
	find . -type d -name "pyrtkgps.egg-info" | xargs rm -rf
	find . -type d -name "__pycache__" | xargs rm -rf
