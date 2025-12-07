from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .forms import RegisterForm, UpdateForm
from django.contrib.auth.models import User

def register(request):
    if request.method == "POST":
       form = RegisterForm(request.POST)
       if form.Is_valid():
           form.save()
           username = form.cleaned_data.get('username')
           messages.success(request, f"Account created for {username}. You can now log in.") 
           return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, "Your profile was updated.")
            return redirect('profile')
    else:
        u_form = UpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }
    return render(request, 'blog/profile.html', context)


