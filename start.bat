@echo off
echo ===================================================
echo             Starting OmniFix Demo System
echo ===================================================

echo.
echo [1/3] Starting Python Backend on Port 5000...
start "OmniFix Backend" cmd /k "python app.py"

echo.
echo [2/3] Starting Employee App (React) on Port 3000...
start "Employee Portal" cmd /k "cd employee_web && npm run dev"

echo.
echo [3/3] Starting Control Panel (React) on Port 3001...
start "OmniFix Control Panel" cmd /k "cd control_web && npm run dev"

echo.
echo ===================================================
echo System is booting up! Please wait a few seconds...
echo.
echo 👉 Employee Portal: http://localhost:3000
echo 👉 Control Panel:   http://localhost:3001
echo ===================================================
pause
