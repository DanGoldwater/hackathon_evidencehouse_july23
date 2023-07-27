from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader
import pathlib

# PATH_TO_DATA = pathlib.Path('data/feedback_data/')
# loader = DirectoryLoader(PATH_TO_DATA, glob="**/*.odt", use_multithreading=True)

# # Load the document, split it into chunks, embed each chunk and load it into the vector store.
# # raw_documents = TextLoader('../../../state_of_the_union.txt').load()
# raw_documents = loader.load()
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# documents = text_splitter.split_documents(raw_documents)
# db = Chroma.from_documents(documents, OpenAIEmbeddings())

import os
import langchain
from langchain.vectorstores import Vectorstore
from langchain.embeddings.openai import OpenAIEmbeddings

import xml.etree.ElementTree as ET

def create_vectorstore(folder):

  # Initialize variables
  descriptions = []
  details = []  
  embeddings = OpenAIEmbeddings()

  # Iterate over XML files in folder
  for filename in os.listdir(folder):
    if filename.endswith('.xml'):
        
      try:
        tree = ET.parse(os.path.join(folder, filename))
        
        # Extract descriptions
        descriptions.extend([notice.find('Description').text for notice in tree.findall('FullNotice')])
            
        # Extract details
        details.extend([detail.find('TextData').text  
                        for notice in tree.findall('FullNotice')
                        for detail in notice.find('AdditionalDetails')])
        
      except Exception as e:
        # Log exceptions
        with open('exceptions.txt', 'a') as f:
          f.write(filename + ": " + str(e) + "\n")

  # Create vectorstore 
  docs = descriptions + details
  vs = Vectorstore(docs, embedding=embeddings)
  
  return vs

#%%
