embeddings = OpenAIEmbeddings(openai_api_key = openai_api_key)
llm = OpenAI(temperature=0)
chain = load_summarize_chain(llm, chain_type="stuff")

