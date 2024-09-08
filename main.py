import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
date = input("in which year you want to time travel enter the date in YYYY-MM-DD format\n")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"
playlist_id = os.environ.get("playlist_id")
SPOTIFY_ENDPOINT = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
SPOTIFY_URI = f"spotify:track:{playlist_id}"

response = requests.get(URL)
html_content = response.text
soup = BeautifulSoup(html_content, "html.parser")
top_100_songs = soup.select("li h3")
songs_list = [song.getText().strip() for song in top_100_songs]
sliced_list = songs_list[:100]
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="Avinash Gembali",
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in sliced_list:
    result = sp.search(q=song, type="track", limit=1)
    if result['tracks']['items']:
        song_uri = result['tracks']['items'][0]['uri']
        song_uris.append(song_uri)
        print(f"Found URI for {song}: {song_uri}")
    else:
        print(f"No result found for {song}")


playlist_name = f"{date} Billboard 100"

new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
playlist_id = new_playlist["id"]
if song_uris:
    sp.playlist_add_items(playlist_id, song_uris)
    print(f"Added {len(song_uris)} songs to the playlist '{playlist_name}'")
else:
    print("No songs to add to the playlist.")