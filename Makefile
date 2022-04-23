lint:
	@echo "linting pyrtkgps:"
	autopep8 --in-place --recursive ./pyrtkgps
	find ./pyrtkgps -type f -name "*.py" | xargs pylint
