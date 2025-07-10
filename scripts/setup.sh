#!/usr/bin/env bash

./scripts/clean.sh \
    && pdm python install 3.13 \
    && pdm venv create \
    && pdm use --venv in-project \
    && rm -f .python-version \
    && pdm run clean \
    && pdm run build
