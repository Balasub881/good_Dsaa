from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import ExpenseForm, FilterForm
from .models import Category
from .models import Expense
from django.db.models import Sum
from datetime import datetime

def homepage(request):
    form = FilterForm()
    if request.method == 'POST':
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        expenses = Expense.objects.filter(date__gte=start, date__lte=end, user=request.user)
        value = expenses.aggregate(monthly_expense=Sum('amount'))
        categories = Category.objects.filter(expense__date__gte=start, expense__date__lte=end,
                                             expense__user=request.user).annotate(
            exp_sum=Sum('expense__amount')).values_list('name', 'exp_sum')
    else:
        expenses = Expense.objects.filter(date__month=datetime.today().month, date__year=datetime.today().year,
                                          user=request.user)
        value = expenses.aggregate(monthly_expense=Sum('amount'))
        categories = Category.objects.filter(expense__date__month=datetime.today().month,
                                             expense__date__year=datetime.today().year,
                                             expense__user=request.user).annotate(
            exp_sum=Sum('expense__amount')).values_list('name', 'exp_sum')
    labels = []
    data = []
    for cat in categories:
        labels.append(cat[0])
        data.append(cat[1])

    context = {
        'expenses': expenses,
        'total_expense': value['monthly_expense'],
        'data': data,
        'labels': labels,
        'form': form
    }

    return render(request, 'home.html', context)


class UserRegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

def logoutUser(request):
    logout(request)
    return redirect('login')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)

def add_expense(request):
        if request.method == 'POST':
            form = ExpenseForm(request.POST)
            if form.is_valid():
                expense = form.save(commit=False)
                expense.user = request.user
                expense.save()
                return redirect('home')
        elif request.method == 'GET':
            form = ExpenseForm()
        return render(request, 'ADD_EXPENSE.HTML.html', {'expense_form': form})


