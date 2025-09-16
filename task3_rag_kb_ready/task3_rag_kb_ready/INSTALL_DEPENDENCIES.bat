@echo off
echo Installing RAG Knowledge Base Dependencies...
echo.
echo This will install the required Python packages.
echo Please wait while packages are downloaded and installed...
echo.
pip install scikit-learn fastapi uvicorn numpy
echo.
echo Installation complete!
echo You can now run the project using START_CLI.bat or START_WEB.bat
echo.
pause
