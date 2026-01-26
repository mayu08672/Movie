from django.http import HttpResponse
from django.shortcuts import render




def create_account(request):
    return render(request, 'create_account.html')



def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    return render(request, 'logout.html')

def latest_movies(request):
    return render(request, 'latest.html')

def movie_detail(request, movie_id):
    return render(request, 'movie_detail.html', {'movie_id': movie_id})
def my_subscriptions(request):
    return render(request, 'my_subscriptions.html')