# KHQR Integration Setup Script for Windows
# Run with: .\setup_khqr.ps1

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "KHQR Payment Integration Setup" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ Python is installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check Node.js installation
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js is installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js 16+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Setting up Backend..." -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

Set-Location backend

# Check if virtual environment exists
if (-not (Test-Path "env")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv env
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\env\Scripts\Activate.ps1

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install bakong-khqr requests pillow qrcode celery redis django-celery-beat

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  Please edit .env file with your KHQR credentials" -ForegroundColor Yellow
}

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Setting up Frontend..." -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

Set-Location ..\inventory-frontend

# Install Node dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install qr-code-styling --legacy-peer-deps

Set-Location ..

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Configure KHQR credentials:" -ForegroundColor Yellow
Write-Host "   Edit backend\.env with your Bakong API credentials"
Write-Host ""
Write-Host "2. Install and start Redis:" -ForegroundColor Yellow
Write-Host "   Option A: Use WSL (Windows Subsystem for Linux)"
Write-Host "     wsl sudo service redis-server start"
Write-Host ""
Write-Host "   Option B: Download Redis for Windows"
Write-Host "     https://github.com/microsoftarchive/redis/releases"
Write-Host ""
Write-Host "3. Start the services (open 4 separate PowerShell windows):" -ForegroundColor Yellow
Write-Host ""
Write-Host "   Window 1 - Django:" -ForegroundColor White
Write-Host "   PS> cd backend"
Write-Host "   PS> .\env\Scripts\Activate.ps1"
Write-Host "   PS> python manage.py runserver"
Write-Host ""
Write-Host "   Window 2 - Celery Worker:" -ForegroundColor White
Write-Host "   PS> cd backend"
Write-Host "   PS> .\env\Scripts\Activate.ps1"
Write-Host "   PS> celery -A core worker --loglevel=info --pool=solo"
Write-Host ""
Write-Host "   Window 3 - Celery Beat:" -ForegroundColor White
Write-Host "   PS> cd backend"
Write-Host "   PS> .\env\Scripts\Activate.ps1"
Write-Host "   PS> celery -A core beat --loglevel=info"
Write-Host ""
Write-Host "   Window 4 - Next.js Frontend:" -ForegroundColor White
Write-Host "   PS> cd inventory-frontend"
Write-Host "   PS> npm run dev"
Write-Host ""
Write-Host "4. Open http://localhost:3000 in your browser" -ForegroundColor Cyan
Write-Host ""
Write-Host "For detailed documentation, see KHQR_INTEGRATION_GUIDE.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "Note: On Windows, use '--pool=solo' flag for Celery worker" -ForegroundColor Yellow
Write-Host ""
