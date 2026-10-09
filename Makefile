.PHONY: install test demo bench docker clean

install:
	pip install -e ".[dev]"

test:
	pytest

demo:
	python -m demo_agent.run

bench:
	python -m benchmark.runner --all

docker:
	docker-compose up --build

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	rm -rf build dist *.egg-info
