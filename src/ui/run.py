import gradio as gr
import random
import pandas as pd
import time

from .components.chat import chat_ui
from .models import RiskFactor, CostDriver
from .components.graphs_tab import graphs_tab_ui
from .components.summary_tab import summary_tab_ui
from .components.cost_drivers_tab import cost_drivers_tab_ui
from .components.risk_factors_tab import risk_factors_tab_ui

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
                graphs = graphs_tab_ui()
            with gr.Tab("Risk Factors"):
                risk_factors_elements = risk_factors_tab_ui(
                    [
                        RiskFactor(
                            title="Foreign Goods Tax Increase",
                            description="If the onboard computer chips are sourced from Taiwanese factories with Chinese suppliers, any increase in foreign goods tax may lead to an increase in chip costs. Given the geopolitical tension and trade wars, the probability of such an occurrence is moderate.",
                            risk_probability="moderate",
                            min_cost=10_000_000,
                            max_cost=20_000_000,
                        ),
                        RiskFactor(
                            title="Rare Earth Elements",
                            description="Rare earth elements are required for the construction of the submarines. The cost of rare earth elements is expected to increase by 5% annually.",
                            risk_probability="low",
                            min_cost=10_000_000,
                            max_cost=20_000_000,
                        ),
                        RiskFactor(
                            title="Disruption of Supply Chain",
                            description="The supply chain for the construction of the submarines is complex and involves multiple suppliers. Any disruption in the supply chain may lead to delays in the project. The probability of such an occurrence is low.",
                            risk_probability="low",
                            min_cost=10_000_000,
                            max_cost=20_000_000,
                        ),
                    ]
                )

            with gr.Tab("Cost Drivers"):
                cost_drivers_elements = cost_drivers_tab_ui(
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
                summary_tab_ui(
                    """
            # Project Summary: Procurement of 10x Submarines
            ## I. Project Overview 
            The project aims to procure 10 state-of-the-art submarines to enhance our naval capabilities. 
            These submarines will be outfitted with advanced onboard systems, stealth technology, and high-strength steel hulls. 

            ## II. Project Scope 1. 
            **Procurement of 10 Submarines**: 
            Submarines must be capable of long-range operations, equipped with advanced stealth technologies, 
            and meet all international and domestic regulatory requirements. 
            2. **Training**: Training programs for crew members and maintenance personnel. 
            3. **Maintenance & Support**: A comprehensive maintenance package for a 5-year period, including spare parts, regular system upgrades, and technical support. 
            4. **Delivery & Commissioning**: Safe delivery and commissioning of the submarines at designated naval bases. 
            ## III. Budget The estimated budget for this project is currently confidential,
            subject to adjustments depending on market conditions and the final technical specifications of the submarines. 
            ## IV. Timeline The project is expected to be completed in a span of 5-7 years, including the bidding process, construction, 
            testing, delivery, and commissioning. 
            ## V. Key Stakeholders 
            - 1. Ministry of Defense (Project Owner) 
            - 2. Selected Contractor (Submarine Supplier)
            - 3. Naval Command (End Users) 4. Training Providers (For Crew and Maintenance Personnel) 
            ## VI. Risk Analysis
            Several risk factors have been identified and will be closely monitored throughout the project. These include: 
            """
                )

        with gr.Column(scale=2, min_width=600):
            chat = chat_ui(
                risk_factors_elements,
                cost_drivers_elements,
            )

demo.queue()
demo.launch()
