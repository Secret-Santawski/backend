# Secret Santa
## Description
The "Secret Santa" project is a simple Flask-based web application that organizes Secret Santa events. It randomly assigns gift givers to recipients and sends personalized emails with details about the gift category and budget.

## Features
- Random assignment of Secret Santa pairs.
- Email notifications with personalized gift details.
- Integration with customizable email templates.

# Installation
To install and run the project, follow these steps:

## Prerequisites
- Python 3.x
- Flask
- An SMTP server (e.g., Gmail)

## Instructions
Clone the Repository:

```
git clone https://github.com/Secret-Santawski/backend.git
cd secret-santa
```

## Create a virtual enviroment
```
python3 -m venv .venv
source .venv/bin/activate
```

## Install Dependencies:

```
pip install -r requirements.txt
```

## Download the Firebase Configuration File
Go to your Firebase console. 
Select the desired project. 
Navigate to "Project settings" > "Service accounts" > "Firebase Admin SDK". 
Click on "Generate new private key file" and save the json file.

## Set Environment Variables:

- **SENDER_EMAIL**: The email address used to send out notifications.
- **SENDER_PASSWORD**: The password for the email account.
- **FIREBASE_SECRET_PATH**: The path for the json secrets downloaded from Firebase.

## Run the Application:

```
python src/app.py
```

## Usage
### To use the application, start the Server:

```
python src/app.py
```

### Send Secret Santa Emails:

Make a POST request to the **/SecretSanta/** endpoint with a JSON payload containing participant details.
