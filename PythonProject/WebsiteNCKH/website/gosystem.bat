@echo off
echo Starting the application...
echo Wait...
start "" powershell -NoExit -Command "cd D:\NCKH\deepface-master; .\venv\Scripts\activate; python system_GUI.py"

echo All done! 
timeout /t 5 /nobreak