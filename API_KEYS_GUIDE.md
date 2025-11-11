# How to Get API Keys for Credgerly

This guide will help you obtain the API keys needed for the AI Tips and Financial News features.

---

## 🔑 OpenAI API Key (for AI Tips Feature)

### What it's for:
- Generates personalized savings tips based on your spending patterns
- Provides AI-powered financial recommendations

### Steps to Get Your OpenAI API Key:

1. **Go to OpenAI Platform**
   - Visit: https://platform.openai.com/
   - Click **"Sign up"** or **"Log in"** if you already have an account

2. **Create/Login to Your Account**
   - Sign up with your email or use Google/Microsoft account
   - Verify your email address if required

3. **Navigate to API Keys**
   - Once logged in, click on your **profile icon** (top right)
   - Select **"API keys"** from the dropdown menu
   - Or go directly to: https://platform.openai.com/api-keys

4. **Create a New API Key**
   - Click the **"+ Create new secret key"** button
   - Give it a name (e.g., "Credgerly App")
   - Click **"Create secret key"**

5. **Copy Your API Key**
   - ⚠️ **IMPORTANT**: Copy the key immediately! You won't be able to see it again.
   - It will look like: `sk-proj-abc123xyz789...` (long string starting with `sk-`)
   - Save it securely (password manager, notes app, etc.)

6. **Add to Render**
   - Go to your Render service → Environment tab
   - Add variable:
     - **Key**: `OPENAI_API_KEY`
     - **Value**: Paste your copied key
   - Click "Save Changes"

### Pricing:
- OpenAI offers **free credits** for new users (usually $5-18 worth)
- After free credits, pay-as-you-go pricing applies
- AI tips feature uses minimal tokens, so it's very affordable
- Check current pricing: https://openai.com/pricing

### Important Notes:
- ⚠️ Keep your API key secret - never share it publicly
- ⚠️ If you lose it, you'll need to create a new one
- ⚠️ Monitor your usage to avoid unexpected charges
- The app will work without this key (uses default tips instead)

---

## 📰 NewsAPI Key (for Financial News Feature)

### What it's for:
- Fetches latest financial news articles
- Displays global financial news on the Articles page

### Steps to Get Your NewsAPI Key:

1. **Go to NewsAPI Website**
   - Visit: https://newsapi.org/
   - Click **"Get API Key"** button (top right)

2. **Create an Account**
   - Click **"Get API Key"**
   - Fill in the registration form:
     - Email address
     - Password
     - First name
     - Last name
   - Accept the terms and conditions
   - Click **"Create Account"**

3. **Verify Your Email**
   - Check your email inbox
   - Click the verification link sent by NewsAPI

4. **Get Your API Key**
   - After verification, you'll be redirected to your dashboard
   - Your API key will be displayed on the dashboard
   - It will look like: `abc123def456ghi789...` (long alphanumeric string)
   - Copy this key

5. **Add to Render**
   - Go to your Render service → Environment tab
   - Add variable:
     - **Key**: `NEWS_API_KEY`
     - **Value**: Paste your copied key
   - Click "Save Changes"

### Pricing:
- **Free tier**: 100 requests per day (perfect for personal use)
- **Developer tier**: $449/month (for higher volume)
- For Credgerly, the free tier is usually sufficient

### Important Notes:
- ⚠️ Free tier has rate limits (100 requests/day)
- ⚠️ Free tier is for development/testing only
- ⚠️ For production apps, consider upgrading
- The app will work without this key (just won't fetch external news)

---

## 🚀 Quick Setup Checklist

### OpenAI API Key:
- [ ] Sign up at https://platform.openai.com/
- [ ] Go to API Keys section
- [ ] Create new secret key
- [ ] Copy the key (starts with `sk-`)
- [ ] Add to Render as `OPENAI_API_KEY`

### NewsAPI Key:
- [ ] Sign up at https://newsapi.org/register
- [ ] Verify your email
- [ ] Copy API key from dashboard
- [ ] Add to Render as `NEWS_API_KEY`

---

## 💡 Do I Need Both Keys?

**Short answer: No!** Both are optional.

- **Without OpenAI Key**: App works fine, shows default savings tips instead of AI-generated ones
- **Without NewsAPI Key**: App works fine, just won't fetch external financial news
- **Without Both**: App works perfectly, just missing these enhanced features

The core features (expense tracking, budgets, reports, goals) work without any API keys!

---

## 🔒 Security Best Practices

1. **Never commit API keys to Git**
   - They're already in `.gitignore`
   - Always use environment variables

2. **Don't share your keys**
   - Treat them like passwords
   - If exposed, revoke and create new ones

3. **Monitor usage**
   - Check OpenAI dashboard for usage
   - Check NewsAPI dashboard for request count

4. **Rotate keys periodically**
   - Good security practice
   - Create new keys and update in Render

---

## 🆘 Troubleshooting

### "Invalid API Key" Error

**OpenAI:**
- Make sure you copied the entire key (they're long!)
- Check for extra spaces before/after
- Verify the key starts with `sk-`
- Try creating a new key if needed

**NewsAPI:**
- Verify your email is confirmed
- Check you copied the full key
- Make sure there are no spaces
- Try regenerating if needed

### "Rate Limit Exceeded"

**NewsAPI:**
- Free tier: 100 requests/day
- Wait 24 hours or upgrade plan
- App will still work, just won't fetch new news

**OpenAI:**
- Check your usage in OpenAI dashboard
- You may have exceeded free credits
- Add payment method if needed

### API Not Working

1. Check environment variables are set correctly in Render
2. Verify keys are correct (no typos)
3. Check Render logs for error messages
4. Test keys directly:
   - OpenAI: https://platform.openai.com/playground
   - NewsAPI: https://newsapi.org/docs/endpoints/everything

---

## 📚 Additional Resources

- **OpenAI Documentation**: https://platform.openai.com/docs
- **NewsAPI Documentation**: https://newsapi.org/docs
- **OpenAI Pricing**: https://openai.com/pricing
- **NewsAPI Pricing**: https://newsapi.org/pricing

---

## ✅ After Adding Keys

1. **Save changes in Render**
2. **Wait for redeployment** (2-3 minutes)
3. **Test the features**:
   - Visit "AI Tips" page - should show personalized tips
   - Visit "Articles" page - should show financial news
4. **Check logs** if something doesn't work

---

**Need help?** Check the Render logs or review the error messages in your app.

