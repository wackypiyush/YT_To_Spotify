from flask import Flask, request, redirect, session, url_for  # Import Flask modules
import os  # Import the OS module for environment variables
from spotipy import Spotify  # Import the Spotify module from Spotipy
from spotipy.oauth2 import SpotifyOAuth  # Import SpotifyOAuth for authentication
from spotipy.cache_handler import FlaskSessionCacheHandler  # Import FlaskSessionCacheHandler for caching sessions
from titles import lst  # Import the 'lst' variable from the main module

# Initialize the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)  # Set a secret key for the Flask app

# Spotify API credentials and parameters
client_id = 'c576c76565bb499cbc2a49dc8c010f18'  # Replace with your Spotify client ID
client_secret = '4373a21db1024f76bf453cec953399d3'  # Replace with your Spotify client secret
redirect_uri = 'http://localhost:5000/callback'  # Redirect URI for Spotify authorization
scope = scope = 'playlist-read-private playlist-modify-public playlist-modify-private'  # Spotify scopes

# Initialize FlaskSessionCacheHandler for caching sessions
cache_handler = FlaskSessionCacheHandler(session)
# Initialize SpotifyOAuth for Spotify authentication
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)
# Initialize the Spotify client
sp = Spotify(auth_manager=sp_oauth)

# Define the home route '/'
@app.route('/')
def home():
    # Check if the Spotify token is valid
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        # If not valid, redirect to Spotify authorization URL
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    # If valid, redirect to the 'get_playlists' route
    return redirect(url_for('get_playlists'))

# Define the callback route '/callback' for Spotify authorization callback
@app.route('/callback')
def callback():
    # Retrieve the Spotify access token from the authorization code
    sp_oauth.get_access_token(request.args['code'])
    # Redirect to the 'get_playlists' route
    return redirect(url_for('get_playlists'))

# Define the route '/get_playlists' to retrieve and display user playlists
@app.route('/get_playlists')
def get_playlists():
    # Check if the Spotify token is valid
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        # If not valid, redirect to Spotify authorization URL
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    # Get the user's playlists from Spotify
    playlists = sp.current_user_playlists()
    # Extract playlist information (name, URL, ID)
    playlists_info = [(pl['name'], pl['external_urls']['spotify'], pl['id']) for pl in playlists['items']]
    # Generate HTML for displaying playlists with an 'Add Songs' button
    playlists_html = '<br'.join([f'<a href="{url}">{name}</a> - <form method="post" action="/add_songs"><input type="hidden" name="playlist_id" value="{playlist_id}"><input type="submit" value="Add Songs"></form>' for name, url, playlist_id in playlists_info])

    return playlists_html  # Return the HTML content

# Define the route '/create_playlist' to create a new Spotify playlist
@app.route('/create_playlist')
def create_playlist():
    # Specify the desired playlist name
    playlist_name = 'My New Playlist'
    # Get the user ID from Spotify
    user_id = sp.me()['id']
    # Create a new public playlist on Spotify
    new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    # Return a message with the URL of the created playlist
    return f"Created new playlist: {new_playlist['external_urls']['spotify']}"

# Define the route '/add_songs' to add songs to a Spotify playlist
@app.route('/add_songs', methods=['POST'])
def add_songs():
    playlist_id = request.form['playlist_id']  # Get the playlist ID from the form
    songs = lst  # Use the 'lst' variable from the main module
    # Search for each song and get its URI from Spotify
    song_uris = [sp.search(q=song, type='track')['tracks']['items'][0]['uri'] for song in songs]
    # Add the songs to the specified playlist on Spotify
    sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
    return "Songs added to the playlist"  # Return a success message

# Run the Flask app in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)
