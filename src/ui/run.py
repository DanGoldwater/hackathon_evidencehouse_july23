import gradio as gr
import random
import pandas as pd
import time
from .components.chat import chat_ui
from .components.graphs_tab import graphs_tab_ui
from .components.risk_factors_tab import risk_factors_tab_ui

with gr.Blocks(
    css="""
.contain { display: flex; flex-direction: column; }
#component-0 { height: 100%; }
#chatbot { flex-grow: 1; }
#predicted-stats {font-size: 22px; }
"""
) as demo:
    with gr.Row(equal_height=False):
        with gr.Column(scale=2, min_width=600):
            chat = chat_ui()

        with gr.Column(scale=2, min_width=600):
            with gr.Tab("Graphs"):
                graphs = graphs_tab_ui()
            with gr.Tab("Risk Factors"):
                risk_factors = risk_factors_tab_ui(
                    [
                        "1. **Foreign Goods Tax Increase**: If the onboard computer chips used in the submarines are sourced from Taiwanese factories with Chinese suppliers, an increase in foreign goods tax could lead to a significant increase in chip costs, impacting the overall budget.",
                        "2. **Supply Chain Disruption**: If the submarine's torpedo systems are produced in a region experiencing political unrest or natural disasters, it may lead to supply chain disruptions, causing delays in the procurement process.",
                        "3. **Foreign Exchange Rate Fluctuation**: If a substantial portion of submarine components are procured from countries using different currencies, a sudden fluctuation in exchange rates can increase costs unexpectedly.",
                        "4. **Intellectual Property Rights Dispute**: If there's a disagreement about the ownership of the submarine's stealth technology between the designing firm and the manufacturing firm, it could lead to legal complications and project delays.",
                        "5. **Technical Issues in Advanced Systems**: If the submarines employ state-of-the-art sonar systems developed by a third-party firm, any technical failure or incapability on the part of that firm can significantly impact the project's timeline and quality.",
                    ]
                )


demo.queue()
demo.launch()


# What are the different cost drivers of the procurement
# What are the costs of potential risks
#
