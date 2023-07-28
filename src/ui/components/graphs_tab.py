import gradio as gr
import pandas as pd


# TODO - replace dummy data
# Check column names
DUMMY_DATA = pd.DataFrame(
    {"Name": ["Project 1", "Project 2", "Project 3", "Project 4", "Project 5"],
     "Total Value": [45, 67, 78, 32, 46],
     "Labour": [10, 20, 7, 10, 12],
     "Overhead": [10, 10, 13, 10, 30],
     "Materials": [25, 37, 58, 12, 4],
     "unforseen_costs": ["Overspend on IT", "Unexpected inflation", "Supplier went bust", "Pandemic-related costs", "Cost of materials increased"],
    })

# TODO - a hack!
dummy_data = pd.DataFrame({"Notice Identifier": [], "Estimate - Labour: A-AAA":[], "Estimate - Labour: B - BBB":[], "Estimate - Overhead: A-AAA":[], "Estimate - Overhead: B - BBB":[], 'Estimate - Materials: A-AAA':[], 'Estimate - Materials: B - BBB':[], "Total Estimate": []})

def costs_barchart_ui(df):
    print(df)

    id_col = "Notice Identifier"
    categories = ["Estimate - Labour: A-AAA", "Estimate - Labour: B - BBB", "Estimate - Overhead: A-AAA", "Estimate - Overhead: B - BBB", 'Estimate - Materials: A-AAA', 'Estimate - Materials: B - BBB']
    categories_and_id = [id_col, "Estimate - Labour: A-AAA", "Estimate - Labour: B - BBB", "Estimate - Overhead: A-AAA", "Estimate - Overhead: B - BBB", 'Estimate - Materials: A-AAA', 'Estimate - Materials: B - BBB']
    
    # Total costs bar chart
    total_costs_df = df[[id_col, "Total Estimate"]] # TODO check column names including 
    print("I expect a bar plot")
    gr.BarPlot(total_costs_df, x=id_col, y="Total Estimate", title="Estimated costs of similar projects", min_width=1200)

        # Stacked 
        stacked_df = df[categories_and_id]
        stacked_df = stacked_df.melt(id_vars=id_col, value_vars=categories)
        gr.BarPlot(stacked_df, x=id_col, y="value", color="variable", title="Estimated costs split by type")

    # Unforseen costs
    # gr.HTML("<b>Unforseen costs</b>")
    # with gr.Column():
    #     unforseen_costs = df["unforseen_costs"].values.tolist()
    #     for description in unforseen_costs:
    #         gr.HTML(f"<li>{description}</li>")


def graphs_tab_ui(df=dummy_data):
    print(df)
    return costs_barchart_ui(df)
