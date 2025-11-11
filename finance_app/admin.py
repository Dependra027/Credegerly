from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category, Expense, Budget, Goal, Article, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'description']
    search_fields = ['name']


@admin.register(Expense)
class ExpenseAdmin(ImportExportModelAdmin):
    list_display = ['title', 'user', 'category', 'amount', 'date', 'created_at']
    list_filter = ['category', 'date', 'user']
    search_fields = ['title', 'description', 'user__username']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'month', 'year', 'amount', 'created_at']
    list_filter = ['year', 'month', 'user']
    search_fields = ['user__username']


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'target_amount', 'current_amount', 'status', 'target_date', 'created_at']
    list_filter = ['status', 'user', 'created_at']
    search_fields = ['name', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_featured', 'view_count', 'created_at']
    list_filter = ['category', 'is_featured', 'created_at']
    search_fields = ['title', 'content', 'summary', 'author']
    readonly_fields = ['view_count', 'created_at', 'updated_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'currency_code', 'currency_symbol', 'created_at']
    list_filter = ['country', 'currency_code']
    search_fields = ['user__username', 'user__email', 'country']
    readonly_fields = ['created_at', 'updated_at']

