from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    """Expense categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='💰', help_text="Emoji or icon name")
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Expense(models.Model):
    """User expenses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='expenses')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['user', 'category']),
        ]
    
    def __str__(self):
        return f"{self.title} - ${self.amount} ({self.user.username})"


class Budget(models.Model):
    """Monthly budgets for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'month', 'year']
        ordering = ['-year', '-month']
        indexes = [
            models.Index(fields=['user', '-year', '-month']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year}: ${self.amount}"
    
    def get_total_expenses(self):
        """Calculate total expenses for this budget period"""
        from django.db.models import Sum
        total = self.user.expenses.filter(
            date__year=self.year,
            date__month=self.month
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        return total
    
    def get_remaining(self):
        """Calculate remaining budget"""
        return self.amount - self.get_total_expenses()
    
    def get_percentage_used(self):
        """Calculate percentage of budget used"""
        if self.amount == 0:
            return 0
        return min(100, (self.get_total_expenses() / self.amount) * 100)
    
    def is_over_budget(self):
        """Check if user has exceeded budget"""
        return self.get_total_expenses() > self.amount


class Goal(models.Model):
    """Savings goals for users"""
    GOAL_STATUS = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    name = models.CharField(max_length=200, help_text="e.g., 'Trip to Europe', 'New Laptop'")
    description = models.TextField(blank=True)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    target_date = models.DateField(null=True, blank=True, help_text="Optional target date")
    status = models.CharField(max_length=20, choices=GOAL_STATUS, default='active')
    icon = models.CharField(max_length=50, default='🎯', help_text="Emoji or icon name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"{self.name} - ${self.current_amount}/{self.target_amount}"
    
    def get_progress_percentage(self):
        """Calculate progress percentage"""
        if self.target_amount == 0:
            return 0
        return min(100, (self.current_amount / self.target_amount) * 100)
    
    def get_remaining_amount(self):
        """Calculate remaining amount to reach goal"""
        return max(0, self.target_amount - self.current_amount)
    
    def is_completed(self):
        """Check if goal is completed"""
        return self.current_amount >= self.target_amount


class Article(models.Model):
    """Financial literacy articles"""
    ARTICLE_TYPE = [
        ('article', 'Article'),
        ('news', 'News'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles', help_text="User who submitted this article (null for admin/news articles)")
    article_type = models.CharField(max_length=20, choices=ARTICLE_TYPE, default='article', help_text="Type: Article (user-submitted) or News (from external source)")
    title = models.CharField(max_length=300)
    content = models.TextField()
    summary = models.TextField(max_length=500, blank=True, help_text="Short summary/description")
    category = models.CharField(max_length=100, blank=True, help_text="e.g., 'Savings', 'Investing', 'Budgeting'")
    source = models.CharField(max_length=200, blank=True, help_text="Source URL or name")
    author = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(blank=True, help_text="Optional image URL")
    is_featured = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['is_featured', '-created_at']),
            models.Index(fields=['article_type', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class UserProfile(models.Model):
    """User profile with currency preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    country = models.CharField(max_length=100, default='US', help_text="Country code (e.g., US, IN, GB)")
    currency_code = models.CharField(max_length=3, default='USD', help_text="ISO 4217 currency code (e.g., USD, INR, GBP)")
    currency_symbol = models.CharField(max_length=10, default='$', help_text="Currency symbol (e.g., $, ₹, £)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username} - {self.currency_code}"
    
    @staticmethod
    def get_currency_for_country(country_code):
        """Get currency information for a country"""
        country_currency_map = {
            'US': {'code': 'USD', 'symbol': '$'},
            'IN': {'code': 'INR', 'symbol': '₹'},
            'GB': {'code': 'GBP', 'symbol': '£'},
            'CA': {'code': 'CAD', 'symbol': 'C$'},
            'AU': {'code': 'AUD', 'symbol': 'A$'},
            'DE': {'code': 'EUR', 'symbol': '€'},
            'FR': {'code': 'EUR', 'symbol': '€'},
            'IT': {'code': 'EUR', 'symbol': '€'},
            'ES': {'code': 'EUR', 'symbol': '€'},
            'NL': {'code': 'EUR', 'symbol': '€'},
            'BE': {'code': 'EUR', 'symbol': '€'},
            'AT': {'code': 'EUR', 'symbol': '€'},
            'PT': {'code': 'EUR', 'symbol': '€'},
            'IE': {'code': 'EUR', 'symbol': '€'},
            'FI': {'code': 'EUR', 'symbol': '€'},
            'GR': {'code': 'EUR', 'symbol': '€'},
            'JP': {'code': 'JPY', 'symbol': '¥'},
            'CN': {'code': 'CNY', 'symbol': '¥'},
            'KR': {'code': 'KRW', 'symbol': '₩'},
            'SG': {'code': 'SGD', 'symbol': 'S$'},
            'MY': {'code': 'MYR', 'symbol': 'RM'},
            'TH': {'code': 'THB', 'symbol': '฿'},
            'ID': {'code': 'IDR', 'symbol': 'Rp'},
            'PH': {'code': 'PHP', 'symbol': '₱'},
            'VN': {'code': 'VND', 'symbol': '₫'},
            'BR': {'code': 'BRL', 'symbol': 'R$'},
            'MX': {'code': 'MXN', 'symbol': '$'},
            'AR': {'code': 'ARS', 'symbol': '$'},
            'ZA': {'code': 'ZAR', 'symbol': 'R'},
            'EG': {'code': 'EGP', 'symbol': 'E£'},
            'AE': {'code': 'AED', 'symbol': 'د.إ'},
            'SA': {'code': 'SAR', 'symbol': '﷼'},
            'NZ': {'code': 'NZD', 'symbol': 'NZ$'},
            'CH': {'code': 'CHF', 'symbol': 'CHF'},
            'SE': {'code': 'SEK', 'symbol': 'kr'},
            'NO': {'code': 'NOK', 'symbol': 'kr'},
            'DK': {'code': 'DKK', 'symbol': 'kr'},
            'PL': {'code': 'PLN', 'symbol': 'zł'},
            'RU': {'code': 'RUB', 'symbol': '₽'},
            'TR': {'code': 'TRY', 'symbol': '₺'},
        }
        
        country_code = country_code.upper()
        currency_info = country_currency_map.get(country_code, {'code': 'USD', 'symbol': '$'})
        return currency_info


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile when user is created"""
    if created:
        UserProfile.objects.get_or_create(user=instance, defaults={
            'country': 'US',
            'currency_code': 'USD',
            'currency_symbol': '$'
        })
