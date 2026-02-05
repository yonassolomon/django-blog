from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    context={
        'title':'Home page'
    }
    return render(request,'blog/home_page.html',context)

def about_page(request):
    return HttpResponse("wellcome to about us page🫡")
