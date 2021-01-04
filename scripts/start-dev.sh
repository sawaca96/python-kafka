#!/bin/bash
poetry install --no-interaction --no-ansi;
uvicorn trading:app --host 0.0.0.0 --reload;
