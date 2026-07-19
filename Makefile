PYTHON := python3
APP := app.py

.PHONY: install run dev format clean

install:
	pip install -r requirements.txt

run:
	streamlit run $(APP)

dev:
	STREAMLIT_SERVER_RUN_ON_SAVE=true streamlit run $(APP)

format:
	black .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete