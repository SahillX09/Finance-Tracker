from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('set-income/', views.set_income, name='set_income'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('edit-transaction/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('delete-transaction/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('add-category/', views.add_category, name='add_category'),
    path('logout/', views.logout_view, name='logout'),
    path('export/', views.export_transactions, name='export_transactions'),
    path('analytics/', views.analytics, name='analytics'),
    path('budget-goals/', views.budget_goals, name='budget_goals'),
    path('add-budget-goal/', views.add_budget_goal, name='add_budget_goal'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
]
