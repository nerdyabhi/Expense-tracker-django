from django.shortcuts import render , redirect , HttpResponse
from expense_tracker.models import *
from django.contrib import messages
from django.db.models import Sum

# Create your views here.
def register(request):
    return render(request , 'register.html')

def regi(request):
    name = request.GET['user_name']
    email = request.GET['user_email']
    password = request.GET['user_pass']

    if user.objects.filter(email= email).exists():
        data = {'email' :email , 'message' : "User Already exists Please Login "}
        return render(request , 'login.html' , {'data' : data})

    u = user()
    u.name = name 
    u.email = email
    u.password = password
    u.save()

    k = user.objects.get(email = email)
    exp = expense.objects.filter(user = k)
    return render(request, 'welcome.html' , {'u':k , 'expense' :exp , 'total' :0} )

def login(request):
    return render(request , 'login.html')

def logi(request):
    email = request.GET['user_email']
    password = request.GET['user_pass']
    if(user.objects.filter(email = email , password = password)):
        u = user.objects.get(email = email)
        exp = expense.objects.filter(user  = u)
        total_expense = expense.objects.filter(user=u).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        return render(request, 'welcome.html' , {'u' :u, 'expense':exp , 'total':total_expense})
    

    data = {'message' : "wrong pass or no user exists"}
    return render(request , 'login.html' , {'data' : data } )

def show(request ):
    u = user.objects.all()
    return render(request , 'show.html' , {'db':u})


def addTransaction(request):
    email = request.GET['email']
    description = request.GET['expense_name']
    amount = request.GET['amount']

    u = user.objects.get(email = email)

    exp = expense()
    exp.expense_name = description
    exp.amount = amount
    exp.user = u
    exp.save()
    user_obj = user.objects.get(email = email)
    db = expense.objects.filter(user = user_obj).values()
    total_expense = expense.objects.filter(user=user_obj).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    return render(request, 'welcome.html', {'u': user_obj, 'expense': db, 'total': total_expense})