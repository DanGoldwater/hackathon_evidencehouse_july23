import random
import time
from typing import Tuple

import gradio as gr
import openai

from src.embellish import embellish
from src.ui.backend.consts import MODEL_TYPE
from src.ui.backend.llm_inference import (create_chat_completion,
                                          load_intial_prompt,
                                          load_system_prompt)
from src.ui.backend.parsers import (parse_cost_drivers_data,
                                    parse_risk_factors_data)
from src.ui.components.cost_drivers_tab import (get_cost_driver_html_single,
                                                get_cost_driver_html_total)
from src.ui.components.graphs_tab import (create_stacked_barchart_df,
                                          get_unforseen_costs_html)
from src.ui.components.risk_factors_tab import get_risk_factor_html_total
from src.vector_store import vector_store

TOP_K_SIMILAR_CONTRACTS = 5


def chat_ui(
    risk_factors: gr.Blocks,
    cost_drivers: gr.Blocks,
    markdown_summary: gr.Blocks,
    barplot1: gr.Blocks,
    barplot2: gr.Blocks,
    unforseen_costs_html: gr.Blocks,
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

    def update_charts(
        history,
        risk_factors,
        cost_drivers,
        markdown_summary,
        barplot1,
        barplot2,
        unforseen_costs,
    ):
        if len(history) == 1:
            # summary
            summary = "Summary: " + history[-1][1].split("Summary: ")[-1]
            # bar plots (recomput)
            sub_df = vector_store.query_vector_store(
                df=vector_store.DF,
                path=vector_store.FAISS_OPAI_PATH,
                query_text=history[-1][0],
            )
            sub_df = embellish.embellish_dataframe(df=sub_df)
            barplot_1 = sub_df
            barplot_2 = create_stacked_barchart_df(sub_df)
            unforseen_costs = get_unforseen_costs_html(sub_df)

            # data
            risk_factors_data = get_risk_factor_html_total(
                parse_risk_factors_data(history[-1][1])
            )
            cost_drivers_data = get_cost_driver_html_total(
                parse_cost_drivers_data(history[-1][1])
            )
            return (
                risk_factors_data,
                cost_drivers_data,
                summary,
                barplot_1,
                barplot_2,
                unforseen_costs,
            )
        else:
            return (
                risk_factors,
                cost_drivers,
                markdown_summary,
                barplot1,
                barplot2,
                unforseen_costs,
            )

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    ).then(
        update_charts,
        [
            chatbot,
            risk_factors,
            cost_drivers,
            markdown_summary,
            barplot1,
            barplot2,
            unforseen_costs_html,
        ],
        [
            risk_factors,
            cost_drivers,
            markdown_summary,
            barplot1,
            barplot2,
            unforseen_costs_html,
        ],
    )
    clear.click(lambda: None, None, chatbot, queue=False)
