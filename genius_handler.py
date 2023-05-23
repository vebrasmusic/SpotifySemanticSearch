from setup import *
from spotify_handler import *

genius = Genius(token)
genius = lyricsgenius.Genius("my_token")  # replace with your token
genius.verbose = False


def sanitize_filename(name): #this is to make sure the file name is valid
    for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
        name = name.replace(char, '_')
    return name

#custom get song lyrics function, with timeout behavior
def get_song_lyrics(title, artist, max_retries=5, delay_between_retries=10):
    for attempt in range(max_retries):
        try:
            song = genius.search_song(title=title, artist=artist) #search for the song
            if song is not None:
                return song
            else:
                #print(f"No lyrics found for {title} by {artist}.")
                return None
        except Timeout:
            if attempt < max_retries - 1:  # it's not the last attempt
                print(f"Timeout occurred when getting lyrics for {title} by {artist}. "
                      f"Waiting {delay_between_retries} seconds before retrying...")
                time.sleep(delay_between_retries)
                continue
            else:  # it's the last attempt
                print(f"Still experiencing timeouts after {max_retries} attempts. "
                      f"Giving up on getting lyrics for {title} by {artist}.")
                return None
        except Exception as e:
            #print(f"An error occurred: {e}")
            return None
        

def lyric_saving(song_name_array): #this is the function that will save the lyrics to a file
    title = sanitize_filename(song_name_array[0])
    artist = sanitize_filename(song_name_array[1])
    song = get_song_lyrics(title, artist,5,10)
    if song != None and "[Verse" in song.lyrics:
        lyrics = song.lyrics
        return lyrics
        #with open('lyrics/%s_%s.txt'%(title,artist), 'w') as f:
        #    f.write(lyrics)

