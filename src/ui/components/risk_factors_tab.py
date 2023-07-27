import gradio as gr
from pydantic import BaseModel
from src.ui.models import RiskFactor


def get_risk_factor_html(risk_factor: RiskFactor):
    if risk_factor.min_cost is None or risk_factor.max_cost is None:
        return f"""
        <div style='font-size:20px'>
            <b>
                {risk_factor.title}
                <span style='color:red; margin-left:10px'> Risk: {risk_factor.risk_probability}</span>
                <span style='color:green; margin-left:10px'> Cost Range: N/A</span>
            </b>
            <br/>
        </div>
        <div style='font-size:18px'>
            {risk_factor.description}
        </div>
        <hr/>
        """
    else:
        return f"""
        <div style='font-size:20px'>
            <b>
                {risk_factor.title}
                <span style='color:red; margin-left:10px'> Risk: {risk_factor.risk_probability}</span>
                <span style='color:green; margin-left:10px'> Cost Range: ${risk_factor.min_cost/1_000_000}M - {risk_factor.max_cost/1_000_000}M</span>
            </b>
            <br/>
        </div>
        <div style='font-size:18px'>
            {risk_factor.description}
        </div>
        <hr/>
        """


def risk_factors_tab_ui(risk_factors: list[RiskFactor]):
    with gr.Column():
        return_elements = []
        for factor in risk_factors:
            rendered_el = gr.HTML(
                get_risk_factor_html(factor),
                interactive=True,
            )
            rendered_el = rendered_el.update(value="<div></div>")
            return_elements.append(rendered_el)

        return return_elements
