import time
import random
import gradio as gr
from src.ui.backend.consts import MODEL_TYPE
from src.ui.backend.llm_inference import (
    create_chat_completion,
    load_system_prompt,
    load_intial_prompt,
)


def chat_ui():
    def predict(message, history):
        chat_messages = []

        for human, assistant in history:
            chat_messages.append({"role": "user", "content": human})
            chat_messages.append({"role": "assistant", "content": assistant})

        chat_messages = [
            {"role": "system", "content": load_system_prompt()}
        ] + chat_messages

        # If its the first message use the initial prompt (and vector db query)
        if len(chat_messages) == 1:
            chat_messages.append(
                {"role": "user", "content": load_intial_prompt(message)}
            )
        else:
            chat_messages.append({"role": "user", "content": message})

        stream = create_chat_completion(messages=chat_messages)

        response = ""
        for chunk in stream:
            response += chunk
            yield response

    return gr.ChatInterface(
        predict,
    )
