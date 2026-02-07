#!/bin/bash

# Phase III Todo AI Chatbot - Quick Setup Script
# This script helps you set up the development environment

echo "🚀 Setting up Phase III Todo AI Chatbot..."

# Check if required tools are installed
echo "📋 Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

# Check Python
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ from https://python.org/"
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Setup backend
echo "🔧 Setting up backend..."
cd backend

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created backend/.env from template"
    echo "⚠️  Please edit backend/.env with your actual values!"
else
    echo "📝 backend/.env already exists"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

cd ..

# Setup frontend
echo "🎨 Setting up frontend..."
cd frontend

# Copy environment file
if [ ! -f .env.local ]; then
    cp .env.local.example .env.local
    echo "📝 Created frontend/.env.local from template"
    echo "⚠️  Please edit frontend/.env.local with your actual values!"
else
    echo "📝 frontend/.env.local already exists"
fi

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit backend/.env with your database URL and OpenAI API key"
echo "2. Edit frontend/.env.local with matching BETTER_AUTH_SECRET"
echo "3. Generate secrets with: openssl rand -hex 32"
echo "4. Run database migrations: cd backend && python migrate.py"
echo "5. Start backend: cd backend/src && python -m uvicorn app.main:app --reload"
echo "6. Start frontend: cd frontend && npm run dev"
echo ""
echo "🔗 URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📚 For more details, see README.md"