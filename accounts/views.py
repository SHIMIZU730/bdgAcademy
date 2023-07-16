from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import CustomUser

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView

class EmailUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

def signup(request):
    if request.method == "POST":
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("devapp:index")
    else:
        form = EmailUserCreationForm()
    return render(request, "signup.html", {"form": form})
    

class CustomLoginView(LoginView):
    template_name = 'login.html'


# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('devapp:index')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})
    