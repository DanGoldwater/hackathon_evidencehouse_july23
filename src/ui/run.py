import random
import time

import gradio as gr
import pandas as pd

from .components.chat import chat_ui
from .components.cost_drivers_tab import cost_drivers_tab_ui
from .components.graphs_tab import graphs_tab_ui
from .components.risk_factors_tab import risk_factors_tab_ui
from .components.summary_tab import summary_tab_ui
from .models import CostDriver, RiskFactor

with gr.Blocks(
    css="""
.contain { display: flex; flex-direction: column; }
#component-0 { height: 100%; }
#chatbot { flex-grow: 1; }
#predicted-stats {font-size: 22px; }
""",
    live=True,
) as demo:
    with gr.Row(equal_height=False):
        with gr.Column(scale=2, min_width=600):
            with gr.Tab("Graphs"):
                barplot1, barplot2, unforseen_costs_html = graphs_tab_ui()
            with gr.Tab("Risk Factors"):
                risk_factors_element = risk_factors_tab_ui(
                    [
                        RiskFactor(
                            title="Foreign Goods Tax Increase",
                            description="If the onboard computer chips are sourced from Taiwanese factories with Chinese suppliers, any increase in foreign goods tax may lead to an increase in chip costs. Given the geopolitical tension and trade wars, the probability of such an occurrence is moderate.",
                            risk_probability="moderate",
                            min_cost=10_000_000,
                            max_cost=20_000_000,
                            impact="high",
                        ),
                        RiskFactor(
                            title="Rare Earth Elements",
                            description="Rare earth elements are required for the construction of the submarines. The cost of rare earth elements is expected to increase by 5% annually.",
                            risk_probability="low",
                            min_cost=10_000_000,
                            max_cost=20_000_000,
                            impact="high",
                        ),
                        RiskFactor(
                            title="Disruption of Supply Chain",
                            description="The supply chain for the construction of the submarines is complex and involves multiple suppliers. Any disruption in the supply chain may lead to delays in the project. The probability of such an occurrence is low.",
                            risk_probability="low",
                            min_cost=10_000_000,
                            max_cost=20_000_000,
                            impact="high",
                        ),
                    ]
                )

            with gr.Tab("Cost Drivers"):
                cost_drivers_element = cost_drivers_tab_ui(
                    [
                        CostDriver(
                            title="Skilled Labour",
                            description="Skilled labour is required for the construction of the submarines. The cost of labour is expected to increase by 5% annually.",
                            min_cost=10_000_000,
                            max_cost=20_000_000,
                        ),
                        CostDriver(
                            title="Rare Earth Elements",
                            description="Rare earth elements are required for the construction of the submarines. The cost of rare earth elements is expected to increase by 5% annually.",
                            min_cost=10_000_000,
                            max_cost=20_000_000,
                        ),
                        CostDriver(
                            title="Administrative Costs",
                            description="Administrative costs are expected to increase by 5% annually.",
                            min_cost=10_000_000,
                            max_cost=20_000_000,
                        ),
                    ]
                )

            with gr.Tab("Summary"):
                markdown = summary_tab_ui("")

        with gr.Column(scale=2, min_width=600):
            chat = chat_ui(
                risk_factors_element,
                cost_drivers_element,
                markdown,
                barplot1,
                barplot2,
                unforseen_costs_html,
            )

demo.queue()
demo.launch()
