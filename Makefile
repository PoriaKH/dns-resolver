.DEFAULT_GOAL := run

venv:
	test -d venv || python3 -m venv ./venv
install:
	( \
       source ./venv/bin/activate; \
       pip install -r ../requirements.txt; \
    )

setup: venv install

run: setup
	pyinstaller main.py --onefile ;

clean:
	rm -r build
	rm -r dist
	rm -r venv
	rm -rf __pycache__
	rm -r main.spec

.PHONY:
	run clean