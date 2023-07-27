import gradio as gr


def risk_factors_tab_ui(risk_factors: list[str]):
    return gr.Text(lines=10, label="Risk Factors", default=",".join(risk_factors))
