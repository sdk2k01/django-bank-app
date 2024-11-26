# django-bank-app
Bank Application using Django.

## Setting Up Locally
1. Create and activate a python 3.12 virtual environment in project's root directory.
```bash
# Using pyenv
% pyenv virtualenv 3.12 <venv_name>
% pyenv local <venv_name>

# Setting up pyright
% pyenv pyright

# Modify pyrightconfig.json and add:
# {
#     "pythonVersion": "3.12",
#   # other options
# }
```

2. Install dependencies.
```bash
(venv)% pip install -U pip uv pre-commit
(venv)% uv pip sync requirements/*.txt # For dev
```

3. Setting Up Migrations.
```bash
(venv)% python manage.py makemigrations bank
(venv)% python manage.py migrate
# Create SuperUser
(venv)% python manage.py createsuperuser
# Enter credentials
```

4. Running Server in Dev Mode.
```bash
(venv)% python manage.py runserver
# Open http://localhost:8000/admin in the address bar of your favorite browser and login using superuser credentials created in step 3.
```
