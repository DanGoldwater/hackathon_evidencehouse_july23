import gradio as gr
import pandas as pd


# TODO - a hack!
dummy_data = pd.DataFrame({"Notice Identifier": [], "Estimate - Labour: A-AAA":[], "Estimate - Labour: B - BBB":[], "Estimate - Overhead: A-AAA":[], "Estimate - Overhead: B - BBB":[], 'Estimate - Materials: A-AAA':[], 'Estimate - Materials: B - BBB':[], "Total Estimate": [], "unforseen_costs": []})

dummy_data2 = pd.read_csv("src/data/test_chart_data2.csv") # For a sample project - air conditioning in hospital


def costs_barchart_ui(df):
    id_col = "Notice Identifier"
    categories = ["Estimate - Labour: A-AAA", "Estimate - Labour: B - BBB", "Estimate - Overhead: A-AAA", "Estimate - Overhead: B - BBB", 'Estimate - Materials: A-AAA', 'Estimate - Materials: B - BBB']
    categories_and_id = [id_col, "Total Estimate", "Estimate - Labour: A-AAA", "Estimate - Labour: B - BBB", "Estimate - Overhead: A-AAA", "Estimate - Overhead: B - BBB", 'Estimate - Materials: A-AAA', 'Estimate - Materials: B - BBB', "unforseen_costs"]
    
    df = df[categories_and_id]

    # Total costs bar chart
    total_costs_df = df[[id_col, "Total Estimate"]] # TODO check column names including 
    gr.BarPlot(total_costs_df, x=id_col, y="Total Estimate", title="Estimated costs of similar projects", min_width=1200)

    # Stacked 
    stacked_df = df[categories_and_id]
    stacked_df = stacked_df.melt(id_vars=id_col, value_vars=categories)
    gr.BarPlot(stacked_df, x=id_col, y="value", color="variable", title="Estimated costs split by type")

    # Unforseen costs
    gr.HTML("<b>Unforseen costs</b>")
    with gr.Column():
        unforseen_costs = df["unforseen_costs"].values.tolist()
        for description in unforseen_costs:
            gr.HTML(f"<li>{description}</li>")


def graphs_tab_ui(df=dummy_data2):

    return costs_barchart_ui(df)
