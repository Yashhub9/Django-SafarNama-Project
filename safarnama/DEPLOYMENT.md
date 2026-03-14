# Safarnama Deployment

## 1. Local prep

Create a local `.env` file based on `.env.example` and fill in your real values.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run a final local check:

```bash
python manage.py check
python manage.py migrate
python manage.py collectstatic
```

## 2. PythonAnywhere setup

1. Create a new web app on PythonAnywhere.
2. Choose `Manual configuration`.
3. Choose the same Python version you want for the app.

Open a Bash console on PythonAnywhere and run:

```bash
git clone https://github.com/Yashhub9/Django-SafarNama-Project.git
cd Django-SafarNama-Project
python -m venv ~/.virtualenvs/safarnama-venv
source ~/.virtualenvs/safarnama-venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root and add your production values.

For a simple first deployment, keep:

```env
DB_ENGINE=sqlite
```

## 3. Web tab configuration

In the PythonAnywhere `Web` tab:

- Source code: `/home/yourusername/Django-SafarNama-Project`
- Working directory: `/home/yourusername/Django-SafarNama-Project`
- Virtualenv: `/home/yourusername/.virtualenvs/safarnama-venv`

Edit the WSGI configuration file so it points to your project:

```python
import os
import sys

path = "/home/yourusername/Django-SafarNama-Project"
if path not in sys.path:
    sys.path.insert(0, path)

os.environ["DJANGO_SETTINGS_MODULE"] = "safarnama.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 4. Static and database

Run these commands in the Bash console:

```bash
cd ~/Django-SafarNama-Project
source ~/.virtualenvs/safarnama-venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

In the `Web` tab, add static mappings:

- URL: `/static/` -> Directory: `/home/yourusername/Django-SafarNama-Project/staticfiles`
- URL: `/media/` -> Directory: `/home/yourusername/Django-SafarNama-Project/media`

## 5. Final step

Reload the web app from the `Web` tab.

If something fails, check:

- The PythonAnywhere error log
- The server log
- That your `.env` file has the correct values
- That `ALLOWED_HOSTS` contains `yourusername.pythonanywhere.com`

