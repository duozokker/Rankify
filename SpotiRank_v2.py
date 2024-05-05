import math
from random import randint, sample



##Get songs
    


# Elo Rating

# Function to calculate the Probability
 
 
def probability(rating1, rating2):
 
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))
 
 
# Function to calculate Elo rating
# K is a constant.
# d determines whether
# Player A wins or Player B. 
# d= "a" => player A wins

def eloRating(Ra, Rb, d, K = 100):
 
    # To calculate the Winning
    # Probability of Player B
    Pb = probability(Ra, Rb)
 
    # To calculate the Winning
    # Probability of Player A
    Pa = probability(Rb, Ra)
 
    # Case -1 When Player A wins
    # Updating the Elo Ratings
    if (d == "a"):
        Ra = Ra + K * (1 - Pa)
        Rb = Rb + K * (0 - Pb)
 
    # Case -2 When Player B wins
    # Updating the Elo Ratings
    else:
        Ra = Ra + K * (0 - Pa)
        Rb = Rb + K * (1 - Pb)
 
    print("Updated Ratings:-")
    print("Ra =", round(Ra, 6), " Rb =", round(Rb, 6))
    return round(Ra, 6), round(Rb, 6)
 


#Structure
class Song:
    def __init__(self, item, id, rank=1000):
        self.item = item
        self.rank = rank
        self.id = id

    def getId(self):
        return self.id
    
    def getRank(self):
        return self.rank
    
    def getItem(self):
        return self.item
    
    def setRank(self, newRank):
        self.rank = newRank
    
    def __str__(self) -> str:
        return self.item # + self.id

class Playlist:
    def __init__(self, playlistParam):
        self.playlist = playlistParam
    
    def get(self):
        return self.playlist
    
    def set(self, set):
        self.playlist = set

    # get Item at index i
    def getIndex(self, i):
        return self.playlist[i]
    
    # give Index, get Elo
    def getElo(self, i):
        return self.getIndex(i).getRank()

    def sort(self):
        playlist = self.playlist
        self.playlist = sorted(playlist, key=lambda playlist: -playlist.rank) #, reverse=True)
    
    # return 2 indices 
    def randSample(self, n=2):
        return sample(range(len(self.playlist)), n)
    
    # a - player a index
    # b - player b index
    # d - winner as String
    def game(self, a, b, d):
        aElo = self.getIndex(a).getRank()
        bElo = self.getIndex(b).getRank()

        aElo, bElo = eloRating(aElo, bElo, d)

        self.getIndex(a).setRank(aElo)
        self.getIndex(b).setRank(bElo)

        self.sort()

        #return aElo, bElo
    
    def __str__(self) -> str:
        rstring = ""
        for i in self.playlist:
            rstring += str(i) + f" - {i.getRank()}\n"
        return rstring



# Game 

# Setup Classes
# load tracklist into Class


def __main__():
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import os
    from dotenv import load_dotenv


    # Replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual credentials
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')


    # Authenticate with Spotify API
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Replace 'USERNAME' and 'PLAYLIST_ID' with the username and playlist ID you want to retrieve
    username = 'USERNAME'
    playlist_id = '57OPbzeNozOLLJ9xEUd5UD'

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


    playlist = Playlist([Song(item, id) for item, id in tracklist])
    print(playlist)
    #CLI game test
    import sys
    while True:
            try:
                aIndex, bIndex = playlist.randSample()
                aName, bName = str(playlist.getIndex(aIndex)), str(playlist.getIndex(bIndex))
                aElo, bElo = playlist.getElo(aIndex), playlist.getElo(bIndex)
                
                winner = input(f"{aElo} [a] {aName}  ## VS ## {bName} [b] {bElo}")

                playlist.game(aIndex, bIndex, winner)

                print(playlist)

            except KeyboardInterrupt:
                playlist.sort()
                print(playlist)
                sys.exit(0)


 
 