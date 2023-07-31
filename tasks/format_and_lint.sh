echo "Activating venv..."
source "./.venv/bin/activate"
echo "Running isort formatter..."
python -m isort "./cme"
echo "Running flake8 linter..."
python -m flake8 "./cme"
echo "Running mypy static type checker..."
python -m mypy cme tests --ignore-missing-imports --strict --warn-unused-ignores