@echo off
setlocal enabledelayedexpansion

echo Creating virtual environment...
python -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

:: Check if .env already exists
if exist .env (
    echo .env file already exists.
    set /p OVERWRITE="Do you want to overwrite it? (y/n): "

    if /I "!OVERWRITE!"=="n" (
        echo Keeping the existing .env file.
        goto MIGRATE
    )
)

:: Only prompt for secret key if creating a new .env file
set /p DJANGO_SECRET_KEY="Enter your Django Secret Key: "

echo Creating .env file...
(
    echo DJANGO_SECRET_KEY=!DJANGO_SECRET_KEY!
    echo DJANGO_DEBUG=True
) > .env

:MIGRATE
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

echo Collecting static files...
python manage.py collectstatic --noinput

echo Starting the server...
python manage.py runserver

pause
