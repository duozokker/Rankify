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
 


class Song:
    def __init__(self, item: str, id: int, rank: int = 1000):
        """
        Initializes the Song object.
        
        :param item: The name of the song.
        :type item: str
        :param id: The unique identifier of the song.
        :type id: int
        :param rank: The rank of the song, defaults to 1000.
        :type rank: int
        """
        self.item = item
        self.rank = rank
        self.id = id

    def getId(self) -> int:
        """
        Returns the id of the Song.
        
        :return: The id of the song.
        :rtype: int
        """
        return self.id
    
    def getRank(self) -> int:
        """
        Returns the rank of the Song.
        
        :return: The rank of the song.
        :rtype: int
        """
        return self.rank
    
    def getItem(self) -> str:
        """
        Returns the item of the Song.
        
        :return: The name of the song.
        :rtype: str
        """
        return self.item
    
    def setRank(self, newRank: int):
        """
        Sets a new rank for the Song.
        
        :param newRank: The new rank of the song.
        :type newRank: int
        """
        self.rank = newRank
    
    def __str__(self) -> str:
        """
        Returns the string representation of the Song.
        
        :return: The name of the song.
        :rtype: str
        """
        return self.item

class Playlist:
    def __init__(self, playlistParam: list):
        """
        Initializes the Playlist object.
        
        :param playlistParam: The list of songs.
        :type playlistParam: list
        """
        self.playlist = playlistParam
    
    def get(self) -> list:
        """
        Returns the playlist.
        
        :return: The list of songs.
        :rtype: list
        """
        return self.playlist
    
    def set(self, set: list):
        """
        Sets a new playlist.
        
        :param set: The new list of songs.
        :type set: list
        """
        self.playlist = set

    def getIndex(self, i: int) -> Song:
        """
        Returns the Song at index i in the playlist.
        
        :param i: The index of the song.
        :type i: int
        :return: The song at the given index.
        :rtype: Song
        """
        return self.playlist[i]
    
    def getElo(self, i: int) -> int:
        """
        Returns the rank (Elo) of the Song at index i in the playlist.
        
        :param i: The index of the song.
        :type i: int
        :return: The rank of the song at the given index.
        :rtype: int
        """
        return self.getIndex(i).getRank()

    def sort(self):
        """
        Sorts the playlist based on the rank of the Songs.
        """
        playlist = self.playlist
        self.playlist = sorted(playlist, key=lambda playlist: -playlist.rank)
    
    def randSample(self, n: int = 2) -> list:
        """
        Returns n random indices from the playlist.
        
        :param n: The number of random indices to return, defaults to 2.
        :type n: int
        :return: The list of random indices.
        :rtype: list
        """
        return sample(range(len(self.playlist)), n)
    
    def game(self, a: int, b: int, d: str):
        """
        Plays a game between the Songs at index a and b. The winner is determined by the string d.
        
        :param a: The index of the first song.
        :type a: int
        :param b: The index of the second song.
        :type b: int
        :param d: The winner of the game.
        :type d: str
        """
        aElo = self.getIndex(a).getRank()
        bElo = self.getIndex(b).getRank()

        aElo, bElo = eloRating(aElo, bElo, d)

        self.getIndex(a).setRank(aElo)
        self.getIndex(b).setRank(bElo)

        self.sort()
    
    def __str__(self) -> str:
        """
        Returns the string representation of the Playlist.
        
        :return: The string representation of the playlist.
        :rtype: str
        """
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


 
 