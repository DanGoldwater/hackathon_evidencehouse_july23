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

# tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
# model = DistilBertModel.from_pretrained('distilbert-base-uncased')


from langchain.embeddings import HuggingFaceEmbeddings

# model_name = "sentence-transformers/all-mpnet-base-v2"
# model_kwargs = {'device': 'cpu'}
# encode_kwargs = {'normalize_embeddings': False}
# hf = HuggingFaceEmbeddings(
#     model_name=model_name,
#     model_kwargs=model_kwargs,
#     encode_kwargs=encode_kwargs
# )
from dotenv import load_dotenv


FAISS_PATH = 'faiss_index.pkl'

load_dotenv()
key = os.getenv("OPENAI_API_KEY")


tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')


def get_main_df():
    return pandas.read_csv(
        "src/data/nhs_contract_data/NHS_early_future_opportunity_awarded_closed.csv"    )
    

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
    faiss.write_index(index, FAISS_PATH)



def get_text_from_row(row):
    title = row["Title"]    
    description = row["Description"]
    additional_text = row["Additional Text"]

    # Concatenate into single doc
    text = str(title) + " " + description + " " + str(additional_text)
    return text


def get_nearest_rows_from_df(query:str, df: pandas.DataFrame=get_main_df(), top_k=5):
    model = SentenceTransformer('all-mpnet-base-v2')
    index = faiss.read_index(FAISS_PATH)
    
    # Encode query and reshape it to 2D
    query_emb = model.encode(query).reshape(1, -1)
    
    # Search index
    distances, indices = index.search(query_emb, top_k)
    
    # Flatten the indices array
    indices = indices.flatten()
    
    # Get most similar rows
    sub_df = df.loc[indices]
    return sub_df


def main():
    df = get_main_df()
    sub_df = get_nearest_rows_from_df(query='Biggest NHS procure', top_k=2)
    print(sub_df.head())
    


if __name__ == "__main__":
    main()
