Write-Host "Starting 43v3rMES Bootstrap..."

# Install dependencies
Write-Host "Installing backend dependencies..."
pip install -r backend/requirements.txt

Write-Host "Installing frontend dependencies..."
Set-Location frontend
npm install
Set-Location ..

# Setup environment
if (-not (Test-Path .env)) {
    Write-Host "Initializing .env from .env.example..."
    Copy-Item .env.example .env
}

Write-Host "Bootstrap complete! You can now start the services."
