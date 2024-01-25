# DjangoCoreApp
A Django app with a custom user model setup.  This uses an email address instead of a username to login.

## Instructions

1. Clone this repository into a folder named core within your Django folder.
```
	git clone https://github.com/majormunky/DjangoCoreApp.git core
```
2. Open your project settings.py file
3. Add this setting to the bottom of the file
```
	AUTH_USER_MODEL = "core.CoreUser"
```
4. Add core to the list of INSTALLED_APPS
5. Run:
```
	python manage.py makemigrations core
	python manage.py migrate
```
6. That should be it!

## What does this do?
Normally Django will set you up with a user model that uses a username.  I prefer to just use an email address instead, so this is an easy way for me to get that setup.

This app will define a custom user model that uses an email address as the username.