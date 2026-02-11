from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

from django.contrib.auth.decorators import login_required

@login_required  # ← REQUIRE LOGIN FOR HOMEPAGE TOO
def homepage(request):
    context = {
        'title': 'Private Blog Home'
    }
    return render(request, 'blog/home_page.html', context)

def about_page(request):
    return HttpResponse("wellcome to about us page🫡")

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            messages.success(request, f"🎉 Welcome {user.username}! Your account has been created.")
            return redirect('homepage')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})