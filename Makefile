########################################################################################################################
# Project installation
########################################################################################################################

install:
	pyenv virtualenv --force 3.11.6 local-efficient-data-platform
	pyenv local local-efficient-data-platform
	# Running poetry install inside a Make command requires a VIRTUAL_ENV variable
	VIRTUAL_ENV=$$(pyenv prefix) poetry install --no-root --sync

########################################################################################################################
# Quality checks
########################################################################################################################

test:
	poetry run pytest tests --cov src --cov-report term --cov-report=html --cov-report xml --junit-xml=tests-results.xml

format-check:
	poetry run ruff format --check src tests

format-fix:
	poetry run ruff format src tests

lint-check:
	poetry run ruff check src tests

lint-fix:
	poetry run ruff check src tests --fix

type-check:
	poetry run mypy src
