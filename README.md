# ECM2434-Sustainability

## Introduction
![Ecoworld](https://ecoworld.dev/static/resources/Logo.webp)
### Plant A Greener Future

The prototype of our web app brings sustainability to life through an engaging, interactive experience that rewards eco-friendly actions with a gamified progression system. Players can earn points by participating in sustainable activities, completing quizzes, and interacting with real-world sustainability initiatives.


## Production Server
The production server is hosted at https://ecoworld.dev/ and is managed by the team. The server is running the latest version of the application and is available for public use.

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


## Automatic Setup
#### Windows
Run the following command to automatically set up and run the application:
```Console
./setup.bat
```

#### MacOS/Linux
Run the following command to make the setup file executable
```Console
chmod 755 setup.sh
```
Execute the setup file
```Console
./setup.sh
```

#### Secret Key Generation
When asked you can select any random combination of characters to generate a secret key for the Django application.

## Manual Setup

Install the required packages using the following command:
```bash
python pip install -r requirements.txt
```


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
Run the following command to import the quiz questions to the database
```bash
python manage.py import_quiz
```
Run the following command to add a default admin and user to the database
```bash
python manage.py import_user
```
Run the following command to start the server:
```bash
python manage.py runserver
```

### Accessing the server
After this you should be able to access the server at http://127.0.0.1:8000/
The default admin username is `admin` and the password is `admin`
The default user account is `user` and the password is `user`

### Accessing Admin Pages
Current admin pages have url:
```djangourlpath
127.0.0.1:8000/accounts/manage_roles/
```


## Testing
Run the following command to run the tests:
```bash 
python manage.py test
```
