# Django rest API implementation for passwordless login (Login with otp/passcode) with JWT authentication.

Django login system without password, Register with phone number and get an otp. Verify yourself by providing otp and receive JWT refresh token and access token. Use access token to update profile of the user.

Currently, OTP is not sent through SMS. Otp can be retrieved from database directly from table `authentication_otp` for that specific user.

## Setup

1. The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/theshohidul/django-passcode-login-jwt.git
$ cd django-passcode-login-jwt
```

2. This project requires MySQL as database. So prepare a MySQL database. 

3. Rename `.env.example` to `.env`. Open `.env` and edit values if necessary.

4. Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv env
$ source env/bin/activate
```

5. Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

6. Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py migrate
(env)$ python manage.py runserver 8000
```
# Parking31_NEW_backend
