from setup import *
from spotify_handler import *  
from genius_handler import *
from langchain_handler import *




df = pd.DataFrame(columns=['Lyrics', 'Song Name','Artist'])
conn = sqlite3.connect('songs.db')

def add_to_db(lyrics, trackName, trackArtist): #add the lyrics to the pandas dataframe
    global df 
    return(df)

def add_to_sql(trackList, conn): #add the tracklist to the database
    df.to_sql('songs', conn, if_exists='append')

def read_from_sql():
    conn = sqlite3.connect('songs.db')
    df = pd.read_sql_query("SELECT * FROM songs", conn)
    conn.close()
    return(df)

