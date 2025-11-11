# How to Access Your Deployed Website on Render

After deploying your app to Render, here's how to find and access it.

---

## 🚀 Quick Steps

### Step 1: Find Your Website URL

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Log in to your account

2. **Click on Your Web Service**
   - Find your service (e.g., "credgerly" or whatever you named it)
   - Click on it to open the service dashboard

3. **Find Your URL**
   - At the top of the service page, you'll see your **service URL**
   - It will look like: `https://your-app-name.onrender.com`
   - This is your live website URL!

### Step 2: Check Deployment Status

Before accessing, make sure your app is deployed:

1. **Check the Status**
   - Look for a status indicator at the top (usually green "Live" or "Deployed")
   - If it says "Building" or "Deploying", wait a few minutes

2. **Check the Logs**
   - Click on the **"Logs"** tab in the left sidebar
   - Look for messages like:
     - ✅ "Build successful"
     - ✅ "Deployed successfully"
     - ✅ "Application is live"

### Step 3: Access Your Website

1. **Click the URL**
   - Click on the URL shown at the top of your service page
   - Or copy and paste it into your browser

2. **Or Use the "Open Live App" Button**
   - Some Render dashboards have an "Open Live App" button
   - Click it to open your website in a new tab

---

## 📍 Where to Find Your URL

### Option 1: Service Dashboard
```
Render Dashboard
└── Your Service (credgerly)
    └── Top of page: https://credgerly.onrender.com ← Your URL here!
```

### Option 2: Service Settings
1. Go to your service
2. Click **"Settings"** in the left sidebar
3. Scroll down to **"Service Details"**
4. Your URL is listed under **"Service URL"**

### Option 3: Overview Tab
1. Go to your service
2. Click **"Overview"** tab
3. Your URL is displayed prominently at the top

---

## 🔍 What Your URL Looks Like

Your Render URL follows this pattern:
```
https://[your-service-name].onrender.com
```

**Examples:**
- If your service is named `credgerly`: `https://credgerly.onrender.com`
- If your service is named `my-finance-app`: `https://my-finance-app.onrender.com`

---

## ✅ Testing Your Website

After accessing your URL, test these:

1. **Homepage/Login Page**
   - Should load without errors
   - Should show the login/signup interface

2. **Sign Up**
   - Create a test account
   - Verify registration works

3. **Login**
   - Log in with your test account
   - Should redirect to dashboard

4. **Core Features**
   - Add an expense
   - View dashboard
   - Check reports
   - Test budget feature

---

## 🐛 Troubleshooting

### Issue: "Service Unavailable" or 503 Error

**Possible Causes:**
- App is still deploying (wait 2-3 minutes)
- Build failed (check logs)
- Environment variables missing (check Environment tab)

**Solution:**
1. Check the **"Logs"** tab for errors
2. Verify all required environment variables are set
3. Wait for deployment to complete
4. Try refreshing the page

### Issue: "DisallowedHost" Error

**Cause:** `ALLOWED_HOSTS` doesn't match your URL

**Solution:**
1. Go to Environment tab
2. Check `ALLOWED_HOSTS` value
3. Make sure it matches your URL (e.g., `credgerly.onrender.com`)
4. Save and redeploy

### Issue: Page Loads But Shows Errors

**Solution:**
1. Check browser console (F12 → Console tab)
2. Check Render logs for backend errors
3. Verify database is connected
4. Check that migrations ran successfully

### Issue: Can't Find the URL

**Solution:**
1. Make sure your service is a **Web Service** (not a Background Worker)
2. Check that deployment completed successfully
3. Look in the "Overview" or "Settings" tab
4. The URL should be visible at the top of your service page

---

## 📱 Sharing Your Website

Once your app is live, you can:

1. **Share the URL** with others
   - Copy the URL from Render dashboard
   - Share it: `https://your-app-name.onrender.com`

2. **Add a Custom Domain** (Optional)
   - Go to Settings → Custom Domains
   - Add your own domain (e.g., `credgerly.com`)
   - Update `ALLOWED_HOSTS` to include your custom domain

---

## 🔄 After Making Changes

When you update your code:

1. **Push to GitHub** (if connected)
   - Render auto-deploys on push
   - Or manually trigger deployment

2. **Wait for Deployment**
   - Check "Events" or "Logs" tab
   - Wait for "Deployed successfully" message

3. **Refresh Your Browser**
   - Hard refresh: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)
   - Or clear cache and reload

---

## 📊 Monitoring Your Website

### Check Deployment Status
- **"Events"** tab: Shows deployment history
- **"Logs"** tab: Shows real-time logs and errors
- **"Metrics"** tab: Shows performance metrics (if available)

### Common Log Messages
- ✅ `Build successful` - Code built successfully
- ✅ `Deployed successfully` - App is live
- ✅ `Application is listening on port...` - Server is running
- ❌ `Build failed` - Check build logs for errors
- ❌ `Application failed to start` - Check environment variables

---

## 🎯 Quick Checklist

Before accessing your website, verify:

- [ ] Service status shows "Live" or "Deployed"
- [ ] Build completed successfully (check Logs)
- [ ] All environment variables are set
- [ ] Database is connected (if using PostgreSQL)
- [ ] Migrations ran successfully
- [ ] No errors in the Logs tab

---

## 💡 Pro Tips

1. **Bookmark Your URL** - Save it for easy access
2. **Check Logs Regularly** - Monitor for errors
3. **Test After Each Deploy** - Make sure everything works
4. **Use Incognito Mode** - Test without cached data
5. **Check Mobile View** - Test on phone/tablet too

---

## 🆘 Still Can't Access?

1. **Check Render Status**: https://status.render.com
2. **Review Logs**: Look for error messages
3. **Verify Environment Variables**: All required vars set?
4. **Check Build Command**: Is it correct?
5. **Contact Support**: Render has helpful support

---

**Your website should be accessible at: `https://[your-service-name].onrender.com`**

Just look for the URL at the top of your Render service dashboard! 🚀

