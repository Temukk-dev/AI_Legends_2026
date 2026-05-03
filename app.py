from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import gradio as gr
import pandas as pd

from invoice_agent_core import (
    FINAL_RESULT_COLUMNS,
    aggregate_answer,
    build_processing_summary_text,
    fact_check_invoice,
    load_final_results,
    process_invoices_pipeline,
)


DEFAULT_INPUT_ROOT = Path("invoice")
DEFAULT_OUTPUT_DIR = Path("outputs")
SMOKE_RESULTS_PATH = Path("outputs_smoke") / "final_results.csv"
SMOKE_FAILED_PATH = Path("outputs_smoke") / "failed_files.csv"


def _resolve_path(raw_value: Optional[str], fallback: Path) -> Path:
    if raw_value:
        return Path(raw_value).expanduser().resolve()
    return fallback.resolve()


def _empty_results_frame() -> pd.DataFrame:
    return pd.DataFrame(columns=FINAL_RESULT_COLUMNS)


def load_current_results(output_dir: Optional[str] = None) -> pd.DataFrame:
    output_path = _resolve_path(output_dir, DEFAULT_OUTPUT_DIR)
    final_results_path = output_path / "final_results.csv"
    if final_results_path.exists():
        return load_final_results(final_results_path)
    if SMOKE_RESULTS_PATH.exists():
        return load_final_results(SMOKE_RESULTS_PATH)
    return _empty_results_frame()


def load_current_failed(output_dir: Optional[str] = None) -> pd.DataFrame:
    output_path = _resolve_path(output_dir, DEFAULT_OUTPUT_DIR)
    failed_path = output_path / "failed_files.csv"
    if failed_path.exists():
        return pd.read_csv(failed_path, keep_default_na=False)
    if SMOKE_FAILED_PATH.exists():
        return pd.read_csv(SMOKE_FAILED_PATH, keep_default_na=False)
    return pd.DataFrame(columns=["file_name", "file_path", "processing_status", "error_types", "error_message"])


def run_processing(input_root: str, output_dir: str, max_files: Optional[int]) -> Tuple[str, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    preferred_input_root = _resolve_path(input_root, DEFAULT_INPUT_ROOT)
    preferred_output_dir = _resolve_path(output_dir, DEFAULT_OUTPUT_DIR)
    result = process_invoices_pipeline(
        preferred_input_root=preferred_input_root,
        preferred_output_dir=preferred_output_dir,
        max_files=max_files,
        checkpoint_every=10,
    )
    final_df = result["final_df"].copy()
    failed_df = result["failed_df"].copy()
    summary_text = build_processing_summary_text(final_df, failed_df, result["project_paths"])
    return summary_text, final_df, failed_df, final_df


def parse_max_files(raw_value: str) -> Optional[int]:
    value = str(raw_value).strip()
    if not value:
        return None
    parsed = int(float(value))
    return parsed if parsed > 0 else None


def answer_aggregate_question(question: str, current_results: pd.DataFrame, output_dir: str) -> str:
    df = current_results if isinstance(current_results, pd.DataFrame) and not current_results.empty else load_current_results(output_dir)
    return aggregate_answer(question, df)


def answer_fact_check(invoice_identifier: str, question: str, current_results: pd.DataFrame, output_dir: str) -> str:
    df = current_results if isinstance(current_results, pd.DataFrame) and not current_results.empty else load_current_results(output_dir)
    return fact_check_invoice(invoice_identifier, question, df)


with gr.Blocks(title="AI Legends 2026 Invoice Automation AI Agent") as demo:
    gr.Markdown(
        "# AI Legends 2026 Invoice Automation AI Agent\n"
        "Demo surface over `invoice_agent_core.py`. This is the repository-facing UI, not the production engine."
    )

    current_results_state = gr.State(load_current_results())

    with gr.Tab("Process Invoices"):
        gr.Markdown(
            "Run the batch pipeline against the moved `invoice/` folder or a custom input root. "
            "The pipeline exports `final_results.csv`, `failed_files.csv`, and `aggregate_answers.csv`."
        )
        with gr.Row():
            input_root = gr.Textbox(value=str(DEFAULT_INPUT_ROOT), label="Input root")
            output_dir = gr.Textbox(value=str(DEFAULT_OUTPUT_DIR), label="Output directory")
            max_files = gr.Textbox(value="", label="Max files (blank = all)")
        run_button = gr.Button("Run pipeline")
        summary_output = gr.Textbox(label="Run summary", lines=10)
        results_output = gr.Dataframe(label="final_results.csv preview")
        failed_output = gr.Dataframe(label="failed_files.csv preview")
        run_button.click(
            lambda input_root, output_dir, max_files: run_processing(input_root, output_dir, parse_max_files(max_files)),
            inputs=[input_root, output_dir, max_files],
            outputs=[summary_output, results_output, failed_output, current_results_state],
        )

    with gr.Tab("Aggregate Q&A"):
        gr.Markdown("Ask questions over the single source of truth in `final_results.csv`.")
        aggregate_question = gr.Textbox(label="Question", placeholder="Нийт хэдэн invoice байна вэ?")
        aggregate_answer_box = gr.Textbox(label="Answer", lines=6)
        aggregate_button = gr.Button("Ask")
        aggregate_button.click(
            answer_aggregate_question,
            inputs=[aggregate_question, current_results_state, output_dir],
            outputs=aggregate_answer_box,
        )

    with gr.Tab("Invoice Fact Check"):
        gr.Markdown("Check one invoice record by file name, invoice number, or path fragment.")
        invoice_identifier = gr.Textbox(label="Invoice identifier", placeholder="invoice_001.jpg")
        fact_question = gr.Textbox(
            label="Question",
            placeholder="final decision юу вэ?",
        )
        fact_answer_box = gr.Textbox(label="Answer", lines=6)
        fact_button = gr.Button("Check invoice")
        fact_button.click(
            answer_fact_check,
            inputs=[invoice_identifier, fact_question, current_results_state, output_dir],
            outputs=fact_answer_box,
        )

    gr.Markdown(
        "Demo mode notes:\n"
        "- The UI calls the shared core engine.\n"
        "- It is intended for review and submission demos.\n"
        "- Production processing remains in `invoice_agent_core.py`."
    )


if __name__ == "__main__":
    demo.launch()
