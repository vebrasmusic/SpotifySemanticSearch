# Global imports for main script
from tqdm import tnrange, tqdm_notebook, tqdm
from time import sleep
from lyricsgenius import Genius
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# Importing the libraries
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import DeepLake
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from langchain.vectorstores import Pinecone

import random
import string

import time
import lyricsgenius
from requests.exceptions import Timeout

import pinecone
from langchain.chains.summarize import load_summarize_chain

#get my secret sauce variables
from dotenv import load_dotenv
import os
load_dotenv() 

from concurrent.futures import ThreadPoolExecutor


PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET=os.getenv('SPOTIFY_CLIENT_SECRET')
token = os.getenv('GENIUS_ACCESS_TOKEN')