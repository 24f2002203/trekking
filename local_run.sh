#!/bin/sh
echo "==================================="
echo "Welcome to the local run"
echo "running the application for you"
echo "==================================="  

if [ -d '.venv' ]; then
    echo "Activating virtual environment..."
    . .venv/bin/activate
else
    echo "Virtual environment not found. Please run local_setup.sh first."
    exit 1
fi
export ENV=development
export FLASK_APP="app:create_app"


if [ -d 'migrations' ]; then
    echo "Running database migrations..."
    flask db stamp head
    flask db migrate -m "auto migration"
    flask db upgrade

else
    echo "Migrations directory not found. Please run local_setup.sh first."
    exit 1
fi

echo "Running the application..."
python app.py