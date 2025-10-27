#!/bin/bash

echo "🚀 Setting up SpyNet Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp env.example .env
    echo "⚠️ Please edit .env file with your Supabase credentials"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Edit .env file with your Supabase credentials"
echo "3. Set up your Supabase database using setup_supabase.sql"
echo "4. Run the server: uvicorn app.main:app --reload"
echo ""
