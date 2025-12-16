# ===============================
# AMP-GSTI Unified Intelligence
# Minimal Makefile
# ===============================

.PHONY: help install run dev test lint format clean

PYTHON ?= python3
APP_MODULE ?= app.main:app
HOST ?= 0.0.0.0
PORT ?= 8000

help:
	@echo "Available targets:"
	@echo "  install   Install runtime dependencies"
	@echo "  dev       Run development server with reload"
	@echo "  run       Run production server"
	@echo "  test      Run test suite"
	@echo "  lint      Run static analysis (ruff)"
	@echo "  format    Format code (black)"
	@echo "  clean     Remove cache and build artifacts"

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install .

dev:
	uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT) --reload

run:
	uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT)

test:
	pytest

lint:
	ruff .

format:
	black .

clean:
	rm -rf __pycache__ .pytest_cache build dist *.egg-info
