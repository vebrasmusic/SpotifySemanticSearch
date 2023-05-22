from setup import *
from spotify_handler import *
from genius_handler import *   

embeddings = OpenAIEmbeddings(openai_api_key = openai_api_key)
llm = OpenAI(temperature=0) #temperature is the creativity of the AI, 0 is the most creative, 1 is the least creative
chain = load_summarize_chain(llm, chain_type="stuff")





