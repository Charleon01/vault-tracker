from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ExpenseForm, CategoryForm




@login_required
def dashboard(request):
    user_expenses = Expense.objects.filter(user=request.user)
    
    # Use Decimal('0.00') instead of 0.00 float fallback
    total_spent = user_expenses.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    recent_expenses = user_expenses[:5]
    
    categories = Category.objects.filter(user=request.user)
    category_progress = []
    
    for cat in categories:
        spent = Expense.objects.filter(user=request.user, category=cat).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        budget = cat.monthly_budget or Decimal('0.00')
        
        # Cast both to float for safe percentage calculation
        if budget > 0:
            percentage = (float(spent) / float(budget)) * 100
        else:
            percentage = 0.0
            
        category_progress.append({
            'category': cat,
            'spent': spent,
            'budget': budget,
            'percentage': min(percentage, 100.0),
        })

    context = {
        'total_spent': total_spent,
        'recent_expenses': recent_expenses,
        'category_progress': category_progress,
    }
    return render(request, 'expenses/dashboard.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto log-in after registration
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'expenses/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    # Style AuthenticationForm inputs dynamically
    for field in form.fields.values():
        field.widget.attrs.update({
            'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500'
        })

    return render(request, 'expenses/login.html', {'form': form})



def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('dashboard')


@login_required
def add_expense(request):
    # Auto-generate default categories if user has none
    if not Category.objects.filter(user=request.user).exists():
        default_categories = ['Groceries', 'Utilities', 'Transportation', 'Entertainment']
        for cat_name in default_categories:
            Category.objects.create(user=request.user, name=cat_name, type='expense')

    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm(user=request.user)

    return render(request, 'expenses/add_expense.html', {'form': form})




@login_required
def manage_categories(request):
    categories = Category.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('manage_categories')
    else:
        form = CategoryForm()

    return render(request, 'expenses/manage_categories.html', {
        'form': form,
        'categories': categories
    })


