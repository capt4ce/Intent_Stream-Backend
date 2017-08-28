init:
    pip install -r requirements.txt

build:
    py.test tests

start: init build

.PHONY: start
