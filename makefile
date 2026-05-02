.PHONY: install run debug clean lint

install:
	pip install -r requirements.txt

run:
	python3 fly_in.py

debug:
	python3 -m pdb fly_in.py

clean:
	rm -rf __pycache__
	rm -rf mapbuilder/__pycache__
	rm -rf algorithm/__pycache__
	rm -rf .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs