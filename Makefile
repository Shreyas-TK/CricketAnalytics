.PHONY: install test run smoke docker-build docker-run

PYTHON ?= python3
PORT ?= 8501

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest -q

run:
	$(PYTHON) -m streamlit run dashboard/app.py --server.headless false --server.port $(PORT) --server.address 0.0.0.0

smoke:
	$(PYTHON) test.py

docker-build:
	docker build -t cricket-analytics .

docker-run:
	docker run --rm -p 8501:8501 cricket-analytics
