import gradio as gr
import pandas as pd


# TODO - replace dummy data
# Check column names
DUMMY_DATA = pd.DataFrame(
    {"Name": ["Proj 1", "Proj 2", "Proj 3", "Proj 4"],
     "Total Value": [45, 67, 78, 32],
     "Labour": [10, 20, 10, 10],
     "Overhead": [10, 10, 10, 10],
     "Materials": [25, 37, 58, 12],
     "unforseen_costs": ["cost 1", "r", 'R', "l"],
    })


def costs_barchart_ui(df=DUMMY_DATA):
    # Total costs bar chart
    total_costs_df = df[["Name", "Total Value"]] # TODO check column names including 
    gr.BarPlot(total_costs_df, x="Name", y="Total Value", title="Total value of similar projects", min_width=1200)

    # Stacked 
    stacked_df = df[["Name", "Labour", "Overhead", "Materials"]]
    stacked_df = stacked_df.melt(id_vars="Name", value_vars=["Labour", "Overhead", "Materials"])
    print(stacked_df.head())
    gr.BarPlot(stacked_df, x="Name", y="value", color="variable", title="Costs split by type")

    # Unforseen costs
    gr.HTML("<b>Unforseen costs</b>")
    with gr.Column():
        unforseen_costs = df["unforseen_costs"].values.tolist()
        for description in unforseen_costs:
            gr.HTML(f"<li>{description}</li>")


def graphs_tab_ui():
    return costs_barchart_ui()
