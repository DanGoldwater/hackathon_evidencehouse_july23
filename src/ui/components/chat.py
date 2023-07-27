import time
import random
import gradio as gr
from src.embellish import embellish
from src.ui.backend.parsers import parse_risk_factors_data, parse_cost_drivers_data
from src.ui.backend.consts import MODEL_TYPE
from src.ui.backend.llm_inference import (
    create_chat_completion,
    load_system_prompt,
    load_intial_prompt,
)
from src.ui.components.risk_factors_tab import get_risk_factor_html
from src.ui.components.cost_drivers_tab import get_cost_driver_html
from src.vector_store import vector_store

TOP_K_SIMILAR_CONTRACTS = 5


def chat_ui(
    risk_factors: list[gr.Blocks],
    cost_drivers: list[gr.Blocks],
):
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
            
            sub_df = vector_store.get_nearest_rows_from_df(
                query=message,
                df=vector_store.get_main_df(),
                top_k=TOP_K_SIMILAR_CONTRACTS
                )
            
            sub_df = embellish.embellish_dataframe(df=sub_df)
            
            text_from_sub_df = vector_store.get_strucutred_text_from_small_df(df=sub_df)

            chat_messages.append(
                {"role": "user", "content": load_intial_prompt(message, text_from_sub_df)}
            )
        else:
            chat_messages.append({"role": "user", "content": message})

        stream = create_chat_completion(messages=chat_messages)

        response = ""
        for chunk in stream:
            response += chunk
            yield response

        # If its the first call then parse and render the risk factors and cost drivers
        if len(chat_messages) == 2:
            risk_factors_data = parse_risk_factors_data(response)
            cost_drivers_data = parse_cost_drivers_data(response)

            for i in range(len(risk_factors)):
                risk_factors[i].update(get_risk_factor_html(risk_factors_data[i]))
                cost_drivers[i].update(get_cost_driver_html(cost_drivers_data[i]))

    return gr.ChatInterface(
        predict,
    )
