# Quick Deployment Guide

## 🚀 Fastest Way: Deploy to Render (Recommended for Beginners)

### 5-Minute Setup:

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

2. **Go to Render.com**
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your repository

3. **Configure:**
   - **Name**: `credgerly` (or any name)
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py create_default_categories
     ```
   - **Start Command**: 
     ```bash
     gunicorn finance_project.wsgi
     ```

4. **Add PostgreSQL:**
   - Click "New +" → "PostgreSQL"
   - Name it `credgerly-db`
   - Render will auto-set `DATABASE_URL`

5. **Set Environment Variables:**
   - Go to your service → "Environment"
   - Add these variables:
     ```
     SECRET_KEY = [Generate one: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"]
     DEBUG = False
     ALLOWED_HOSTS = your-app-name.onrender.com
     ```
   - Optional: Add `OPENAI_API_KEY` and `NEWS_API_KEY` if you have them

6. **Deploy!**
   - Click "Create Web Service"
   - Wait 2-3 minutes
   - Your app is live! 🎉

---

## 🚂 Alternative: Railway (Also Easy)

1. **Go to railway.app**
2. **Click "New Project" → "Deploy from GitHub"**
3. **Add PostgreSQL database** (automatic)
4. **Set environment variables** (same as above)
5. **Done!** Railway auto-detects everything

---

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

- [ ] Code is pushed to GitHub/GitLab
- [ ] `SECRET_KEY` is generated (don't use the default!)
- [ ] `DEBUG=False` for production
- [ ] `ALLOWED_HOSTS` includes your domain
- [ ] Database is set up (PostgreSQL recommended)
- [ ] Environment variables are configured
- [ ] Static files will be collected (`collectstatic` in build command)

---

## 🔑 Generate Secret Key

Run this command to generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and use it as your `SECRET_KEY` environment variable.

---

## ✅ After Deployment

1. **Run migrations** (if not in build command):
   ```bash
   python manage.py migrate
   ```

2. **Create default categories**:
   ```bash
   python manage.py create_default_categories
   ```

3. **Create superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

4. **Test your app:**
   - Visit your URL
   - Sign up for an account
   - Add an expense
   - Check the dashboard

---

## 🆘 Common Issues

**Static files not loading?**
- Make sure `collectstatic` runs in build command
- Check WhiteNoise is in `requirements.txt`

**Database errors?**
- Verify `DATABASE_URL` is set
- Check database is running
- Run migrations manually

**500 errors?**
- Check logs in platform dashboard
- Verify all environment variables
- Ensure `DEBUG=False`

---

## 📚 Full Documentation

See `DEPLOYMENT.md` for detailed instructions for all platforms.

---

**Need help?** Check the platform's documentation or review error logs in your dashboard.

