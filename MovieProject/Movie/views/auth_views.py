from django.http import HttpResponse
from django.shortcuts import render




def create_account(request):
    return render(request, 'create_account.html')



def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    return render(request, 'logout.html')

def latest_movies(request):
    return render(request, 'latest_movies.html')

def movie_detail(request, movie_id):
    return render(request, 'movie_detail.html', {'movie_id': movie_id})
def my_subscriptions(request):
    return render(request, 'my_subscriptions.html')

def tmdb_search(request):
        return HttpResponse("TMDB Search API Endpoint")
    

def tmdb_discover(request):
    return HttpResponse("TMDB Discover API Endpoint")

def collection_page(request, collection_id):
    return render(request, "collection_detail.html", {"collection_id": collection_id})

def person_detail(request, person_id):
    return render(request, 'person_detail.html', {'person_id': person_id})

def tmdb_movie_detail(request, id):
    return HttpResponse(f"TMDB Movie Detail API Endpoint for movie ID: {id}")

def tmdb_tv_detail(request, id):
    return HttpResponse(f"TMDB TV Detail API Endpoint for TV ID: {id}")
def collection_detail(request, collection_id):
    return HttpResponse(f"Collection Detail API Endpoint for collection ID: {collection_id}")
def tmdb_person_detail(request, id):
    return HttpResponse(f"TMDB Person Detail API Endpoint for person ID: {id}")

def tmdb_person_works(request, id):
    return HttpResponse(f"TMDB Person Works API Endpoint for person ID: {id}")


