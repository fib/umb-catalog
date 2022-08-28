.DEFAULT_GOAL := _help
.SHELL := /bin/bash

install: ## install dependencies
	python -m pip install flake8 pytest
	if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

lint: ## just a lint
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --max-complexity=10 --max-line-length=127 --statistics

_help: ## show this help.
	grep -E '^[a-zA-Z_\-\/\.]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# vim: tabstop=2 shiftwidth=2 noexpandtab
