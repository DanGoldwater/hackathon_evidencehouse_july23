import gradio as gr
import pandas as pd
from src.ui.models import CostDriver


def cost_drivers_tab_ui(cost_drivers: list[CostDriver]):
    with gr.Column():
        for factor in cost_drivers:
            gr.HTML(
                f"""
            <div style='font-size:20px'>
                <b>
                    {factor.title}
                    <span style='color:green; margin-left:10px'> Cost: ${factor.cost_gbp/1_000_000}M</span>
                </b>
                <br/>
            </div>
            <div style='font-size:18px'>
                {factor.description}
            </div>
            <hr/>
            """
            )
        # Bar chart that displays the cost drivers
    data2 = pd.DataFrame(
        {
            "Name": [
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "I",
                "A2",
                "B2",
                "C2",
                "D2",
                "E2",
                "F2",
                "G2",
                "H2",
                "I2",
            ],
            "Cost": [
                28,
                55,
                43,
                91,
                81,
                53,
                19,
                87,
                52,
                28,
                55,
                43,
                91,
                81,
                53,
                19,
                87,
                52,
            ],
        }
    )
    gr.BarPlot(value=data2, x="Name", y="Cost", title="Cost Drivers", min_width=1200)
