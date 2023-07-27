from langchain.chat_models import ChatAnthropic
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage


def get_reply_from_anthropic(
    main_string: str,
    prepend_string:str = '',
    ):
    chat = ChatAnthropic(anthropic_api_key=)

    messages = [
        # SystemMessage(content=prepend_string),
        HumanMessage(
            content=main_string
        )
    ]
    response = chat()
    return response

print(get_reply_from_anthropic(
    main_string='What is a horse?',
    prepend_string='You are a helpful assistant'
))


    
    

