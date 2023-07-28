import gradio as gr
import pandas as pd


def create_stacked_barchart_df(raw_df):
    id_col = "Notice Identifier"
    categories_and_id = [
        id_col,
        "Total Estimate",
        "Estimate - Labour: A-AAA",
        "Estimate - Labour: B - BBB",
        "Estimate - Overhead: A-AAA",
        "Estimate - Overhead: B - BBB",
        "Estimate - Materials: A-AAA",
        "Estimate - Materials: B - BBB",
        "unforseen_costs",
    ]
    categories = [
        "Estimate - Labour: A-AAA",
        "Estimate - Labour: B - BBB",
        "Estimate - Overhead: A-AAA",
        "Estimate - Overhead: B - BBB",
        "Estimate - Materials: A-AAA",
        "Estimate - Materials: B - BBB",
    ]
    stacked_df = raw_df[categories_and_id]
    stacked_df = stacked_df.melt(id_vars=id_col, value_vars=categories)
    return stacked_df


def get_unforseen_costs_list(raw_df):
    return raw_df["unforseen_costs"].values.tolist()


def get_unforseen_costs_html(df=None):
    html = ""
    if df is None:
        return html
    unforseen_costs = df["unforseen_costs"].values.tolist()
    for description in unforseen_costs:
        html += f"<li>{description}</li>"
    return html


def costs_barchart_ui():
    # Total costs bar chart
    barplot1 = gr.BarPlot(
        # df,
        x="Notice Identifier",
        y="Total Estimate",
        title="Estimated costs of similar projects",
        min_width=1200,
    )

    barplot2 = gr.BarPlot(
        # create_stacked_barchart_df(df),
        x="Notice Identifier",
        y="value",
        color="variable",
        title="Estimated costs split by type",
    )

    # Unforseen costs
    gr.HTML("<b>Unforseen costs</b>")
    with gr.Column():
        html = get_unforseen_costs_html(None)
    returned_html = gr.HTML(html)
    return barplot1, barplot2, returned_html


def graphs_tab_ui():
    return costs_barchart_ui()
