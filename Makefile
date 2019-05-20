install-deps:
	pip install -r requirements.txt

test:
	export PYTHONPATH=.; \
	python -m unittest tests/test_dbgetreader.py
	python -m unittest tests/test_dbget.py
