from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum, Q
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import HttpResponse
from datetime import datetime, timedelta
import csv
from .models import Transaction, Category, UserProfile, BudgetGoal, Currency
from .forms import TransactionForm, CategoryForm

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tracker/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Create default categories
            default_categories = [
                ('Salary', 'income'),
                ('Freelance', 'income'),
                ('Investment', 'income'),
                ('Groceries', 'expense'),
                ('Transport', 'expense'),
                ('Shopping', 'expense'),
                ('Entertainment', 'expense'),
                ('Bills', 'expense'),
            ]
            
            for name, cat_type in default_categories:
                Category.objects.create(user=user, name=name, category_type=cat_type)
            
            messages.success(request, 'Welcome to MoneyMap! Default categories have been created for you.')
            return redirect('set_income')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def dashboard(request):
    # Get filter parameters
    category_filter = request.GET.get('category', '')
    type_filter = request.GET.get('type', '')
    search_query = request.GET.get('search', '')
    month_filter = request.GET.get('month', '')
    year_filter = request.GET.get('year', '')
    
    # Get current month and year
    now = timezone.now()
    current_month = int(month_filter) if month_filter else now.month
    current_year = int(year_filter) if year_filter else now.year
    
    # Base queryset
    all_transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-id')
    
    # Apply filters
    if category_filter:
        all_transactions = all_transactions.filter(category_id=category_filter)
    
    if type_filter:
        all_transactions = all_transactions.filter(transaction_type=type_filter)
    
    if search_query:
        all_transactions = all_transactions.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Current month transactions
    monthly_transactions = Transaction.objects.filter(
        user=request.user,
        date__year=current_year,
        date__month=current_month
    )
    
    # Calculate totals
    total_income = Transaction.objects.filter(
        user=request.user, 
        transaction_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_expense = Transaction.objects.filter(
        user=request.user, 
        transaction_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    monthly_expense = monthly_transactions.filter(
        transaction_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Category-wise breakdown for current month
    category_breakdown = monthly_transactions.filter(
        transaction_type='expense'
    ).values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Get profile
    profile = request.user.profile
    
    # Balance calculation
    balance = profile.monthly_income - monthly_expense
    
    # Calculate percentage
    if profile.monthly_income > 0:
        expense_percentage = (monthly_expense / profile.monthly_income) * 100
    else:
        expense_percentage = 0
    
    # Pagination
    paginator = Paginator(all_transactions, 10)  # 10 transactions per page
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)
    
    # Get all categories for filter dropdown
    categories = Category.objects.filter(user=request.user)
    
    # Generate month/year options
    months = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    years = range(now.year - 2, now.year + 1)
    
    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'monthly_expense': monthly_expense,
        'balance': balance,
        'monthly_income': profile.monthly_income,
        'expense_percentage': expense_percentage,
        'category_breakdown': category_breakdown,
        'categories': categories,
        'months': months,
        'years': years,
        'selected_month': current_month,
        'selected_year': current_year,
        'selected_category': category_filter,
        'selected_type': type_filter,
        'search_query': search_query,
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def export_transactions(request):
    # Get all transactions for the user
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="moneymap_transactions.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Title', 'Category', 'Type', 'Amount', 'Description'])
    
    for transaction in transactions:
        writer.writerow([
            transaction.date.strftime('%Y-%m-%d'),
            transaction.title,
            transaction.category.name if transaction.category else 'Uncategorized',
            transaction.transaction_type.capitalize(),
            transaction.amount,
            transaction.description
        ])
    
    return response

@login_required
def analytics(request):
    now = timezone.now()
    
    # Last 6 months data for chart
    months_data = []
    for i in range(5, -1, -1):
        month_date = now - timedelta(days=30*i)
        month_transactions = Transaction.objects.filter(
            user=request.user,
            date__year=month_date.year,
            date__month=month_date.month
        )
        
        income = month_transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expense = month_transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        
        months_data.append({
            'month': month_date.strftime('%b %Y'),
            'income': float(income),
            'expense': float(expense)
        })
    
    # Category-wise data
    category_data = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__year=now.year,
        date__month=now.month
    ).values('category__name').annotate(total=Sum('amount')).order_by('-total')[:5]
    
    context = {
        'months_data': months_data,
        'category_data': list(category_data),
    }
    return render(request, 'tracker/analytics.html', context)

@login_required
def budget_goals(request):
    goals = BudgetGoal.objects.filter(user=request.user).select_related('category')
    
    # Calculate spending for each goal
    now = timezone.now()
    goals_with_spending = []
    
    for goal in goals:
        spent = Transaction.objects.filter(
            user=request.user,
            category=goal.category,
            transaction_type='expense',
            date__year=now.year,
            date__month=now.month
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        percentage = (spent / goal.monthly_limit * 100) if goal.monthly_limit > 0 else 0
        
        goals_with_spending.append({
            'goal': goal,
            'spent': spent,
            'remaining': goal.monthly_limit - spent,
            'percentage': min(percentage, 100)
        })
    
    context = {
        'goals_with_spending': goals_with_spending,
        'categories': Category.objects.filter(user=request.user, category_type='expense')
    }
    return render(request, 'tracker/budget_goals.html', context)

@login_required
def add_budget_goal(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        monthly_limit = request.POST.get('monthly_limit')
        
        category = get_object_or_404(Category, id=category_id, user=request.user)
        
        BudgetGoal.objects.update_or_create(
            user=request.user,
            category=category,
            defaults={'monthly_limit': monthly_limit}
        )
        
        messages.success(request, f'Budget goal set for {category.name}!')
        return redirect('budget_goals')
    
    return redirect('budget_goals')

@login_required
def profile_settings(request):
    profile = request.user.profile
    currencies = Currency.objects.all()
    
    if request.method == 'POST':
        monthly_income = request.POST.get('monthly_income')
        currency_id = request.POST.get('currency')
        
        if monthly_income:
            profile.monthly_income = monthly_income
        
        if currency_id:
            profile.currency_id = currency_id
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile_settings')
    
    context = {
        'profile': profile,
        'currencies': currencies
    }
    return render(request, 'tracker/profile_settings.html', context)

@login_required
def set_income(request):
    profile = request.user.profile
    if request.method == 'POST':
        monthly_income = request.POST.get('monthly_income')
        try:
            profile.monthly_income = float(monthly_income)
            profile.save()
            messages.success(request, 'Monthly income updated successfully!')
            return redirect('dashboard')
        except ValueError:
            messages.error(request, 'Please enter a valid amount')
    
    return render(request, 'tracker/set_income.html', {'profile': profile})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('dashboard')
    else:
        form = TransactionForm()
    
    form.fields['category'].queryset = Category.objects.filter(user=request.user)
    return render(request, 'tracker/add_transaction.html', {'form': form})

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('dashboard')
    else:
        form = TransactionForm(instance=transaction)
    
    form.fields['category'].queryset = Category.objects.filter(user=request.user)
    return render(request, 'tracker/edit_transaction.html', {'form': form, 'transaction': transaction})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('dashboard')
    return render(request, 'tracker/delete_transaction.html', {'transaction': transaction})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, 'tracker/add_category.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')
