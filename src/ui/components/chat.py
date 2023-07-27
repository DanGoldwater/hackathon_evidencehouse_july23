import time
import random
import gradio as gr
from src.ui.backend.consts import MODEL_TYPE
from src.ui.backend.llm_inference import create_chat_completion


def chat_ui():
    def predict(message, history):
        chat_messages = []
        for human, assistant in history:
            chat_messages.append({"role": "user", "content": human})
            chat_messages.append({"role": "assistant", "content": assistant})
        chat_messages.append({"role": "user", "content": message})

        stream = create_chat_completion(messages=chat_messages)

        response = ""
        for chunk in stream:
            response += chunk
            yield response

    return gr.ChatInterface(predict)
