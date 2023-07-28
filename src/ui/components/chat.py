import time
import random
import openai
import gradio as gr
from src.ui.components.cost_drivers_tab import (
    get_cost_driver_html_single,
)
from src.ui.components.risk_factors_tab import (
    get_risk_factor_html_total,
)
from src.embellish import embellish
from src.ui.backend.parsers import parse_risk_factors_data, parse_cost_drivers_data
from src.ui.backend.consts import MODEL_TYPE
from src.ui.backend.llm_inference import (
    create_chat_completion,
    load_system_prompt,
    load_intial_prompt,
)
from src.ui.components.risk_factors_tab import get_risk_factor_html_total
from src.ui.components.cost_drivers_tab import get_cost_driver_html_total
from src.vector_store import vector_store

TOP_K_SIMILAR_CONTRACTS = 5


def chat_ui(
    risk_factors: gr.Blocks,
    cost_drivers: gr.Blocks,
):
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        chat_messages = []

        chat_messages = [
            {"role": "system", "content": load_system_prompt()}
        ] + chat_messages
        # First message
        if len(chat_messages) == 1:
            sub_df = vector_store.query_vector_store(
                df=vector_store.DF,
                path=vector_store.FAISS_OPAI_PATH,
                query_text=history[-1][0],
            )
            sub_df = embellish.embellish_dataframe(df=sub_df)
            text_from_sub_df = vector_store.get_strucutred_text_from_small_df(df=sub_df)

            chat_messages.append(
                {
                    "role": "user",
                    "content": load_intial_prompt(history[-1][0], text_from_sub_df),
                }
            )
        else:
            chat_messages.append({"role": "user", "content": history[-1][0]})

        for human, assistant in history:
            if human is not None:
                chat_messages.append({"role": "user", "content": human})
            if assistant is not None:
                chat_messages.append({"role": "assistant", "content": assistant})

        response = create_chat_completion(messages=chat_messages)
        history[-1][1] = ""
        for character in response:
            history[-1][1] += character
            yield history

    def update_charts(history, risk_factors, cost_drivers):
        if len(history) == 1:
            risk_factors_data = get_risk_factor_html_total(
                parse_risk_factors_data(history[-1][1])
            )
            cost_drivers_data = get_cost_driver_html_total(
                parse_cost_drivers_data(history[-1][1])
            )
            return risk_factors_data, cost_drivers_data
        else:
            return risk_factors, cost_drivers

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    ).then(
        update_charts,
        [chatbot, risk_factors, cost_drivers],
        [risk_factors, cost_drivers],
    )
    clear.click(lambda: None, None, chatbot, queue=False)
