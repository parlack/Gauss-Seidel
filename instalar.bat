@echo off
echo ================================================================
echo 🔢 INSTALADOR - Resolver Sistemas de Ecuaciones (Gauss-Seidel)
echo ================================================================
echo.

echo ✅ Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo    Por favor, instala Python 3.7+ desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

echo.
echo 📦 Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Error al instalar dependencias
    echo    Verifica tu conexión a internet y que pip esté actualizado
    pause
    exit /b 1
)

echo.
echo ✅ ¡Instalación completada exitosamente!
echo.
echo 🚀 Para ejecutar la aplicación, usa uno de estos comandos:
echo    • Doble clic en "ejecutar.bat"
echo    • O desde terminal: python main.py
echo.
pause

