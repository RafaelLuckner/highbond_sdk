@echo off
REM Script para regenerar a documentação do HighBond SDK

echo.
echo ========================================
echo HighBond SDK - Regenerador de Docs
echo ========================================
echo.

REM Verificar se estamos na pasta docs
if not exist "conf.py" (
    echo Erro: Execute este script dentro da pasta 'docs'
    pause
    exit /b 1
)

echo Regenerando documentação...
python -m sphinx -b html . _build/html -q

if %errorlevel% equ 0 (
    echo.
    echo ✓ Documentação regenerada com sucesso!
    echo.
    echo Para visualizar: _build\html\index.html
    echo.
) else (
    echo.
    echo ✗ Erro ao regenerar documentação
    pause
    exit /b 1
)

pause
