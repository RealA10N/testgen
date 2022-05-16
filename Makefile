PY ?= python3
.PHONY: build upload

build:
	rm -rf dist build
	git stash --include-untracked
	$(PY) setup.py sdist bdist_wheel
	git stash pop

upload: build
	$(PY) -m twine upload dist/*
