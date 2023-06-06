# Spotify Semantic Search

Spotify Semantic Search is an innovative project aimed at enhancing the music discovery experience. Leveraging powerful language models, it allows users to find songs on Spotify that semantically resonate with their input.

## Overview

The project is composed of several Python scripts and a Jupyter notebook, each serving a specific role:

- `setup.py`: This script is used for setting up the environment, including installing necessary dependencies.

- `main.ipynb`: This Jupyter notebook serves as the driver of the project, coordinating the different components and providing an interactive interface for testing and development.

- `genius_handler.py`: This script is responsible for interfacing with the Genius API to gather lyrics for songs.

- `spotify_handler.py`: This script handles interactions with the Spotify API, fetching song metadata.

- `database_handler.py`: This script manages interactions with Pinecone, storing and retrieving vector representations of songs.

- `langchain_handler.py`: This script interfaces with Langchain or GPT-4, transforming user input into a semantic vector representation.

The general flow of the project is as follows:

1. The `spotify_handler.py` and `genius_handler.py` scripts gather song metadata and lyrics, respectively.
2. This data is fed into OpenAI's Ada (with plans to upgrade to BERT) to convert it into a vector representation.
3. The vector is stored in Pinecone using `database_handler.py`.
4. User input is processed through `langchain_handler.py` to generate a semantic vector.
5. This vector is compared with the song vectors in Pinecone, and the top 10 closest matches are returned as recommendations.

## Getting Started

### Prerequisites

Please ensure you have the following installed:

- Python 3.7+
- Pinecone
- OpenAI's Ada or GPT-4
- Spotify API Key
- Genius API Key

### Installation

1. Clone the repo:
```
git clone https://github.com/your_username/Spotify-Semantic-Search.git
```
2. Install the necessary dependencies:
```
pip install -r requirements.txt
```
3. Run the setup script:
```
python setup.py
```
4. Launch the Jupyter notebook:
```
jupyter notebook main.ipynb
```
Happy music hunting!


