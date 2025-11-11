# Setting Up Environment Variables in Render

This guide will walk you through adding environment variables to your Render deployment.

## Step-by-Step Instructions

### Step 1: Access Your Render Dashboard
1. Go to [render.com](https://render.com)
2. Log in to your account
3. Click on your web service (the one you created for Credgerly)

### Step 2: Navigate to Environment Variables
1. In your service dashboard, look for the **"Environment"** tab in the left sidebar
2. Click on **"Environment"**
3. You'll see a section called **"Environment Variables"**

### Step 3: Add Each Environment Variable

Click the **"Add Environment Variable"** button and add each variable one by one:

#### 1. SECRET_KEY (Required)
- **Key**: `SECRET_KEY`
- **Value**: Generate one using this command:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- **Example**: `django-insecure-abc123xyz789...` (long random string)

#### 2. DEBUG (Required)
- **Key**: `DEBUG`
- **Value**: `False`
- **Important**: Must be `False` for production!

#### 3. ALLOWED_HOSTS (Required)
- **Key**: `ALLOWED_HOSTS`
- **Value**: Your Render app URL (replace `your-app-name` with your actual app name)
  ```
  your-app-name.onrender.com
  ```
- **Example**: If your app is named `credgerly`, use:
  ```
  credgerly.onrender.com
  ```
- **Note**: If you have a custom domain, add it like this:
  ```
  credgerly.onrender.com,yourdomain.com,www.yourdomain.com
  ```

#### 4. DATABASE_URL (Usually Auto-Set)
- **Key**: `DATABASE_URL`
- **Value**: Usually automatically set by Render when you add a PostgreSQL database
- **If not set**: Go to your PostgreSQL database service → "Connections" → Copy "Internal Database URL"
- **Format**: `postgresql://user:password@host:port/dbname`

#### 5. OPENAI_API_KEY (Optional - for AI Tips feature)
- **Key**: `OPENAI_API_KEY`
- **Value**: Your OpenAI API key from https://platform.openai.com/api-keys
- **Note**: This is optional. If not set, the app will use default tips instead of AI-generated ones.

#### 6. NEWS_API_KEY (Optional - for Financial News feature)
- **Key**: `NEWS_API_KEY`
- **Value**: Your NewsAPI key from https://newsapi.org/register
- **Note**: This is optional. If not set, the news feature won't fetch external articles.

### Step 4: Save Changes
1. After adding all variables, click **"Save Changes"** at the bottom
2. Render will automatically redeploy your application with the new environment variables

### Step 5: Verify Deployment
1. Wait for the deployment to complete (check the "Events" or "Logs" tab)
2. Once deployed, visit your app URL
3. Test that everything works correctly

---

## Visual Guide

```
Render Dashboard
├── Your Service (credgerly)
│   ├── Overview
│   ├── Environment  ← Click here!
│   │   └── Environment Variables
│   │       ├── Add Environment Variable
│   │       │   ├── Key: SECRET_KEY
│   │       │   └── Value: [your-secret-key]
│   │       ├── Add Environment Variable
│   │       │   ├── Key: DEBUG
│   │       │   └── Value: False
│   │       └── ... (add more)
│   ├── Logs
│   └── Settings
```

---

## Quick Copy-Paste Checklist

Use this checklist to make sure you add all required variables:

- [ ] `SECRET_KEY` = [Generate using Python command above]
- [ ] `DEBUG` = `False`
- [ ] `ALLOWED_HOSTS` = `your-app-name.onrender.com`
- [ ] `DATABASE_URL` = [Auto-set or copy from PostgreSQL service]
- [ ] `OPENAI_API_KEY` = [Optional - your OpenAI key]
- [ ] `NEWS_API_KEY` = [Optional - your NewsAPI key]

---

## Common Issues

### Issue: "Invalid SECRET_KEY"
**Solution**: Make sure you generated a proper Django secret key using the command above. It should be a long random string.

### Issue: "DisallowedHost at /"
**Solution**: 
- Check that `ALLOWED_HOSTS` includes your exact Render URL
- Make sure there are no extra spaces
- Format: `your-app-name.onrender.com` (no `https://` prefix)

### Issue: Database connection errors
**Solution**:
- Verify `DATABASE_URL` is set correctly
- Check that your PostgreSQL database is running
- Ensure the database URL format is correct

### Issue: Static files not loading
**Solution**:
- This is usually handled automatically by the build command
- Check that `collectstatic` runs in your build command
- Verify WhiteNoise is in `requirements.txt`

---

## Testing Your Environment Variables

After deployment, you can verify your environment variables are set correctly:

1. Go to your service → "Logs" tab
2. Look for any error messages
3. If you see errors about missing variables, double-check your Environment tab

---

## Updating Environment Variables Later

To update environment variables:
1. Go to Environment tab
2. Click the pencil icon (✏️) next to the variable you want to edit
3. Update the value
4. Click "Save Changes"
5. Render will automatically redeploy

---

## Need Help?

- Check Render's documentation: https://render.com/docs/environment-variables
- Review your deployment logs in the "Logs" tab
- Make sure all required variables are set (especially `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS`)

---

**Pro Tip**: After setting up environment variables, your app should automatically redeploy. Wait for the deployment to complete (usually 2-3 minutes) before testing.

