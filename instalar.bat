@echo off
echo =========================================
echo ⚙️ Creando entorno virtual...
echo =========================================
python -m venv venv

echo =========================================
echo 📦 Activando entorno e instalando librerias...
echo =========================================
call venv\Scripts\activate
pip install -r requirements.txt

echo =========================================
echo ✅ ¡Instalacion completada con exito!
echo =========================================
pause