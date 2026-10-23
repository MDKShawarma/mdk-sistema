@echo off
cd /d "%~dp0"
:inicio
python puente_impresion.py
timeout /t 3 >nul
goto inicio