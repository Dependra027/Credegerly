# Deployment Guide for Credgerly

This guide covers deploying Credgerly to various cloud platforms.

## Prerequisites

1. **Generate a Django Secret Key**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Save this key securely - you'll need it for deployment.

2. **Get API Keys (Optional)**
   - **OpenAI API Key**: https://platform.openai.com/api-keys (for AI tips feature)
   - **NewsAPI Key**: https://newsapi.org/register (for financial news feature)

## Environment Variables

Set these environment variables in your deployment platform:

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key | ✅ Yes | Generated key |
| `DEBUG` | Debug mode | ✅ Yes | `False` for production |
| `ALLOWED_HOSTS` | Allowed hostnames | ✅ Yes | `yourdomain.com,www.yourdomain.com` |
| `DATABASE_URL` | Database connection string | ✅ Yes | Auto-set by platform |
| `OPENAI_API_KEY` | OpenAI API key | ❌ Optional | For AI tips |
| `NEWS_API_KEY` | NewsAPI key | ❌ Optional | For financial news |

---

## Option 1: Deploy to Render

[Render](https://render.com) offers free hosting with PostgreSQL.

### Steps:

1. **Create a Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create a PostgreSQL Database**
   - Click "New +" → "PostgreSQL"
   - Name: `credgerly-db`
   - Plan: Free
   - Click "Create Database"
   - Copy the "Internal Database URL"

3. **Create a Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - **Name**: `credgerly`
     - **Environment**: `Python 3`
     - **Build Command**: 
       ```bash
       pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
       ```
     - **Start Command**: 
       ```bash
       gunicorn finance_project.wsgi
       ```

4. **Set Environment Variables**
   - Go to your service → "Environment"
   - Add:
     - `SECRET_KEY`: Your generated secret key
     - `DEBUG`: `False`
     - `ALLOWED_HOSTS`: `your-app-name.onrender.com`
     - `DATABASE_URL`: (Auto-set if using Render PostgreSQL)
     - `OPENAI_API_KEY`: (Optional)
     - `NEWS_API_KEY`: (Optional)

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Your app will be live at `https://your-app-name.onrender.com`

### Using render.yaml (Alternative)

If you have `render.yaml` in your repo:
1. Click "New +" → "Blueprint"
2. Connect your repository
3. Render will automatically detect and use `render.yaml`

---

## Option 2: Deploy to Railway

[Railway](https://railway.app) offers simple deployment with automatic PostgreSQL.

### Steps:

1. **Create a Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create a New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add PostgreSQL Database**
   - Click "+ New" → "Database" → "PostgreSQL"
   - Railway automatically sets `DATABASE_URL`

4. **Configure Environment Variables**
   - Go to your service → "Variables"
   - Add:
     - `SECRET_KEY`: Your generated secret key
     - `DEBUG`: `False`
     - `ALLOWED_HOSTS`: `*.railway.app` (or your custom domain)
     - `OPENAI_API_KEY`: (Optional)
     - `NEWS_API_KEY`: (Optional)

5. **Deploy**
   - Railway auto-detects Python projects
   - It will run migrations automatically
   - Your app will be live at `https://your-app-name.railway.app`

### Custom Domain (Optional)

1. Go to your service → "Settings" → "Domains"
2. Add your custom domain
3. Update `ALLOWED_HOSTS` to include your domain

---

## Option 3: Deploy to Heroku

[Heroku](https://www.heroku.com) is a popular platform for Django apps.

### Steps:

1. **Install Heroku CLI**
   - Download from https://devcenter.heroku.com/articles/heroku-cli

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create a Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Add PostgreSQL Addon**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```
   (This automatically sets `DATABASE_URL`)

5. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
   heroku config:set OPENAI_API_KEY="your-key"  # Optional
   heroku config:set NEWS_API_KEY="your-key"     # Optional
   ```

6. **Deploy**
   ```bash
   git push heroku main
   ```

7. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py create_default_categories
   ```

8. **Create Superuser (Optional)**
   ```bash
   heroku run python manage.py createsuperuser
   ```

9. **Open Your App**
   ```bash
   heroku open
   ```

---

## Option 4: Deploy to PythonAnywhere

[PythonAnywhere](https://www.pythonanywhere.com) offers free hosting for Python web apps.

### Steps:

1. **Create a PythonAnywhere Account**
   - Go to https://www.pythonanywhere.com
   - Sign up for free account

2. **Upload Your Code**
   - Use the "Files" tab to upload your project
   - Or use Git: `git clone https://github.com/yourusername/your-repo.git`

3. **Set Up Virtual Environment**
   - Open a Bash console
   ```bash
   cd ~/your-project-name
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Set Up Database**
   - Go to "Databases" tab
   - Create a MySQL database (free tier)
   - Update `settings.py` to use MySQL:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'yourusername$credgerly',
           'USER': 'yourusername',
           'PASSWORD': 'your-db-password',
           'HOST': 'yourusername.mysql.pythonanywhere.com',
       }
   }
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py create_default_categories
   ```

6. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration" → Python 3.10
   - Edit WSGI file:
   ```python
   import os
   import sys
   
   path = '/home/yourusername/your-project-name'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   os.environ['DJANGO_SETTINGS_MODULE'] = 'finance_project.settings'
   
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

7. **Set Environment Variables**
   - In WSGI file or use `.env` file:
   ```python
   import os
   os.environ['SECRET_KEY'] = 'your-secret-key'
   os.environ['DEBUG'] = 'False'
   os.environ['ALLOWED_HOSTS'] = 'yourusername.pythonanywhere.com'
   ```

8. **Reload Web App**
   - Click "Reload" button in Web tab

---

## Post-Deployment Steps

After deploying to any platform:

1. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

2. **Create Default Categories**
   ```bash
   python manage.py create_default_categories
   ```

3. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

4. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **Test Your Deployment**
   - Visit your app URL
   - Create a test account
   - Test key features:
     - Sign up / Login
     - Add expenses
     - View dashboard
     - Check reports

---

## Troubleshooting

### Static Files Not Loading

- Ensure `collectstatic` runs during build
- Check `STATIC_ROOT` and `STATIC_URL` in settings
- Verify WhiteNoise is installed and configured

### Database Connection Errors

- Verify `DATABASE_URL` is set correctly
- Check database credentials
- Ensure database is running

### 500 Internal Server Error

- Check logs in your platform's dashboard
- Verify all environment variables are set
- Ensure `DEBUG=False` in production
- Check `ALLOWED_HOSTS` includes your domain

### Migrations Not Running

- Manually run: `python manage.py migrate`
- Check database permissions
- Verify database connection

### API Features Not Working

- Verify API keys are set in environment variables
- Check API key validity
- Review API usage limits

---

## Security Checklist

- ✅ `DEBUG=False` in production
- ✅ Strong `SECRET_KEY` set
- ✅ `ALLOWED_HOSTS` configured
- ✅ HTTPS enabled (most platforms do this automatically)
- ✅ Database credentials secured
- ✅ API keys stored as environment variables
- ✅ CSRF protection enabled (Django default)
- ✅ SQL injection protection (Django ORM)

---

## Monitoring & Maintenance

1. **Check Logs Regularly**
   - Monitor error logs in your platform dashboard
   - Set up error tracking (e.g., Sentry)

2. **Backup Database**
   - Most platforms offer automatic backups
   - Export data regularly: `python manage.py dumpdata > backup.json`

3. **Update Dependencies**
   - Regularly update `requirements.txt`
   - Test updates in development first

4. **Monitor Performance**
   - Use platform analytics
   - Monitor response times
   - Check database query performance

---

## Need Help?

- Check platform-specific documentation
- Review Django deployment checklist: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
- Check project README.md for local setup
- Review error logs in your platform dashboard

---

**Good luck with your deployment! 🚀**

