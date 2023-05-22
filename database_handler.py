from setup import *
from spotify_handler import *  
from genius_handler import *
from langchain_handler import *




df = pd.DataFrame(columns=['Lyrics', 'Song Name','Artist'])

def add_to_db(lyrics, trackName, trackArtist):
    global df
    df = pd.concat([df, pd.DataFrame({'Lyrics': [lyrics], 'Song Name': [trackName], 'Artist': [trackArtist]})], ignore_index=True)
    return(df)




