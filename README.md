# ECM2434-Sustainability

## Introduction
![Ecoworld](https://ecoworld.dev/static/resources/Logo.webp)
### Plant A Greener Future

The prototype of our web app brings sustainability to life through an engaging, interactive experience that rewards eco-friendly actions with a gamified progression system. Players can earn points by participating in sustainable activities, completing quizzes, and interacting with real-world sustainability initiatives.

## Requirements
- Python 3.12

## Installation
Clone the repository using the following command:
```bash
git clone https://github.com/ECM2434-The-Hackstreet-Boys/ECM2434-Sustainability.git
```
Use CD to access the repository
```bash
cd ECM2434-Sustainability
```


### Automatic Setup
#### Windows
Run the following command to automatically set up and run the application:
```Console
./setup.bat
```

#### MacOS/Linux
```Console
./setup.sh
```


### Manual Setup

Install the required packages using the following command:
```bash
python pip install -r requirements.txt
```



## Local Setup
### .env Setup
Create a .env file in the root directory of the project and add the following variables:
```dotenv
DJANGO_SECRET_KEY='Add a secret key here'
DJANGO_DEBUG=True
```
### Django Setup
Run the following command to create the database:
```bash
python manage.py migrate
```
Run the following command to collect the staticfiles:
```bash
python manage.py collectstatic
```
Run the following command to start the server:
```bash
python manage.py runserver
```
After this you should be able to access the server at http://127.0.0.1:8000/


## Testing
Run the following command to run the tests:
```bash 
python manage.py test
```