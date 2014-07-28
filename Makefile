.PHONY: clean build install uninstall test run

all: clean

clean:
	find . -name \*.pyc -delete
	find . -name \*.pyo -delete
	find . -name \*~ -delete
	rm -rf build dist SharQServer.egg-info

build:
	python setup.py sdist

install:
	pip install dist/SharQServer-*.tar.gz

uninstall:
	yes | pip uninstall sharqserver

test:
	python -m tests

run:
	sharq-server --config sharq.conf
