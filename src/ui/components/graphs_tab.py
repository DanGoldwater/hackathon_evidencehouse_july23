import gradio as gr
import pandas as pd


def price_barchart_ui():
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
    # Previous projects cost
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
            ],
        }
    )
    gr.BarPlot(
        value=data2,
        x="Name",
        y="Cost",
        title="Previous Similair Projects",
        min_width=1200,
    )

    # Predicted stats
    gr.HighlightedText(
        lable="Predicted Statistics",
        value=[
            ("Cost Risk Factor", "23% Increase"),
            ("Expected Costs", "$1.2M"),
            ("Expected Time", "12 Months"),
        ],
        elem_id="predicted-stats",
    )


def graphs_tab_ui():
    return price_barchart_ui()
