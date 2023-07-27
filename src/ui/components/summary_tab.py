import gradio as gr


def summary_tab_ui(summary_markdown: str):
    with gr.Column():
        gr.Markdown(summary_markdown)
