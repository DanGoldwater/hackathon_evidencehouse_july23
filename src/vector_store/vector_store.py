from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader
import pathlib
import os
import langchain
import chromadb
from langchain.embeddings.openai import OpenAIEmbeddings
import pandas
import xml.etree.ElementTree as ET
import pickle
import time
import langchain
from langchain.embeddings import OpenAIEmbeddings
from time import sleep
import langchain
from sentence_transformers import SentenceTransformer
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from transformers import DistilBertTokenizer, DistilBertModel
import torch
import faiss
import numpy as np  
# Load the document, split it into chunks, embed each chunk and load it into the vector store.

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')


from langchain.embeddings import HuggingFaceEmbeddings

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
from dotenv import load_dotenv

CHROMA = './chroma_db'
FAISS_PATH = './faiss'

load_dotenv()
key = os.getenv("OPENAI_API_KEY")


tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')
def local_faisss_again(df):
    model = SentenceTransformer('all-mpnet-base-v2')

    # Get embeddings for each row 
    embeds = []
    for i, row in df.iterrows():
        text = get_text_from_row(row)
        embed = model.encode(text)
        embeds.append(embed)
    # embeddings = [model.encode(row['Text']) for idx, row in df.iterrows()]

    embeds = np.array(embeds)
    index = faiss.IndexIDMap(faiss.IndexFlatIP(768)) 

    # Add embeddings to index
    index.add_with_ids(embeds, np.arange(len(embeds))) 

    # Save index
    faiss.write_index(index, 'faiss_index.pkl')
def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt')
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :].detach().numpy()
    return embeddings

def get_text_from_row(row):
    title = row["Title"]    
    description = row["Description"]
    additional_text = row["Additional Text"]

    # Concatenate into single doc
    text = str(title) + " " + description + " " + str(additional_text)
    return text

def make_faiss_locally(df):
    embeddings = [] 
    texts = []
    for index, row in df.iterrows():
        text = get_text_from_row(row)
        texts.append(text)
        
    embedding = get_embedding(text)
    embeddings.append(embedding)

    # Create a FAISS index
    d = embeddings[0].shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(np.vstack(embeddings))

    # Save the FAISS index to a file
    faiss.write_index(index, 'faiss_index.bin')


def get_embeddings_for_documnts(docs, path):
    retries = 0
    max_retries = 30
    backoff_factor = 2
    print('getting embeddings')
    embeddings_getter = OpenAIEmbeddings(model='text-embedding-ada-002')
    embeddings_getter = get_embedding_locally
    
    with open(path, 'wb') as f:
        pickle.dump(embeddings, f)
    return embeddings

def get_embedding_locally(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt')

    # Get the embeddings from the DistilBERT model
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :].detach().numpy()

    return embeddings


def create_vectorstore_from_NHS_df(df):
    # Initialize docs list
    docs = []
   
    for index, row in df.iterrows():
        # Extract columns for this row
        title = row["Title"]
        description = row["Description"]
        additional_text = row["Additional Text"]

        # Concatenate into single doc
        doc = str(title) + " " + description + " " + str(additional_text)

        # Add to docs list
        docs.append(doc)
    get_embeddings_for_documnts(docs=docs, path=FAISS_PATH)
    



def main():
    df = pandas.read_csv(
        "src/data/nhs_contract_data/NHS_early_future_opportunity_awarded_closed.csv"    )
    
    # make_faiss_locally(df=df)
    local_faisss_again(df.sample(n=10))


if __name__ == "__main__":
    main()
