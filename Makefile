.PHONY: run build

build:
	docker build -t mimimitify:0.0.1 .

run:
	docker run -it --rm --name mimimitify-docker mimimitify:0.0.1