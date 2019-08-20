from django.shortcuts import render

def home(request):
    context = {'a':10 ,'b':20}
    return render(request,'index.html',context)

def signin(request):
    return render(request,'signin.html')

