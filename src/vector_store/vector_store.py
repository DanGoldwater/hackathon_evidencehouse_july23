import os

import faiss
import numpy as np
import pandas
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from transformers import DistilBertModel, DistilBertTokenizer

FAISS_PATH = "faiss_index.pkl"
FAISS_PATH2 = "faiss_index2.pkl"
FAISS_OPAI_PATH = 'src/data/from_opai'

load_dotenv()
key = os.getenv("OPENAI_API_KEY")


import pickle

# tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
# model = DistilBertModel.from_pretrained("distilbert-base-uncased")
# from langchain.document_loaders import 
import faiss
import numpy as np
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from sentence_transformers import SentenceTransformer

# def get_embeddings_for_documnts(docs, path):
#     from langchain.embeddings import OpenAIEmbeddings
#     from langchain.vectorstores import FAISS
#     print('getting embeddings')
#     embeddings_getter = OpenAIEmbeddings()
#     embeddings = FAISS.from_texts(docs, embeddings_getter)
#     with open(path, 'wb') as f:
#         pickle.dump(embeddings, f)
#     return embeddings

def get_main_df():
    return pandas.read_csv(
        # "src/data/smaller.csv"
        "src/data/Contract_Data.csv"
    )
EmbeddingsOpenAi =  OpenAIEmbeddings(model='text-embedding-ada-002')
DF = get_main_df()

from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.document import Document
from langchain.vectorstores import FAISS


def get_embeddings_and_index(df, path):
    # df = df.sample(n=10)
    

    # Store the DataFrame index in the Document metadata
    documents = []
    for index, row in df.iterrows():
        d = Document(text=row['text'], metadata={'df_index': index}, page_content=row['text']) 
        documents += [d]

    db = FAISS.from_documents(documents=documents, embedding=EmbeddingsOpenAi)
    db.save_local(path)

    print('ok')
    return db


def query_vector_store(df, path, query_text):
    db = FAISS.load_local(path, embeddings=EmbeddingsOpenAi)
    query_document = Document(text=query_text, page_content=query_text)

    # Query the VectorStore
    results = db.similarity_search(query=query_text)
    # query(query_document)

    # Retrieve the matching rows from the DataFrame
    matching_rows = df[df.index.isin([doc.metadata['df_index'] for doc in results])]

    return matching_rows


def get_text_from_row(row):
    title = row["Title"]
    description = row["Description"]
    additional_text = row["Additional Text"]

    # Concatenate into single doc
    text = str(title) + " " + description + " " + str(additional_text)
    return text


def get_strucutred_text_from_small_df(df):
    string_out = ""
    for i, row in df.iterrows():
        title = 'Title: ' + str(row['Title'])
        description = 'Description: ' + str(row['Description'])
        additional_text = 'Additional Text: ' + str(row['Additional Text'])
    string_out = string_out + title + description + additional_text + '\n\n'
    return string_out


def get_nearest_rows_from_df(query: str, df: pandas.DataFrame = get_main_df(), top_k=5):
    model = SentenceTransformer("all-mpnet-base-v2")
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

    # make_local_faiss_db(df=df.sample(n=30))
    get_embeddings_and_index(df=DF, path=FAISS_OPAI_PATH)
    print('querying')
    ddf = query_vector_store(df=DF, 
                             path=FAISS_OPAI_PATH,
                             query_text='Our plan is to procure four hundred new street lamps for our count')
    for d in ddf['Description']:
        print(d)
    
    print('done')
    
    
    # sub_df = get_nearest_rows_from_df(query="Biggest NHS procure", df=df, top_k=2)
    # print(sub_df.head())


if __name__ == "__main__":
    main()
