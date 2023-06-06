from setup import *
from genius_handler import *   
from database_handler import *
from concurrent.futures import ThreadPoolExecutor, as_completed



#Spotify Handling, where we get the 100 sorted, random songs with lyrics:

# need to add song length detection, nothing over 6 mins.

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id='36c36f81c0ff4b9da4cdbb44d12de650', client_secret='4ecf40e8b9f5443bae664b740a319465')
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

logging.getLogger('spotipy.client').setLevel(logging.ERROR)

def get_random_search(): #this part basically picks random characters from the list of all characters and puts them in a string
    # A list of all characters that can be chosen.
    characters = string.ascii_lowercase

    # Gets a random character from the characters string.
    random_character = random.choice(characters) #this is the random character that will be used to search for songs
    random_search = ''

    # Places the wildcard character at the beginning, or both beginning and end, randomly.
    switch = random.randint(0, 1)
    if switch == 0:
        random_search = random_character + '%'
    elif switch == 1: 
        random_search = '%' + random_character + '%' 

    return random_search #this is the string that will be used to search for songs


def spotify_query(query_offset):
    try:
        ranNum = random.randint(0,query_offset) # make sure the offset is a random one so there's never repeats, and they aren't all super pop. new.
        query = get_random_search() #use the function to get a random search on a letter, ie. e% so any song that starts with that letter
        track = sp.search(query, limit=1, offset = ranNum, type='track') #query spotify
        trackURI = track['tracks']['items'][0]['uri']
        trackURI = trackURI.replace('spotify:album:', '')
        trackName = track['tracks']['items'][0]['name']
        trackArtist = track['tracks']['items'][0]['artists'][0]['name']
        audio_features = sp.audio_features(trackURI)
        return trackName, trackArtist, audio_features
    except spotipy.SpotifyException as e:
            if e.http_status == 429:
                # If we're being rate limited, wait for a bit before retrying
                print("Rate limited. Waiting...")
                time.sleep(20)  # Wait for 20 seconds
                return spotify_query(query_offset)
            else:
                # For any other error, re-raise the exception
                raise e

def get_instrumentalness(audio_features):
    #Return the instrumentalness of a track, or None if not available.
    if audio_features and len(audio_features) > 0:
        instrumentalness = audio_features[0]['instrumentalness']
        return instrumentalness
    else:
        return None


def fetch_track_data(query_offset):
    try:
        trackName, trackArtist, audio_features = spotify_query(query_offset)  # get the song name, artist, and audio features from a randomized spotify search

         # If any of the values is None, return None
        if trackName is None or trackArtist is None or audio_features is None:
            return None
        
        instrumentalness = get_instrumentalness(audio_features)
        if instrumentalness is not None or instrumentalness > 0.5:
            song_name_array = [trackName, trackArtist]
            lyrics = lyric_saving(song_name_array) #get the lyrics from genius, if they exist
            audio_features_dict = {
                'danceability': audio_features[0]['danceability'],
                'energy': audio_features[0]['energy'],
                'key': audio_features[0]['key'],
                'loudness': audio_features[0]['loudness'],
                'mode': audio_features[0]['mode'],
                'speechiness': audio_features[0]['speechiness'],
                'acousticness': audio_features[0]['acousticness'],
                'instrumentalness': audio_features[0]['instrumentalness'],
                'liveness': audio_features[0]['liveness'],
                'valence': audio_features[0]['valence'],
                'tempo': audio_features[0]['tempo'],
                'duration_ms': audio_features[0]['duration_ms'],
                'time_signature': audio_features[0]['time_signature']
                                }
            return lyrics, trackName, trackArtist, audio_features_dict
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def build_track_list(songNumber, query_offset, max_workers):
    trackNumber = 0
    pbar = tqdm(total=songNumber, dynamic_ncols=True)

    with ThreadPoolExecutor(max_workers=max_workers) as executor: #this is the multithreading part, it's a lot faster than doing it sequentially
        while trackNumber < songNumber:
            future_to_lyrics = {executor.submit(fetch_track_data, query_offset): offset for offset in range(max_workers)}
            for future in as_completed(future_to_lyrics):
                if trackNumber >= songNumber:
                    break
                result = future.result()
                if result is not None and result[0] is not None: #if the lyrics exist, add them to the database
                    lyrics, trackName, trackArtist, audio_features = future.result()
                    df = add_to_db(lyrics, trackName, trackArtist, audio_features['danceability'], audio_features['energy'], audio_features['key'], audio_features['loudness'], audio_features['mode'], audio_features['speechiness'], audio_features['acousticness'], audio_features['instrumentalness'], audio_features['liveness'], audio_features['valence'], audio_features['tempo'], audio_features['duration_ms'], audio_features['time_signature'])
                    with pbar.external_write_mode():
                        pbar.update(1)
                    trackNumber += 1
                    print(trackNumber)

    add_to_sql(df, conn) #add the songs to the database


