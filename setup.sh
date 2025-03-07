#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Creating virtual environment..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env already exists
if [ -f .env ]; then
    echo ".env file already exists."
    read -p "Do you want to overwrite it? (y/n): " OVERWRITE

    if [[ "$OVERWRITE" =~ ^[Nn]$ ]]; then
        echo "Keeping the existing .env file."
        goto_migrate=true
    fi
fi

# Only prompt for secret key if creating a new .env file
if [ -z "$goto_migrate" ]; then
    read -p "Enter your Django Secret Key: " DJANGO_SECRET_KEY

    echo "Creating .env file..."
    cat <<EOL > .env
DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
DJANGO_DEBUG=True
EOL
fi

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput
python manage.py import_quiz
python manage.py import_user
python manage.py load_default_assets


# Start the server
echo "Starting the server..."
python manage.py runserver
