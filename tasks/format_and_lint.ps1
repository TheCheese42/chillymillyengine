Write-Output "Activating venv..."
./.venv/Scripts/Activate.ps1
Write-Output "Running isort formatter..."
python -m isort "./cme" "./tests"
Write-Output "Running flake8 linter..."
python -m flake8 "./cme" "./tests"
Write-Output "Running mypy static type checker..."
python -m mypy cme tests --ignore-missing-imports --strict --no-warn-unused-ignores