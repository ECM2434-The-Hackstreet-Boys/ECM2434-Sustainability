# ECM2434-Sustainability

## Introduction
![Ecoworld](https://ecoworld.dev/static/resources/Logo.webp)
### Plant A Greener Future

The first prototype of our web application brings sustainability to life through an engaging, interactive experience that rewards eco-friendly actions with a gamified progression system. Players are tasked with participating in eco-friendly activities, completing sustainability quizzes, and interacting with real-world sustainability initiatives around campus. Doing these activities allows players to earn points, which they can later spend to their very own, fully-customisable isometric garden, which grows and blossoms the more sustainable actions they make.


## Production Server
Our production server is hosted on the internet via https://ecoworld.dev/ and is managed by the development team. The server is running the latest version of the application and is available for public use!

## Requirements (for running locally)
- Python 3.12

## Local Installation
Please open a terminal or command prompt, and clone the repository by entering the following command:
```bash
git clone https://github.com/ECM2434-The-Hackstreet-Boys/ECM2434-Sustainability.git
```
Next, use CD to access the repository:
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
Run the following command to make the setup file executable on your device:
```Console
chmod 755 setup.sh
```
Execute the setup file:
```Console
./setup.sh
```

#### Secret Key Generation
After running the commands above, you will be prompted to enter a a secret key for the Django application. You can input any combination of characters you'd like, and then hit ENTER! 

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
Run the following command to import the locations for the map
```bash
python manage.py import_locations
```
Run the following command to import the bins for the map
```bash
python manage.py import_bins
```
Run the following command to add a default admin and user to the database
```bash
python manage.py import_user
```
Run the following command to start the server:
```bash
python manage.py runserver
```

### Accessing the Local Server
After completing the local setup (whether you chose to do it automatically or manually), you should be able to access the server at http://127.0.0.1:8000/
The default admin username is `admin` and the password is `admin`
The default user account is `user` and the password is `user`

### Accessing Admin Pages
If you wish to access the current admin web page, please enter the following url into your web browser:
```djangourlpath
127.0.0.1:8000/accounts/manage_roles/
```


## Testing
Run the following command to run the tests:
```bash 
python manage.py test
```
