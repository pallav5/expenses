from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from income.forms import IncomeForm
from category.forms import CategoryForm
from category.models import Category
from income.models import Income
from expenses.forms import ExpensesForm
from expenses.models import Expenses
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models.aggregates import Sum
# Create your views here.

def signin(request):
    if request.method=='GET':
        return render(request,'signin.html')
    else:
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u,password=p)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        return render(request,'signin.html',{'errmsg':'Username and password doesnot match'})



def signup(request):
    if request.method=='GET':
        context = {
        'form':UserCreationForm()
    }
        return render(request,'signup.html',context)
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render (request,'signup.html',{'form':form})

@login_required(login_url='login')
def dashboard(request):
    data = sum_by_categoryexp(request.user.id)
    data1 = sum_by_categoryexp1(request.user.id)
    evs = expensesvssaving(request.user.id)
    context = {

        'data': data,
        'evs': evs,
        'data1': data1,

    }

    return render(request,'dashboard.html',context)

@login_required(login_url='login')
def income(request):
    if request.method=='GET':
        context = {
            'form':IncomeForm(),
            'income': Income.objects.filter(user_id=request.user.id,date__month=getCurrentMonth(),date__year=getCurrentYear()),
            'total': Income.objects.filter(user_id=request.user.id, date__month=getCurrentMonth(),date__year=getCurrentYear()).aggregate(Sum('rupees')),
            'prevIn': getPreviousMonthdataInc(request.user.id),
            'prevTotal': getPreviousMonthdataInc(request.user.id).aggregate(Sum('rupees'))

        }

        return render(request,'income.html',context)
    else:
        form = IncomeForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user_id = request.user.id
            data.save()
            return redirect('income')
        return render(request,'income.html',{'form':form})

@login_required(login_url='login')
def expenses(request):
    data = sum_by_categoryexp(request.user.id)
    if request.method == 'GET':
        context = {
                'form': ExpensesForm(request.user),
                'expenses': Expenses.objects.filter(user_id=request.user.id,date__month=getCurrentMonth(),date__year=getCurrentYear()) [::-1] ,
                'total':Expenses.objects.filter(user_id=request.user.id,date__month=getCurrentMonth(),date__year=getCurrentYear()).aggregate(Sum('rupees')),
                'prevExp':getPreviousMonthdataExp(request.user.id),
                'prevTotal':getPreviousMonthdataExp(request.user.id).aggregate(Sum('rupees')),
                'data' : data
        }
        return render(request,'expenses.html',context)
    else:
        form = ExpensesForm(request.user,request.POST,request.FILES or None)

        if form.is_valid():
            data = form.save(commit=False)
            data.user_id = request.user.id
            data.save()
            return redirect('expenses')
        return render(request, 'expenses.html', {'form': form})


@login_required(login_url='login')
def category(request):

    if request.method=='GET':
        context = {

            'form':CategoryForm(),
            'cat':Category.objects.filter(user_id=request.user.id) [::-1]
        }
        return render(request,'category.html',context)
    else:
        form = CategoryForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user_id = request.user.id
            data.save()
            return redirect('category')
        return render(request,'category.html',{'form':form})

def mylogout(request):
    logout(request)
    return redirect('login')

def getCurrentMonth():
    return datetime.date.today().month


def getCurrentYear():
    return datetime.date.today().year

def getPreviousMonthdataExp(id):
    today_month = datetime.date.today().month
    today_year = datetime.date.today().year

    if today_month!= 1:
        previous_month = today_month-1
        previous_month_year = today_year

    else:
        previous_month = 12
        previous_month_year = today_year-12
    return Expenses.objects.filter(user_id=id,date__month=previous_month,date__year=previous_month_year )

def getPreviousMonthdataInc(id):
    today_month= datetime.date.today().month
    today_year = datetime.date.today().year

    if today_month!=1:
        previous_month = today_month-1
        previous_month_year = today_year

    else:
        previous_month = 12
        previous_month_year = today_year-12
    return Income.objects.filter(user_id=id,date__month=previous_month,date__year=previous_month_year)


def expenses_edit(request,id):
    data = Expenses.objects.get(pk=id)
    form = ExpensesForm(request.user,request.POST or None,request.FILES or None,instance=data)
    if form.is_valid():
        form.save()
        return redirect('expenses')

    context = {

        'form':form
    }
    return render(request,'expenses_edit.html',context)

def expenses_delete(request,id):
    exp = Expenses.objects.get(pk=id)
    exp.delete()
    return redirect('expenses')

def sum_by_categoryexp(id):
    all_category = Category.objects.filter(user_id=id,)
    category_label = []
    category_sum = []
    for c in all_category:
        t = Expenses.objects.filter(user_id=id,date__month=getCurrentMonth(),date__year=getCurrentYear(),category_id=c.id).aggregate(Sum('rupees'))
        if t['rupees__sum'] is not None:
            category_sum.append(t['rupees__sum'])
        else:
            category_sum.append(0)
        category_label.append(c.title)
    print(category_label)
    print(category_sum)

    return (list(zip(category_label,category_sum)))



def sum_by_categoryexp1(id):
    today_month = datetime.date.today().month
    today_year = datetime.date.today().year

    if today_month != 1:
        previous_month = today_month - 1
        previous_month_year = today_year

    else:
        previous_month = 12
        previous_month_year = today_year - 12


    all_category = Category.objects.filter(user_id=id,)
    category_label = []
    category_sum = []
    for c in all_category:
        t = Expenses.objects.filter(user_id=id,date__month=previous_month,date__year=previous_month_year,category_id=c.id).aggregate(Sum('rupees'))
        if t['rupees__sum'] is not None:
            category_sum.append(t['rupees__sum'])
        else:
            category_sum.append(0)
        category_label.append(c.title)
    print(category_label)
    print(category_sum)

    return (list(zip(category_label,category_sum)))



def income_edit(request,id):
    data = Income.objects.get(pk=id)
    form = IncomeForm(request.POST or None, request.FILES or None, instance=data)
    if form.is_valid():
        form.save()
        return redirect('income')

    context = {

        'form': form
    }
    return render(request, 'income_edit.html', context)




def income_delete(request,id):
    inc = Income.objects.get(pk=id)
    inc.delete()
    return redirect('income')



def category_edit(request,id):
    data = Category.objects.get(pk=id)
    form = CategoryForm(request.POST or None, request.FILES or None, instance=data)
    if form.is_valid():
        form.save()
        return redirect('category')

    context = {

        'form': form
    }
    return render(request, 'category_edit.html', context)


def category_delete(request,id):
    cat = Category.objects.get(pk=id)
    cat.delete()
    return redirect('category')



def expensesvssaving(id):
     income = Income.objects.filter(user_id=id,date__month=getCurrentMonth(),date__year=getCurrentYear()).aggregate(Sum('rupees'))
     total_income = income['rupees__sum']
     if total_income is None:
         total_income = 0

     expenses = Expenses.objects.filter(user_id=id, date__month=getCurrentMonth(),date__year=getCurrentYear()).aggregate(Sum('rupees'))
     total_expenses = expenses['rupees__sum']
     if total_expenses is None:
         total_expenses = 0

     saving = total_income-total_expenses
     print(total_expenses)
     return list(zip(['expenses','saving'],[total_expenses,saving]))







