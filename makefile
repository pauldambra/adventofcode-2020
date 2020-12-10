
dependencies:
	PIPENV_VENV_IN_PROJECT=1 pipenv install

lint: dependencies
	pipenv run flake8

test: lint
	pipenv run nosetests --with-xunit