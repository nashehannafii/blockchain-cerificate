# Makefile for common tasks

PY=python3
RUN=./run

.PHONY: help run add-degree mine display validate

help:
	@echo "Available targets: run, add-degree, mine, display, validate"
	@echo "Run the project with './run <command> --help' to see available subcommands."

run:
	@echo "Run demo: ./run               (no args runs demo)"
	@echo "CLI usage: ./run <command> --help  (e.g. ./run add-degree --help)"

add-degree:
	@echo "Example: make add-degree NIM=20210010 NAME='Wahid'"
	$(RUN) add-degree --nim "${NIM}" --name "${NAME}" --degree "${DEGREE}" --major "${MAJOR}" --gpa "${GPA}" --grad-date "${GRAD_DATE}"

mine:
	$(RUN) mine

display:
	$(RUN) display

validate:
	$(RUN) validate
