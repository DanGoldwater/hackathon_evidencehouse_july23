import langchain
import dotenv
import openai
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain

# from dotenv import load_dotenv, find_dotenv

# load_dotenv(find_dotenv())

import os
key = ''
os.environ["OPENAI_API_KEY"] = ''

# g4 = OpenAI(model='gpt-4')

# g4('What is a horse')
llm = OpenAI(openai_api_key=key)

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

llm_chain = LLMChain(prompt=prompt, llm=llm)

completion = openai.ChatCompletion.create( # Change the function Completion to ChatCompletion
  model = 'gpt-3.5-turbo',
  messages = [ # Change the prompt parameter to the messages parameter
    {'role': 'user', 'content': 'What is a horse?'}
  ],
  temperature = 0  
)

print(completion['choices'][0]['message']['content'])