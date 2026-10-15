.PHONY: install test verify run docker-run docker-test clean
install:
	python3 -m pip install -r requirements.txt
test:
	python3 -m unittest -v
verify:
	python3 -m gargalo_lab verify --out output
run:
	python3 -m gargalo_lab all --out output
docker-run:
	docker compose up --build lab
docker-test:
	docker compose run --rm --build tests
clean:
	rm -rf output __pycache__ */__pycache__
