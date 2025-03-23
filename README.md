# ECM2434-Sustainability

## Introduction
![Ecoworld](https://ecoworld.dev/static/resources/Logo.webp)
### Plant A Greener Future
Our final prototype refines and expands our web application, delivering a polished and immersive experience that makes sustainability both engaging and rewarding. Players can now take part in a wider range of eco-friendly activities, complete interactive sustainability quizzes, and engage with real-world sustainability initiatives around campus. With an improved gamified progression system, players earn points for their actions and can use them to further customize their own isometric garden. As they continue making sustainable choices, their garden flourishes, reflecting their impact in a visually rewarding way.

## Production Server
Our production server is hosted on the internet via https://ecoworld.dev/ and is managed by the development team. The server is running the latest version of the application and is available for public use!

## Requirements (for running locally)
- Python 3.12
- [Automatically Installed Python Requirements](./requirements.txt)

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
Run the following command to import the default garden assets
```bash
python manage.py load_default_assets
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
Using the default admin account in the sidebar you will have access to the admin dashboard allowing you to update the roles of users to either gamekeepers or admins



## Testing
Run the following command to run the tests:
```bash 
python manage.py test
```
