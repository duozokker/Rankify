from SpotiRank_v2 import *
from flask import Flask, render_template, redirect, url_for, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import concurrent.futures
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



def setupPlaylist (playlist_id = '57OPbzeNozOLLJ9xEUd5UD'):
    playlist = sp.playlist(playlist_id)

    # Print playlist details
    print("Playlist Name:", playlist['name'])
    print("Playlist Description:", playlist['description'])
    print("Number of Tracks:", playlist['tracks']['total'])

    tracklist = []
    tracklist_ids = []
    # Print track names
    #print("\nTrack Names:")
    for track in playlist['tracks']['items']:
        track_name = track['track']['name']
        artists = ", ".join([artist['name'] for artist in track['track']['artists']])
        #print(f"{track_name} - {artists}")
        tracklist.append(f"{track_name} - {artists}")
        tracklist_ids.append(track['track']['id'])

    #new_tracklist = tracklist, tracklist_ids
    tracklist = list(zip(tracklist, tracklist_ids))
    playlistArray = Playlist([Song(item, id) for item, id in tracklist])
    #print(playlist)

    return tracklist,playlistArray, playlist

global tracklist, playlist, spplaylist
tracklist, playlist, spplaylist = setupPlaylist()


app = Flask(__name__)

def get_album_cover(track_id, size='x'):
    track_info = sp.track(track_id)
    album_id = track_info['album']['id']
    album_data = sp.album(album_id)
    
    # Get album cover
    if size == 'small':
        cover_url = album_data['images'][2]['url']  # Get small cover
    elif size == 'medium':
        cover_url = album_data['images'][1]['url']  # Get medium cover
    else:
        cover_url = album_data['images'][0]['url']  # Get large cover

    return cover_url

def get_both_album_covers(aID, bID):
    return get_album_cover(aID), get_album_cover( bID)

@app.route('/')
def index():
    aIndex, bIndex = playlist.randSample()
    aName, bName = str(playlist.getIndex(aIndex)), str(playlist.getIndex(bIndex))
    #aElo, bElo = playlist.getElo(aIndex), playlist.getElo(bIndex)
    aID, bID = playlist.getIndex(aIndex).getId(), playlist.getIndex(bIndex).getId()

    # Get album covers
    album1, album2 = get_both_album_covers(aID, bID)

    print(album1, album2)

    return render_template('index.html', album1=album1, album2=album2, aName=aName, bName=bName, aIndex=aIndex, bIndex=bIndex, playlistName = spplaylist['name'], playlistDescription = spplaylist['description'], playlistLength = spplaylist['tracks']['total'])

@app.route('/album_click/<aIndex>/<bIndex>/<winner>')
def album_click(aIndex, bIndex, winner):
    #print(aIndex, bIndex, winner)
    playlist.game(int(aIndex), int(bIndex), winner)
    return redirect(url_for('index'))

def fetch_album_data(track_id):
    track_info = sp.track(track_id)
    album_id = track_info['album']['id']
    return sp.album(album_id)

def get_album_covers(track_ids):
    album_covers = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_track_id = {executor.submit(fetch_album_data, track_id): track_id for track_id in track_ids}
        for future in concurrent.futures.as_completed(future_to_track_id):
            album_data = future.result()
            if album_data['images'] and len(album_data['images']) > 2:
                cover_url = album_data['images'][2]['url']  # Get small cover
            elif album_data['images']:
                cover_url = album_data['images'][0]['url']  # Get large cover as fallback
            else:
                cover_url = None  # No cover available
            album_covers.append(cover_url)
    return album_covers
    
    return album_covers

@app.route('/handle_playlist_link')
def handle_playlist_link():
    playlist_link = request.args.get('playlistLink')
    playlist_id = playlist_link[34:-20]
    global tracklist, playlist, spplaylist
    tracklist, playlist, spplaylist = setupPlaylist(playlist_id)
    return redirect(url_for('index'))

@app.route('/playlist')
def playlist_route():
    # Sort the playlist first
    playlist.sort()
    snapshot = playlist.get()

    # Get album IDs
    album_ids = [song.getId() for song in snapshot]

    # Fetch album covers
    album_covers = get_album_covers(album_ids)

    # Create a list of dictionaries, where each dictionary contains the data for one song
    songs = []
    for i, song in enumerate(snapshot):
        song_data = {
            'name': str(song),
            'elo': playlist.getElo(i),
            'cover_url': album_covers[i]
        }
        songs.append(song_data)

    return render_template('playlist.html', songs=songs)


if __name__ == '__main__':
    app.run(debug=True)