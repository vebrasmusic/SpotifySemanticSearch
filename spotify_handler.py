from setup import *
from genius_handler import *   


#Spotify Handling, where we get the 100 sorted, random songs with lyrics:

# need to add song length detection, nothing over 6 mins.

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id='36c36f81c0ff4b9da4cdbb44d12de650', client_secret='4ecf40e8b9f5443bae664b740a319465')
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)



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
    ranNum = random.randint(0,query_offset) # make sure the offset is a random one so there's never repeats, and they aren't all super pop. new.
    query = get_random_search() #use the function to get a random search on a letter, ie. e% so any song that starts with that letter
    track = sp.search(query, limit=1, offset = ranNum, type='track') #query spotify
    trackURI = track['tracks']['items'][0]['uri']
    trackURI = trackURI.replace('spotify:album:', '')
    trackName = track['tracks']['items'][0]['name']
    trackArtist = track['tracks']['items'][0]['artists'][0]['name']
    audio_features = sp.audio_features(trackURI)
    return trackName, trackArtist, audio_features

def get_instrumentalness(audio_features):
    #Return the instrumentalness of a track, or None if not available.
    if audio_features and len(audio_features) > 0:
        instrumentalness = audio_features[0]['instrumentalness']
        return instrumentalness
    else:
        return None


def build_track_list(songNumber, query_offset):
    trackList = []
    pbar = tqdm(total=songNumber)  # progress bar init

    while len(trackList) <= songNumber:
        try:
            trackName, trackArtist, audio_features = spotify_query(query_offset)  # get the song name, artist, and audio features from a randomized spotify search

            instrumentalness = get_instrumentalness(audio_features)
            if instrumentalness is None or instrumentalness > 0.5:
                sleep(0.1)
                pbar.update(1)
                song_name_array = [trackName, trackArtist]
                lyrics = lyric_saving(song_name_array) #get the lyrics from genius, if they exist
                trackList.append(lyrics)
            else:
                continue
        except Exception as e:
            print(f"Error: {e}")
            continue

    return trackList

def fetch_track_data(query_offset):
    try:
        trackName, trackArtist, audio_features = spotify_query(query_offset)  # get the song name, artist, and audio features from a randomized spotify search

        instrumentalness = get_instrumentalness(audio_features)
        if instrumentalness is None or instrumentalness > 0.5:
            song_name_array = [trackName, trackArtist]
            lyrics = lyric_saving(song_name_array) #get the lyrics from genius, if they exist
            return lyrics
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def build_track_list(songNumber, query_offset):
    trackList = []
    pbar = tqdm(total=songNumber)  # progress bar init

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_lyrics = {executor.submit(fetch_track_data, offset): offset for offset in range(query_offset, query_offset + songNumber)}
        for future in concurrent.futures.as_completed(future_to_lyrics):
            lyrics = future.result()
            if lyrics is not None:
                trackList.append(lyrics)
                pbar.update(1)

    return trackList

