#!/bin/sh 
echo "==================================="
echo "Welcome to the local setup" 
echo "setting up the environment for you"
echo "==================================="

if [ -d '.venv' ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
. .venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

export FLASK_ENV=development
export FLASK_APP="app:create_app"

if [ -d 'migrations' ]; then
    echo "Migrations directory already exists. Skipping initialization."
else
    echo "Initializing database migrations..."
    flask db init
    flask db migrate -m "initial migration"
    flask db upgrade
fi

python seed.py
