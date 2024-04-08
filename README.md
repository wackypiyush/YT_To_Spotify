# YouTube to Spotify Playlist Sync
This project allows you to sync a YouTube playlist with a Spotify playlist. It retrieves the list of songs from a specified YouTube playlist and adds those songs to a new or existing Spotify playlist.

## Getting Started

### Prerequisites
1. Python 3.x installed on your system.
2. The required Python packages listed in requirements.txt.
3. YouTube Data API key.
4. Spotify API credentials (client ID and client secret).

## Installation
1. Clone this repository to your local machine.
2. Install the required packages using _pip install -r requirements.txt_.
3. Replace your YouTube API key, Spotify client ID, and client secret.
4. Can get you Google API by following https://blog.hubspot.com/website/how-to-get-youtube-api-key
5. Can get your Spotify credentials using Spotify Developers.

## Usage
1. Run _titles.py_ to retrieve titles of videos from a YouTube playlist.
> URL of playlist looks like this: https://www.youtube.com/watch?v=OW6yRfdrfgU&list=PL13f76aevJUXNvJU3Bbtymq3btS6TaBma
You need to pass the list parameter of this link to the playlist_id.
2. Run the Flask app by executing flask run in the terminal or _python spotify.py_
> Access the app in your browser (usually at http://localhost:5000/).

## Features
1. Retrieve song titles from a YouTube playlist.
2. Authenticate with Spotify to access user playlists.
3. Create a new Spotify playlist and add videos to it.
4. Display user playlists and allow adding songs to selected playlists.

## Contributing
Contributions are welcome! Please follow the standard guidelines.

### Acknowledgments
Thanks to Google and Spotify for their APIs.
Inspiration from real life problem!
