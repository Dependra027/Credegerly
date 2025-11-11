from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='finance_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Expenses
    path('expenses/', views.expense_list_view, name='expense_list'),
    path('expenses/add/', views.expense_create_view, name='expense_create'),
    path('expenses/<int:pk>/edit/', views.expense_edit_view, name='expense_edit'),
    path('expenses/<int:pk>/delete/', views.expense_delete_view, name='expense_delete'),
    
    # Budget
    path('budgets/', views.budget_list_view, name='budget_list'),
    path('budgets/add/', views.budget_create_view, name='budget_create'),
    
    # Reports
    path('reports/', views.reports_view, name='reports'),
    
    # Export
    path('export/csv/', views.export_csv_view, name='export_csv'),
    path('export/pdf/', views.export_pdf_view, name='export_pdf'),
    
    # Smart Features
    path('ai-tips/', views.ai_tips_view, name='ai_tips'),
    path('articles/', views.articles_view, name='articles'),
    path('articles/add/', views.article_create_view, name='article_create'),
    path('articles/<int:pk>/', views.article_detail_view, name='article_detail'),
    path('goals/', views.goals_view, name='goals'),
    path('goals/add/', views.goal_create_view, name='goal_create'),
    path('goals/<int:pk>/edit/', views.goal_edit_view, name='goal_edit'),
    path('goals/<int:pk>/delete/', views.goal_delete_view, name='goal_delete'),
    path('goals/<int:pk>/add-progress/', views.goal_add_progress_view, name='goal_add_progress'),
]

