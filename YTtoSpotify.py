### Python Script

from apiclient.discovery import build
import csv
import spotipy
import spotipy.util as util
import sys

# Max number of titles to get from each channel
MAX_RESULT = 30

# Spotify credentials
SPOTIFY_USERNAME = 'aljiadct4y4ikpszxg9is314q'
CLIENT_ID = '7d26e4efb2ca4af0bdb111be87f7b0c3'
CLIENT_SECRET = '3d4d66b9c20d462dbd79f1a0c83b2c8c'
Scope = 'playlist-modify-private'

# Private Spotify Playlist which will get the new tracks
YOUTUBE_PLAYLIST_ID = 'spotify:playlist:4Aa78fqo7uvtDbXveHREVu'

# Youtube credentials
API_KEY = 'AIzaSyBfaFz7oUSXXwkOLaQT0JQ1EWAh5XwRjVI'

# Add channel usernames from Youtube in this list
CHANNEL_USERNAMES = ['majesticcasual']  #majestic casual's youtube channel
# Add channel IDs from Youtube in this Dictionary like {'channelName' : 'channelID'}
CHANNEL_IDS = {}

# Words to delete from the fetched title name from Youtube
IGNORE = ['(', '[', ' x', ')', ']', '&', 'lyrics', 'lyric',
          'video', '/', ' proximity', ' ft', '.', ' edit', ' feat', ' vs', ',']


# returns youtube client object
def init_youtube_client():
    try:
        print('Initialising Youtube Client....')
        client = build('youtube', 'v3', developerKey=API_KEY)
        print('\nClient initialised!\n')
        return client
    except:
        sys.exit('\nError initialising Youtube Client!\n')


# for channel username
def username_req(client, channel_username):
    req = client.channels().list(part='contentDetails', forUsername=channel_username)
    return req


# for channel id
def id_req(client, channel_id):
    req = client.channels().list(part='contentDetails',
                                 id=channel_id)
    return req


# Takes a request object and youtube client object as input and returns a list of unfiltered titles of a channel
def get_channel_uploads(req, youtube):
    print("\nGetting Channel's uploads...")
    r = req.execute()
    channel_uploads_id = r['items'][-1]['contentDetails']['relatedPlaylists']['uploads']
    req = youtube.playlistItems().list(
        part='snippet', playlistId=channel_uploads_id, maxResults=MAX_RESULT)
    playlist = req.execute()
    videos_list = playlist['items']
    return videos_list


# Takes unfiltered list of channel's titles and returns a filtered list
def filter_titles(videos_list):
    print('Filtering titles...')
    titles = []
    for video in videos_list:
        title = (video['snippet']['title']).lower()
        for ch in IGNORE:
            if ch in title:
                title = title.replace(ch, '')
        artist = (title.rsplit('-')[0]).strip()
        track = (title[len(artist) + 2:]).strip()
        title = (artist + ' ' + track).strip()
        titles.append(title)
    return titles
