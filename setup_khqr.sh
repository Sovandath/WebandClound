#!/bin/bash
# KHQR Integration Setup Script

echo "========================================="
echo "KHQR Payment Integration Setup"
echo "========================================="
echo ""

# Check if Redis is installed
echo "Checking Redis installation..."
if ! command -v redis-cli &> /dev/null; then
    echo "⚠️  Redis is not installed."
    echo "Please install Redis:"
    echo "  - Windows: Download from https://redis.io/download or use WSL"
    echo "  - Ubuntu/Debian: sudo apt-get install redis-server"
    echo "  - macOS: brew install redis"
    exit 1
else
    echo "✅ Redis is installed"
fi

# Check if Redis is running
echo "Checking if Redis is running..."
if redis-cli ping &> /dev/null; then
    echo "✅ Redis is running"
else
    echo "⚠️  Redis is not running. Starting Redis..."
    redis-server --daemonize yes
    sleep 2
    if redis-cli ping &> /dev/null; then
        echo "✅ Redis started successfully"
    else
        echo "❌ Failed to start Redis"
        exit 1
    fi
fi

echo ""
echo "========================================="
echo "Setting up Backend..."
echo "========================================="

cd backend || exit

# Check if virtual environment exists
if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    python -m venv env
fi

# Activate virtual environment
source env/bin/activate || source env/Scripts/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install bakong-khqr requests pillow qrcode celery redis django-celery-beat

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your KHQR credentials"
fi

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

echo ""
echo "========================================="
echo "Setting up Frontend..."
echo "========================================="

cd ../inventory-frontend

# Install Node dependencies
echo "Installing Node.js dependencies..."
npm install qr-code-styling --legacy-peer-deps

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Configure KHQR credentials:"
echo "   Edit backend/.env with your Bakong API credentials"
echo ""
echo "2. Start the services (open 4 separate terminals):"
echo ""
echo "   Terminal 1 - Django:"
echo "   $ cd backend"
echo "   $ python manage.py runserver"
echo ""
echo "   Terminal 2 - Celery Worker:"
echo "   $ cd backend"
echo "   $ celery -A core worker --loglevel=info"
echo ""
echo "   Terminal 3 - Celery Beat:"
echo "   $ cd backend"
echo "   $ celery -A core beat --loglevel=info"
echo ""
echo "   Terminal 4 - Next.js Frontend:"
echo "   $ cd inventory-frontend"
echo "   $ npm run dev"
echo ""
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "For detailed documentation, see KHQR_INTEGRATION_GUIDE.md"
echo ""
