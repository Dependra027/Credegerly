# Smart Features Setup Guide

## Overview
Three new smart features have been added to Credgerly:

1. **AI Tips** - Personalized savings recommendations using OpenAI GPT
2. **Financial Literacy Articles** - Curated educational content
3. **Goal Tracker** - Save for specific goals (trips, purchases, etc.)

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
Create and apply migrations for the new models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. AI Tips Setup (Optional)
To enable AI-powered tips, set your OpenAI API key as an environment variable:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Note:** If no API key is set, the system will show default practical tips instead.

### 4. Create Sample Articles (Optional)
You can add financial literacy articles through the Django admin panel:

1. Go to `/admin/`
2. Navigate to "Articles"
3. Click "Add Article"
4. Fill in:
   - Title
   - Content (full article text)
   - Summary (short description)
   - Category (e.g., "Savings", "Investing", "Budgeting")
   - Author (optional)
   - Source URL (optional)
   - Image URL (optional)
   - Check "Is featured" for featured articles

### 5. Access the Features
- **AI Tips**: Navigate to "Smart Features" → "AI Tips" in the navbar
- **Articles**: Navigate to "Smart Features" → "Articles"
- **Goals**: Navigate to "Smart Features" → "Goals"

## Features Details

### AI Tips
- Analyzes your current month's spending patterns
- Provides personalized savings recommendations
- Refreshes tips based on your latest data
- Falls back to default tips if AI is unavailable

### Articles
- Browse financial literacy articles
- Search by title or content
- Filter by category
- Featured articles highlighted
- View tracking

### Goal Tracker
- Create savings goals with target amounts
- Track progress with visual progress bars
- Add progress manually
- Set target dates
- Auto-complete when goal is reached
- Status tracking (Active, Completed, Paused)

## Admin Features
All new models are registered in Django admin:
- **Goals**: Manage user goals
- **Articles**: Create and manage financial articles

## Next Steps
1. Run migrations
2. (Optional) Set OPENAI_API_KEY for AI tips
3. (Optional) Add some sample articles through admin
4. Start using the features!

## Notes
- AI Tips require an OpenAI API key (get one at https://platform.openai.com/)
- Articles can be manually added or scraped from external sources
- Goals are user-specific and private
- All features respect the dark mode theme






