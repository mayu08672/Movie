from django.contrib.auth import logout
from django.shortcuts import redirect

def my_logout(request):
    logout(request)
    return redirect("/")
