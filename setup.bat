@echo off
REM Phase III Todo AI Chatbot - Quick Setup Script (Windows)
REM This script helps you set up the development environment

echo 🚀 Setting up Phase III Todo AI Chatbot...

REM Check if required tools are installed
echo 📋 Checking prerequisites...

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ from https://python.org/
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!

REM Setup backend
echo 🔧 Setting up backend...
cd backend

REM Copy environment file
if not exist .env (
    copy .env.example .env
    echo 📝 Created backend\.env from template
    echo ⚠️  Please edit backend\.env with your actual values!
) else (
    echo 📝 backend\.env already exists
)

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

cd ..

REM Setup frontend
echo 🎨 Setting up frontend...
cd frontend

REM Copy environment file
if not exist .env.local (
    copy .env.local.example .env.local
    echo 📝 Created frontend\.env.local from template
    echo ⚠️  Please edit frontend\.env.local with your actual values!
) else (
    echo 📝 frontend\.env.local already exists
)

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
npm install

cd ..

echo.
echo 🎉 Setup complete!
echo.
echo 📋 Next steps:
echo 1. Edit backend\.env with your database URL and OpenAI API key
echo 2. Edit frontend\.env.local with matching BETTER_AUTH_SECRET
echo 3. Generate secrets with: openssl rand -hex 32 (or use online generator)
echo 4. Run database migrations: cd backend ^&^& python migrate.py
echo 5. Start backend: cd backend\src ^&^& python -m uvicorn app.main:app --reload
echo 6. Start frontend: cd frontend ^&^& npm run dev
echo.
echo 🔗 URLs:
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 📚 For more details, see README.md
pause