.PHONY: clean build install uninstall test run docker-build docker-run start

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

docker-build:
	docker build -f docker/Dockerfile -t sharq .

docker-run:
	docker run -p 8000:8000 sharq

start:
	docker-compose up start-dependencies
	docker-compose up --build --remove-orphans