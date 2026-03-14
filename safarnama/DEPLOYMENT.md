# Safarnama Deployment On PythonAnywhere

This project is now configured to auto-load a local `.env` file from the project root, which makes PythonAnywhere deployment much easier.

## 1. Before you upload

Create a `.env` file in the project root based on `.env.example`.

Example:

```env
DJANGO_SECRET_KEY=replace-this-with-a-strong-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
TIME_ZONE=Asia/Kolkata
DB_ENGINE=sqlite
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-email@gmail.com
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
```

For a simple first deployment on PythonAnywhere, keep:

```env
DB_ENGINE=sqlite
```

## 2. Push the latest code

From your local machine:

```bash
git add safarnama/settings.py .env.example DEPLOYMENT.md requirements.txt .gitignore
git commit -m "Prepare project for PythonAnywhere deployment"
git push
```

## 3. Clone on PythonAnywhere

Open a Bash console on PythonAnywhere and run:

```bash
git clone https://github.com/Yashhub9/Django-SafarNama-Project.git
cd Django-SafarNama-Project/safarnama
python3.10 -m venv ~/.virtualenvs/safarnama-venv
source ~/.virtualenvs/safarnama-venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

If PythonAnywhere gives you a different Python version, use that version instead.

## 4. Create the `.env` file on PythonAnywhere

Inside `/home/yourusername/Django-SafarNama-Project/safarnama`, create:

```bash
nano .env
```

Paste your production values there and save the file.

## 5. Configure the web app

In the PythonAnywhere `Web` tab:

- Source code: `/home/yourusername/Django-SafarNama-Project/safarnama`
- Working directory: `/home/yourusername/Django-SafarNama-Project/safarnama`
- Virtualenv: `/home/yourusername/.virtualenvs/safarnama-venv`

## 6. Update the WSGI file

Open the WSGI configuration file from the `Web` tab and replace it with:

```python
import os
import sys

path = "/home/yourusername/Django-SafarNama-Project/safarnama"
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "safarnama.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 7. Run migrations and collect static

Back in the Bash console:

```bash
cd ~/Django-SafarNama-Project/safarnama
source ~/.virtualenvs/safarnama-venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## 8. Add static and media mappings

In the PythonAnywhere `Web` tab, add:

- URL: `/static/`
  Directory: `/home/yourusername/Django-SafarNama-Project/safarnama/staticfiles`

- URL: `/media/`
  Directory: `/home/yourusername/Django-SafarNama-Project/safarnama/media`

## 9. Reload the app

Click `Reload` in the `Web` tab.

## 10. If something breaks

Check these first:

- Error log in the PythonAnywhere `Web` tab
- Server log in the PythonAnywhere `Web` tab
- Your `.env` values
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`

## Notes

- Static files are served from `staticfiles` after `collectstatic`.
- Media uploads are stored in the project `media` folder.
- Since old secrets were already committed earlier, rotate your Gmail app password, Razorpay secret, and Django secret key.
