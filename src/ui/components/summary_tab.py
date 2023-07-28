import gradio as gr


def summary_tab_ui(summary_markdown: str):
    with gr.Column():
        markdown = gr.Markdown(summary_markdown)
    return markdown
