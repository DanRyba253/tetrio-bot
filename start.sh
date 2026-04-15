#! /bin/bash

cd python-src
if [ ! -d .venv ]; then
    echo "Скачиваем зависимости, пожалуйста подождите..."
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-linux.txt
    deactivate
fi
source .venv/bin/activate
python main.py



