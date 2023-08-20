# custom-knowledge-gpt-chatbot
Designed to make setting up a chatbot as easy as possible.
Steps:
- run: git clone https://github.com/IrfanThomson/custom-knowledge-gpt-chatbot.git
- run: cd custom-knowledge-gpt-chatbot
- run: pip install -r requirements.txt
- put text data in ./data/data.txt
- set up an index to use on Pinecone (https://www.pinecone.io/)
- follow data_upload.ipynb step by step to upload data
- customize prompt in prompts.py
- run: streamlit run app.py
