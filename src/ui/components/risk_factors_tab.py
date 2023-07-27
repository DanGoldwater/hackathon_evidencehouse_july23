import gradio as gr
from pydantic import BaseModel
from src.ui.models import RiskFactor


def risk_factors_tab_ui(risk_factors: list[RiskFactor]):
    with gr.Column():
        for factor in risk_factors:
            gr.HTML(
                f"""
            <div style='font-size:20px'>
                <b>
                    {factor.title}
                    <span style='color:red; margin-left:10px'> Risk: {factor.risk_probability}</span>
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
