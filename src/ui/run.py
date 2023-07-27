import gradio as gr
import random
import pandas as pd
import time
from .models import RiskFactor
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
                        RiskFactor(
                            title="Foreign Goods Tax Increase",
                            description="If the onboard computer chips are sourced from Taiwanese factories with Chinese suppliers, any increase in foreign goods tax may lead to an increase in chip costs. Given the geopolitical tension and trade wars, the probability of such an occurrence is moderate.",
                            risk_probability="moderate",
                            cost_increase_millions=10,
                        )
                    ]
                )


demo.queue()
demo.launch()


# What are the different cost drivers of the procurement
# What are the costs of potential risks
#
