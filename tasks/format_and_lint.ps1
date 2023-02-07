Write-Output "Activating venv..."
./.venv/Scripts/Activate.ps1
Write-Output "Running isort formatter..."
python -m isort "./cme"
Write-Output "Running flake8 linter..."
python -m flake8 "./cme"