import gradio as gr


def risk_factors_tab_ui(risk_factors: list[str]):
    with gr.Column():
        gr.TextArea(
            value="\n\n".join(risk_factors), min_lines=4, max_lines=30, readonly=True
        )
