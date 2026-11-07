@echo off
setlocal
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
python src\run_robustness.py
if errorlevel 1 exit /b 1
python src\run_sensitivity_extensions.py
if errorlevel 1 exit /b 1
python src\paired_formula_bootstrap.py
if errorlevel 1 exit /b 1
python src\build_publication_assets.py
if errorlevel 1 exit /b 1
python src\build_manuscript.py
if errorlevel 1 exit /b 1
python -m pytest -q tests
endlocal
