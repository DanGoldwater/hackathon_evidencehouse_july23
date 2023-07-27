import gradio as gr
import pandas as pd
from src.ui.models import CostDriver


def get_cost_driver_html(cost_driver: CostDriver):
    if cost_driver.min_cost is None or cost_driver.max_cost is None:
        return f"""
        <div style='font-size:20px'>
            <b>
                {cost_driver.title}
                <span style='color:green; margin-left:10px'> Cost Range: N/A</span>
            </b>
            <br/>
        </div>
        <div style='font-size:18px'>
            {cost_driver.description}
        </div>
        <hr/>
        """
    else:
        return f"""
        <div style='font-size:20px'>
            <b>
                {cost_driver.title}
                <span style='color:green; margin-left:10px'> Cost Range: ${cost_driver.min_cost/1_000_000}M - {cost_driver.max_cost/1_000_000}M</span>
            </b>
            <br/>
        </div>
        <div style='font-size:18px'>
            {cost_driver.description}
        </div>
        <hr/>
        """


def cost_drivers_tab_ui(cost_drivers: list[CostDriver]):
    with gr.Column():
        return_elements = []
        for factor in cost_drivers:
            rendered_el = gr.HTML(
                get_cost_driver_html(factor),
            )
            return_elements.append(rendered_el)
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
    return return_elements
