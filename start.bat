@echo off
chcp 65001
cd python-src

if not exist .venv (
    echo Скачиваем зависимости, пожалуйста подождите...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements-windows.txt
    call .venv\Scripts\deactivate.bat
)

call .venv\Scripts\activate.bat
start pythonw main.py
