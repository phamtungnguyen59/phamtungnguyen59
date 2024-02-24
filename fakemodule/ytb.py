
import spotipy,json,urllib.parse,re
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import parse_qs, urlparse

with open('jsonfile/config.json', 'r') as f:
    Config = json.load(f)
client_id= Config['client_id']
client_secret= Config['client_secret']
sp = spotipy.Spotify(auth_manager= SpotifyClientCredentials(client_id=client_id,client_secret=client_secret))

def get_playlist_id(playlist_url):
    # Normal playlists start with PL, Mixes start with RD + first video ID,
    # Liked videos start with LL, Uploads start with UU,
    # Favorites lists start with FL
    # Album playlists start with OL
    idregx = re.compile(r'((?:RD|PL|LL|UU|FL|OL)[-_0-9a-zA-Z]+)$')

    playlist_id = None
    if idregx.match(playlist_url):
        playlist_id = playlist_url  # ID of video

    if '://' not in playlist_url:
        playlist_url = '//' + playlist_url
    parsedurl = urlparse(playlist_url)
    if parsedurl.netloc in ('youtube.com', 'www.youtube.com'):
        query = parse_qs(parsedurl.query)
        if 'list' in query and idregx.match(query['list'][0]):
            playlist_id = query['list'][0]
    
    return playlist_id

def getidspo(value):
    query = urllib.parse.urlparse(value)
    if query.hostname in ('open.spotify.com'):
        if query.path[:10] == '/playlist/':
            return query.path.split('/')[2]
        if query.path[:7] == '/track/':
            return query.path.split('/')[2]
        if query.path[:7] == '/album/':
            return query.path.split('/')[2]

    return None

def songbyid(id):
    meta = sp.track(id)
    name = meta['name']
    artist=meta['artists'][0]['name']
    return {
        'name':name,
        'artists':artist}
def ambum(id):
    ids = []
    item = sp.album(id)
    for itema in item['tracks']['items']:
        ids.append(itema['id'])
    return ids

def playlist(id):
    ids = []
    item = sp.playlist(id)
    for itema in item['tracks']['items']:
        track = itema['track']
        ids.append(track['id'])
    return ids
