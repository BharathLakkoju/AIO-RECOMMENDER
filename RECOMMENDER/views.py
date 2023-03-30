from django.shortcuts import render
from django.views import View
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tmdbsimple as tmdb

# Create your views here.


class index(View):
    def get(self, request):
        return render(request, 'index.html')

"""API KEYS"""
SPOTIPY_CLIENT_ID = '3f107fdeb1044267abc8f8e11c7531d1'
SPOTIPY_CLIENT_SECRET = '614e983b1f3d416ab4c52c2fd5a8d2d3'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET))
tmdb.API_KEY = '4772c7ae6311512b78faba06a7dd17fb'



class recommender(View):
    def get(self, request):
        return render(request, 'recommender.html')
    
    def post(self, request):
        """Get movie name"""
        movie_name=request.POST.get('movie-name')
        """Get movie id"""
        search = tmdb.Search()
        response = search.movie(query=movie_name)
        def get_movie_id(movie_name):
            if response['results']:
                return response['results'][0]['id']
            return response
        get_movie_id(movie_name)
        """Get recommended movies"""
        def get_recommended_movies(movie_id):
            if movie_id:
                movie = tmdb.Movies(movie_id)
                recommendations = movie.recommendations()
                if recommendations:
                    return recommendations['results'][:10]
            return []
        """Assign recommendations"""
        movie_id = get_movie_id(movie_name)
        movies = get_recommended_movies(movie_id)
        if len(movies)==0:
            movies = response['results'][:10]
        search_result = response['results'][0]
        """songs"""
        
        # results = sp.search(q=movie_name, limit=10, type='track')
        songs = []
        # for track in results['tracks']['items']:
        #     songs.append({
        #         'name': track['name'],
        #         'artist': track['artists'][0]['name'],
        #         'release_date': track['album']['release_date'],
        #         'poster': track['album']['images'][0]['url'],
        #         'uri': track['external_urls']['spotify'],
        #     })

        results = sp.search(q=movie_name,limit=10, type='album')
        album_id = results['albums']['items'][0]['id']
        tracks = sp.album_tracks(album_id)['items']
        track_id = tracks[0]['id']
        track = sp.track(track_id)
        artist_id = track['artists'][0]['id']
        recommendations = sp.recommendations(seed_tracks=[track_id],seed_artists=[artist_id])
        res = recommendations['tracks'][:10]
        for track in res:
            if track['name']!="":
                songs.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'release_date': track['album']['release_date'],
                    'uri': track['external_urls']['spotify'],
                    'poster': track['album']['images'][0]['url'],
                })
        return render(request, 'recommender.html', {'movies': movies, 'songs': songs, 'search': search_result})

