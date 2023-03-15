from django.shortcuts import render
from django.views import View
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tmdbv3api import TMDb
from tmdbv3api import Movie

# Create your views here.


class index(View):
    def get(self, request):
        return render(request, 'index.html')

client_id = '3f107fdeb1044267abc8f8e11c7531d1'
client_secret = '614e983b1f3d416ab4c52c2fd5a8d2d3'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

tmdb = TMDb()
tmdb.api_key = '4772c7ae6311512b78faba06a7dd17fb'

class recommend(View):
    def get(self, request):
        return render(request, 'rec.html')
    
    def post(self, request):
        mname=request.POST.get('movie-name')
        movie = Movie()
        search_result = movie.search(mname)
        if len(search_result) > 0:
            movie_id = search_result[0].id
            recommended_movies = movie.recommendations(movie_id)[:10]
        if len(recommended_movies) == 0:
            recommended_movies = search_result[:10]
        # return render(request, 'rec.html')    
        
        results = sp.search(q=mname, type='track', limit=10)
        if len(results['tracks']['items']) > 0:
            track_id = results['tracks']['items'][0]['id']
            recommended_songs = sp.recommendations(seed_tracks=[track_id])['tracks'][:10]
        return render(request, 'rec.html', {'recommended_movies': recommended_movies, 'recommended_songs': recommended_songs})

