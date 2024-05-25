echo "Activating venv..."
source "./.venv/bin/activate"
echo "Running isort formatter..."
python -m isort "./cme" "./tests"
echo "Running flake8 linter..."
python -m flake8 "./cme" "./tests"
echo "Running mypy static type checker..."
python -m mypy cme tests --ignore-missing-imports --strict