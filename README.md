# LangChainCookBook
Work related to Langchain and OpenAI




# Installation Instructions:
    - pip install -r requirements.txt
    - Please create an environment file (name = ".env") with the content from sample.env
# Command to start the project:

    - streamlit run bookReaderUI.py
    or
    - python3 -m streamlit run bookReaderUI.py

# User Guide:
- Review the UI_sequence.jpg for quick user guide.
- This is a RAG application that is implemented as a ChatBot.
- This RAG application uses streamlit as User Interface for Chat Bot interface.
- User copy pastes an article that is written after 2022. Since That is the last year until ChatGPT is trained with internet datasets.
- Everytime Chat Bot recieves a URL as input then the following steps are exectued: 
    - The RAG converts HTML to Text using HTML2Text library.
    - Creat Chunks using DocumentTransformer RecursiveCharacterTextSplitter with chunk_size=1000, chunk_overlap=0
    - Create Embeddings using ChatGPT. 
    - Use ChromaDB to save Chunks as vectors to ChromaDB
    - ChromaDB has 3 parts.
        - ChromaDB docker container as a server.
        - ChromaDB server has no User Interface.
        - ChromaDB python module.
- After last step for every query that does not have a URL. the RAG will use web URL data as a context.
- So for testing purpose i pick up latest news article URL and paste in the ChatBot. 
- Then ask questions accordingly. 

ToDos:
- Create Map reduce Chain		
- Create Refine Chain		
- Apply Advanced RAG methods like following:
    - Multi Query - Given a single user query, use an LLM to synthetically generate multiple other queries. Use each one of the new queries to retrieve documents, take the union of those documents for the final context of your prompt
    - Contextual Compression - Fluff remover. Normal retrieval but with an extra step of pulling out relevant information from each returned document. This makes each relevant document smaller for your final prompt (which increases information density)
    - Parent Document Retriever - Split and embed small chunks (for maximum information density), then return the parent documents (or larger chunks) those small chunks come from
    - Ensemble Retriever - Combine multiple retrievers together
    - Self-Query - When the retriever infers filters from a users query and applies those filters to the underlying data.
