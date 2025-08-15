VENV = venv
REQS = requirements.txt

venv:
	python -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip

install: venv
	$(VENV)/bin/pip install -r $(REQS)

run:
	$(VENV)/bin/python bot.py
