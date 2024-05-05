# Rankify

Rankify is a fun game that allows you to compare two songs from a given Spotify playlist and choose which one you like more. It's similar to the "Higher Lower" game where one must guess which topic has more search results.

## Setup

1. Clone this repository to your local machine.
2. Install the required Python packages by running `pip install -r requirements.txt`.
3. You need to have Spotify API keys to run this program. If you don't have them, you can get them from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
4. Once you have the API keys, create a ``.env`` file in the root directory of the project.
5. Add your Spotify `CLIENT_ID` and `CLIENT_SECRET` to the ``.env`` file like this:

```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

## Running the Game

1. Run the ``run.py`` script to start the game:

```sh
python run.py
```

2. The game will fetch a playlist from Spotify and randomly select two songs.
3. You will be asked to choose which song you like more.
4. The game continues until you decide to stop.

Enjoy the game and happy ranking!