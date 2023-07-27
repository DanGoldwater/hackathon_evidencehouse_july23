import gradio as gr


def risk_factors_tab_ui(risk_factors: list[str]):
    with gr.Column():
        for factor in risk_factors:
            gr.Label(factor)
    # gr.HighlightedText(
    #     value=[("Text", "Label 1"), ("to be", "Label 2"), ("highlighted", "Label 3")]
    # )
