from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import csv
import json
import os
import re
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from .models import Expense, Budget, Category, Goal, Article, UserProfile
from .forms import SignUpForm, ExpenseForm, BudgetForm, ExpenseFilterForm, GoalForm, ArticleForm
from .currency_utils import format_currency, get_user_currency


def signup_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Get country and set currency
            country = form.cleaned_data.get('country')
            currency_info = UserProfile.get_currency_for_country(country)
            
            # Update or create user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.country = country
            profile.currency_code = currency_info['code']
            profile.currency_symbol = currency_info['symbol']
            profile.save()
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please log in.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'finance_app/signup.html', {'form': form})


@login_required
def dashboard_view(request):
    """Main dashboard with statistics"""
    user = request.user
    now = timezone.now()
    current_month = now.month
    current_year = now.year
    
    # Get current month budget
    try:
        current_budget = Budget.objects.get(user=user, month=current_month, year=current_year)
    except Budget.DoesNotExist:
        current_budget = None
    
    # Current month expenses
    current_month_expenses = Expense.objects.filter(
        user=user,
        date__year=current_year,
        date__month=current_month
    )
    
    total_expenses = current_month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    expense_count = current_month_expenses.count()
    
    # Budget calculations
    remaining_budget = 0
    budget_percentage = 0
    is_over_budget = False
    if current_budget:
        remaining_budget = current_budget.get_remaining()
        budget_percentage = current_budget.get_percentage_used()
        is_over_budget = current_budget.is_over_budget()
    
    # Recent expenses (last 5)
    recent_expenses = Expense.objects.filter(user=user).order_by('-date', '-created_at')[:5]
    
    # Category breakdown for current month
    category_data = list(current_month_expenses.values('category__name').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total'))
    
    # Monthly trend (last 6 months)
    monthly_trends = []
    for i in range(5, -1, -1):
        month_date = now - timedelta(days=30*i)
        month_expenses = Expense.objects.filter(
            user=user,
            date__year=month_date.year,
            date__month=month_date.month
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_trends.append({
            'month': month_date.strftime('%b %Y'),
            'amount': float(month_expenses)
        })
    
    # Upcoming bills (expenses in next 7 days)
    upcoming_date = now.date() + timedelta(days=7)
    upcoming_expenses = Expense.objects.filter(
        user=user,
        date__gte=now.date(),
        date__lte=upcoming_date
    ).order_by('date')[:5]
    
    # Convert Decimal totals for JSON
    category_data_list = []
    for item in category_data:
        category_data_list.append({
            'category__name': item.get('category__name'),
            'total': float(item.get('total') or 0),
            'count': item.get('count')
        })
    
    context = {
        'total_expenses': total_expenses,
        'expense_count': expense_count,
        'current_budget': current_budget,
        'remaining_budget': remaining_budget,
        'budget_percentage': budget_percentage,
        'is_over_budget': is_over_budget,
        'recent_expenses': recent_expenses,
        'category_data': category_data_list,
        'monthly_trends_json': json.dumps(monthly_trends),
        'category_data_json': json.dumps(category_data_list),
        'upcoming_expenses': upcoming_expenses,
    }
    return render(request, 'finance_app/dashboard.html', context)


@login_required
def expense_list_view(request):
    """List all expenses with filters"""
    user = request.user
    expenses = Expense.objects.filter(user=user).order_by('-date', '-created_at')
    
    # Apply filters
    form = ExpenseFilterForm(request.GET)
    if form.is_valid():
        category = form.cleaned_data.get('category')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        min_amount = form.cleaned_data.get('min_amount')
        max_amount = form.cleaned_data.get('max_amount')
        
        if category:
            expenses = expenses.filter(category=category)
        if start_date:
            expenses = expenses.filter(date__gte=start_date)
        if end_date:
            expenses = expenses.filter(date__lte=end_date)
        if min_amount:
            expenses = expenses.filter(amount__gte=min_amount)
        if max_amount:
            expenses = expenses.filter(amount__lte=max_amount)
    
    # Calculate total
    total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get categories for modal
    categories = Category.objects.all().order_by('name')
    
    context = {
        'expenses': expenses,
        'form': form,
        'total_amount': total_amount,
        'categories': categories,
    }
    return render(request, 'finance_app/expense_list.html', context)


@login_required
def expense_create_view(request):
    """Create new expense"""
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'finance_app/expense_form.html', {'form': form, 'title': 'Add Expense'})


@login_required
def expense_edit_view(request, pk):
    """Edit existing expense"""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'finance_app/expense_form.html', {'form': form, 'title': 'Edit Expense', 'expense': expense})


@login_required
def expense_delete_view(request, pk):
    """Delete expense"""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expense_list')
    return render(request, 'finance_app/expense_confirm_delete.html', {'expense': expense})


@login_required
def budget_list_view(request):
    """List all budgets"""
    budgets = Budget.objects.filter(user=request.user).order_by('-year', '-month')
    for budget in budgets:
        budget.total_expenses = budget.get_total_expenses()
        budget.remaining = budget.get_remaining()
        budget.percentage = budget.get_percentage_used()
        budget.is_over = budget.is_over_budget()
    return render(request, 'finance_app/budget_list.html', {'budgets': budgets})


@login_required
def budget_create_view(request):
    """Create or update budget"""
    if request.method == 'POST':
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        budget, created = Budget.objects.get_or_create(
            user=request.user,
            month=month,
            year=year,
            defaults={'amount': Decimal(request.POST.get('amount'))}
        )
        if not created:
            budget.amount = Decimal(request.POST.get('amount'))
            budget.save()
        messages.success(request, f'Budget for {month}/{year} {"created" if created else "updated"} successfully!')
        return redirect('budget_list')
    else:
        form = BudgetForm(initial={'month': timezone.now().month, 'year': timezone.now().year})
    return render(request, 'finance_app/budget_form.html', {'form': form})


@login_required
def reports_view(request):
    """Reports and analytics page"""
    user = request.user
    now = timezone.now()
    
    # Get date range (default: last 6 months)
    months_back = int(request.GET.get('months', 6))
    start_date = now - timedelta(days=30*months_back)
    
    expenses = Expense.objects.filter(user=user, date__gte=start_date.date())
    
    # Category distribution (pie chart data)
    category_dist = expenses.values('category__name', 'category__icon').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Monthly trend (line chart data)
    monthly_data = {}
    for expense in expenses:
        key = expense.date.strftime('%Y-%m')
        if key not in monthly_data:
            monthly_data[key] = 0
        monthly_data[key] += float(expense.amount)
    
    monthly_trend = [{'month': k, 'amount': v} for k, v in sorted(monthly_data.items())]
    
    # Category comparison (bar chart data)
    category_comparison = list(category_dist.values('category__name', 'total'))
    
    # Convert Decimals to floats for JSON serialization
    category_dist_list = list(category_dist)
    for item in category_dist_list:
        item['total'] = float(item['total'] or 0)
    for item in category_comparison:
        item['total'] = float(item['total'] or 0)
    
    # Serialize data for JavaScript
    category_dist_json = json.dumps(category_dist_list)
    monthly_trend_json = json.dumps(monthly_trend)
    category_comparison_json = json.dumps(category_comparison)
    
    # High-level KPIs
    total_spend = float(expenses.aggregate(Sum('amount'))['amount__sum'] or 0)
    months_in_range = max(1, len(monthly_data.keys()))
    average_monthly = total_spend / months_in_range
    top_category = None
    if category_dist_list:
        top_item = category_dist_list[0]
        top_category = {
            'name': top_item.get('category__name') or 'Uncategorized',
            'icon': top_item.get('category__icon', ''),
            'total': float(top_item.get('total') or 0),
        }
    
    context = {
        'category_dist': category_dist_list,
        'category_dist_json': category_dist_json,
        'monthly_trend': monthly_trend,
        'monthly_trend_json': monthly_trend_json,
        'category_comparison': category_comparison,
        'category_comparison_json': category_comparison_json,
        'months_back': months_back,
        'total_spend': total_spend,
        'average_monthly': average_monthly,
        'top_category': top_category,
    }
    return render(request, 'finance_app/reports.html', context)


@login_required
def export_csv_view(request):
    """Export expenses to CSV"""
    user = request.user
    expenses = Expense.objects.filter(user=user).order_by('-date', '-created_at')
    
    # Get user's currency
    currency_info = get_user_currency(user)
    currency_symbol = currency_info['symbol']
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="expenses_{user.username}_{timezone.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Title', 'Category', 'Amount', 'Description'])
    
    for expense in expenses:
        # Format amount with user's currency
        formatted_amount = format_currency(expense.amount, currency_symbol)
        writer.writerow([
            expense.date.strftime('%Y-%m-%d'),
            expense.title,
            expense.category.name if expense.category else 'N/A',
            formatted_amount,
            expense.description
        ])
    
    return response


@login_required
def export_pdf_view(request):
    """Export expenses to PDF"""
    user = request.user
    expenses = Expense.objects.filter(user=user).order_by('-date', '-created_at')
    
    # Get user's currency
    currency_info = get_user_currency(user)
    currency_symbol = currency_info['symbol']
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="expenses_{user.username}_{timezone.now().strftime("%Y%m%d")}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"Expense Report - {user.username}", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Summary
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    formatted_total = format_currency(total, currency_symbol)
    summary = Paragraph(f"Total Expenses: {formatted_total} | Count: {expenses.count()}", styles['Normal'])
    elements.append(summary)
    elements.append(Spacer(1, 0.2*inch))
    
    # Table data
    data = [['Date', 'Title', 'Category', 'Amount']]
    for expense in expenses:
        # Format amount with user's currency
        formatted_amount = format_currency(expense.amount, currency_symbol)
        data.append([
            expense.date.strftime('%Y-%m-%d'),
            expense.title,
            expense.category.name if expense.category else 'N/A',
            formatted_amount
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    return response


@login_required
def ai_tips_view(request):
    """AI-powered savings tips based on user's spending patterns"""
    user = request.user
    now = timezone.now()
    
    # Get user's spending data for context
    current_month_expenses = Expense.objects.filter(
        user=user,
        date__year=now.year,
        date__month=now.month
    )
    
    total_spent = current_month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    expense_count = current_month_expenses.count()
    
    # Get top spending categories with amounts
    top_categories = current_month_expenses.values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')[:5]
    
    # Get user currency for category breakdown
    from .currency_utils import get_user_currency
    currency_info = get_user_currency(user)
    currency_symbol = currency_info['symbol']
    
    # Get category breakdown for detailed analysis
    category_breakdown = []
    for cat in top_categories:
        cat_name = cat['category__name'] or 'Uncategorized'
        cat_total = float(cat['total'])
        percentage = (cat_total / float(total_spent) * 100) if total_spent > 0 else 0
        category_breakdown.append(f"{cat_name}: {currency_symbol}{cat_total:.2f} ({percentage:.1f}%)")
    
    # Get last month's spending for comparison
    last_month = now.month - 1
    last_month_year = now.year
    if last_month == 0:
        last_month = 12
        last_month_year = now.year - 1
    else:
        last_month_year = now.year
    
    last_month_expenses = Expense.objects.filter(
        user=user,
        date__year=last_month_year,
        date__month=last_month
    )
    last_month_total = last_month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate spending trend
    spending_change = 0
    if last_month_total > 0:
        spending_change = ((float(total_spent) - float(last_month_total)) / float(last_month_total)) * 100
    
    # Get current budget if exists
    try:
        current_budget = Budget.objects.get(user=user, month=now.month, year=now.year)
        budget_remaining = current_budget.get_remaining()
        budget_percentage = current_budget.get_percentage_used()
        is_over_budget = current_budget.is_over_budget()
        budget_info = f"Budget: {currency_symbol}{current_budget.amount:.2f}, Spent: {currency_symbol}{total_spent:.2f}, Remaining: {currency_symbol}{budget_remaining:.2f}, Usage: {budget_percentage:.1f}%"
        if is_over_budget:
            budget_info += " (OVER BUDGET)"
    except Budget.DoesNotExist:
        budget_info = "No budget set for this month"
        budget_percentage = 0
        is_over_budget = False
    
    # Get average transaction amount
    avg_transaction = float(total_spent) / expense_count if expense_count > 0 else 0
    
    # Prepare detailed context for AI
    spending_summary = {
        'total_spent': float(total_spent),
        'expense_count': expense_count,
        'top_categories': [cat['category__name'] or 'Uncategorized' for cat in top_categories],
        'category_breakdown': category_breakdown,
        'budget_info': budget_info,
        'last_month_total': float(last_month_total),
        'spending_change': spending_change,
        'avg_transaction': avg_transaction,
        'budget_percentage': budget_percentage,
        'is_over_budget': is_over_budget,
    }
    
    # Get AI tips (optional - requires OpenAI API key)
    # Always generate fresh tips on each request for real-time updates
    ai_tips = []
    error_message = None
    
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    if openai_api_key and HAS_REQUESTS:
        try:
            # Prepare detailed, personalized prompt
            prompt = f"""You are a personal financial advisor analyzing a user's spending data. Provide 4-6 SPECIFIC, PERSONALIZED savings tips based on their actual spending patterns. Make each tip unique and tailored to their situation.

USER'S FINANCIAL DATA:
- Current Month Spending: {currency_symbol}{spending_summary['total_spent']:.2f}
- Number of Transactions: {spending_summary['expense_count']}
- Average Transaction Size: {currency_symbol}{spending_summary['avg_transaction']:.2f}
- Top Spending Categories: {', '.join(spending_summary['category_breakdown']) if spending_summary['category_breakdown'] else 'No categories yet'}
- Budget Status: {spending_summary['budget_info']}
- Last Month Spending: {currency_symbol}{spending_summary['last_month_total']:.2f}
- Spending Change: {spending_summary['spending_change']:+.1f}% {'increase' if spending_summary['spending_change'] > 0 else 'decrease'} from last month

INSTRUCTIONS:
1. Analyze their specific spending patterns (which categories they spend most on)
2. Consider their spending trends (increasing/decreasing)
3. Provide actionable, specific tips that directly address their spending habits
4. Reference their actual categories and amounts when relevant
5. If they're over budget, focus on immediate cost-cutting strategies
6. If spending increased, suggest ways to reverse the trend
7. Make tips personal - mention their specific categories or spending patterns
8. Format as a numbered list (1., 2., 3., etc.)
9. Each tip should be 2-3 sentences and be SPECIFIC to their data, not generic advice

Generate tips NOW based on this user's unique financial situation:"""
            
            # Call OpenAI API
            headers = {
                'Authorization': f'Bearer {openai_api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'system', 'content': 'You are an expert personal financial advisor. You analyze spending data and provide SPECIFIC, PERSONALIZED savings tips tailored to each individual\'s unique spending patterns. Never give generic advice - always reference the user\'s actual data.'},
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': 500,
                'temperature': 0.9  # Higher temperature for more varied, creative responses
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                tips_text = result['choices'][0]['message']['content']
                # Parse tips into list - handle various formats
                ai_tips = []
                for line in tips_text.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                    # Check if line starts with number, bullet, or dash
                    if (line and len(line) > 2 and 
                        (line[0].isdigit() or 
                         line.startswith('-') or 
                         line.startswith('•') or
                         line.startswith('*') or
                         (line[0].isupper() and '.' in line[:5]))):
                        # Remove numbering/bullets and clean
                        cleaned = line
                        # Remove leading numbers and dots
                        if cleaned[0].isdigit():
                            parts = cleaned.split('.', 1)
                            if len(parts) > 1:
                                cleaned = parts[1].strip()
                        # Remove bullets
                        cleaned = cleaned.lstrip('-•* ').strip()
                        if cleaned:
                            ai_tips.append(cleaned)
                
                # If parsing failed, try splitting by common patterns
                if not ai_tips:
                    # Try splitting by numbered patterns
                    tips = re.split(r'\n\s*\d+[\.\)]\s*', tips_text)
                    ai_tips = [tip.strip() for tip in tips if tip.strip() and len(tip.strip()) > 20]
                
                # Final fallback
                if not ai_tips:
                    ai_tips = [tips_text]  # Fallback to full text
            else:
                error_message = "Unable to fetch AI tips. Please try again later."
        except Exception as e:
            error_message = f"AI service temporarily unavailable: {str(e)}. Using default tips."
            # Fallback tips
            ai_tips = [
                "Track your spending daily to identify unnecessary expenses.",
                "Set up automatic transfers to a savings account each payday.",
                "Review subscriptions monthly and cancel unused services.",
                "Use the 24-hour rule: wait a day before making non-essential purchases.",
                "Cook at home more often - it's healthier and cheaper than eating out."
            ]
    else:
        # Default tips when API key is not available
        ai_tips = [
            "Track your spending daily to identify unnecessary expenses.",
            "Set up automatic transfers to a savings account each payday.",
            "Review subscriptions monthly and cancel unused services.",
            "Use the 24-hour rule: wait a day before making non-essential purchases.",
            "Cook at home more often - it's healthier and cheaper than eating out.",
            "Compare prices before making large purchases.",
            "Build an emergency fund covering 3-6 months of expenses."
        ]
    
    # Get current timestamp for tips generation
    tips_generated_at = timezone.now()
    
    context = {
        'ai_tips': ai_tips,
        'spending_summary': spending_summary,
        'error_message': error_message,
        'has_api_key': bool(openai_api_key),
        'tips_generated_at': tips_generated_at,
    }
    
    # Check if this is an AJAX request for real-time refresh
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON for AJAX requests
        return JsonResponse({
            'ai_tips': ai_tips,
            'spending_summary': spending_summary,
            'error_message': error_message,
            'tips_generated_at': tips_generated_at.strftime('%H:%M:%S'),
            'tips_generated_at_iso': tips_generated_at.isoformat(),
        })
    
    response = render(request, 'finance_app/ai_tips.html', context)
    # Add cache control headers to prevent caching - ensure real-time updates
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['X-Accel-Expires'] = '0'
    return response


def fetch_financial_news():
    """Fetch financial news from NewsAPI"""
    news_api_key = os.getenv('NEWS_API_KEY', '')
    news_articles = []
    
    if not news_api_key or not HAS_REQUESTS:
        return news_articles
    
    try:
        # NewsAPI endpoint for financial news
        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': 'finance OR financial OR economy OR stock market OR investing OR cryptocurrency',
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 10,
            'apiKey': news_api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                for item in data.get('articles', [])[:10]:
                    # Check if news article already exists in database
                    existing = Article.objects.filter(
                        article_type='news',
                        title=item.get('title', '')[:300],
                        source=item.get('url', '')[:200]
                    ).first()
                    
                    if not existing and item.get('title') and item.get('description'):
                        # Create news article in database
                        content_text = item.get('content', '') or item.get('description', '')
                        # Truncate content if too long (Article.content is TextField, but we'll limit for consistency)
                        if len(content_text) > 10000:
                            content_text = content_text[:10000] + '...'
                        
                        news_article = Article.objects.create(
                            article_type='news',
                            title=item.get('title', '')[:300],
                            summary=item.get('description', '')[:500] if item.get('description') else '',
                            content=content_text,
                            author=item.get('author', '')[:200] if item.get('author') else 'News Source',
                            source=item.get('url', '')[:200] if item.get('url') else '',
                            image_url=item.get('urlToImage', '')[:500] if item.get('urlToImage') else '',
                            category='News',
                        )
                        news_articles.append(news_article)
                    elif existing:
                        news_articles.append(existing)
    except Exception as e:
        print(f"Error fetching news: {e}")
    
    return news_articles


@login_required
def articles_view(request):
    """Financial literacy articles and news"""
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    show_type = request.GET.get('type', 'all')  # all, article, news
    
    # Get user articles (not news)
    articles = Article.objects.filter(article_type='article')
    
    # Get news articles (don't slice yet - apply filters first)
    news_articles = Article.objects.filter(article_type='news').order_by('-created_at')
    
    # If no news in database, try to fetch
    if not news_articles.exists():
        fetched_news = fetch_financial_news()
        if fetched_news:
            # Re-fetch after adding news
            news_articles = Article.objects.filter(article_type='news').order_by('-created_at')
    
    # Apply filters to articles
    if category_filter:
        articles = articles.filter(category__icontains=category_filter)
    
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(summary__icontains=search_query)
        )
        news_articles = news_articles.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(summary__icontains=search_query)
        )
    
    # Filter by type
    if show_type == 'article':
        news_articles = Article.objects.none()
    elif show_type == 'news':
        articles = Article.objects.none()
    
    # Get unique categories for filter
    categories = Article.objects.filter(article_type='article').values_list('category', flat=True).distinct()
    categories = [cat for cat in categories if cat]
    
    # Featured articles first (only user articles, not news)
    featured = articles.filter(is_featured=True)[:3]
    other_articles = articles.exclude(id__in=[a.id for a in featured])
    
    # Slice news articles after all filters are applied (limit to 10)
    news_articles = news_articles[:10]
    
    context = {
        'featured_articles': featured,
        'articles': other_articles,
        'news_articles': news_articles,
        'categories': categories,
        'current_category': category_filter,
        'search_query': search_query,
        'show_type': show_type,
    }
    return render(request, 'finance_app/articles.html', context)


@login_required
def article_create_view(request):
    """Create a new article"""
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.article_type = 'article'
            article.save()
            messages.success(request, 'Your article has been submitted successfully!')
            return redirect('articles')
    else:
        form = ArticleForm()
    
    context = {
        'form': form,
    }
    return render(request, 'finance_app/article_create.html', context)


@login_required
def article_detail_view(request, pk):
    """Article detail view"""
    article = get_object_or_404(Article, pk=pk)
    article.increment_view_count()
    
    # Get related articles (same type and category)
    related_articles = Article.objects.filter(
        article_type=article.article_type,
        category=article.category
    ).exclude(pk=pk)[:3]
    
    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'finance_app/article_detail.html', context)


@login_required
def goals_view(request):
    """Goal tracker - list all goals"""
    goals = Goal.objects.filter(user=request.user).order_by('-created_at')
    
    # Calculate stats
    total_goals = goals.count()
    active_goals = goals.filter(status='active').count()
    completed_goals = goals.filter(status='completed').count()
    total_target = sum([float(g.target_amount) for g in goals])
    total_saved = sum([float(g.current_amount) for g in goals])
    overall_progress = (total_saved / total_target * 100) if total_target > 0 else 0
    
    context = {
        'goals': goals,
        'total_goals': total_goals,
        'active_goals': active_goals,
        'completed_goals': completed_goals,
        'total_target': total_target,
        'total_saved': total_saved,
        'overall_progress': overall_progress,
    }
    return render(request, 'finance_app/goals.html', context)


@login_required
def goal_create_view(request):
    """Create new goal"""
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Goal created successfully!')
            return redirect('goals')
    else:
        form = GoalForm()
    return render(request, 'finance_app/goal_form.html', {'form': form, 'title': 'Create Goal'})


@login_required
def goal_edit_view(request, pk):
    """Edit existing goal"""
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            # Auto-complete if reached target
            if goal.current_amount >= goal.target_amount and goal.status != 'completed':
                goal.status = 'completed'
                goal.save()
                messages.success(request, 'Congratulations! Goal completed!')
            else:
                messages.success(request, 'Goal updated successfully!')
            return redirect('goals')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'finance_app/goal_form.html', {'form': form, 'title': 'Edit Goal', 'goal': goal})


@login_required
def goal_delete_view(request, pk):
    """Delete goal"""
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted successfully!')
        return redirect('goals')
    return render(request, 'finance_app/goal_confirm_delete.html', {'goal': goal})


@login_required
def goal_add_progress_view(request, pk):
    """Add progress to a goal (AJAX endpoint)"""
    if request.method == 'POST':
        goal = get_object_or_404(Goal, pk=pk, user=request.user)
        try:
            amount = Decimal(request.POST.get('amount', 0))
            goal.current_amount += amount
            if goal.current_amount >= goal.target_amount and goal.status != 'completed':
                goal.status = 'completed'
            goal.save()
            return JsonResponse({
                'success': True,
                'current_amount': float(goal.current_amount),
                'progress_percentage': float(goal.get_progress_percentage()),
                'is_completed': goal.is_completed()
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

