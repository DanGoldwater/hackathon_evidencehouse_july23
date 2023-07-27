import os
import pandas
from sentence_transformers import SentenceTransformer
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from transformers import DistilBertTokenizer, DistilBertModel
import faiss
import numpy as np
from dotenv import load_dotenv
from tqdm import tqdm


FAISS_PATH = "faiss_index.pkl"

load_dotenv()
key = os.getenv("OPENAI_API_KEY")


tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertModel.from_pretrained("distilbert-base-uncased")


def get_main_df():
    return pandas.read_csv(
        "src/data/Contract_Data.csv"
    )


def make_local_faiss_db(df):
    model = SentenceTransformer("all-mpnet-base-v2")

    # Get embeddings for each row
    embeds = []
    for i, row in tqdm(df.iterrows(), total=df.shape[0]):
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
    text = str(title) + " " + str(description) + " " + str(additional_text)
    return text

def get_strucutred_text_from_small_df(df):
    string_out = ''
    for i, row in df.iterrows():
        title = 'Title: ' + row['Title']
        description = 'Description: ' + row['Description']
        additional_text = 'Additional Text: ' + row['Additional Text']
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
    df = get_main_df()
    make_local_faiss_db(df=df.sample(frac=0.5))
    
    
    # sub_df = get_nearest_rows_from_df(query="Biggest NHS procure", df=df, top_k=2)
    # print(sub_df.head())


if __name__ == "__main__":
    main()
