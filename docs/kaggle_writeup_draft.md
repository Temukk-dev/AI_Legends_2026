# Kaggle Writeup Draft

## Project summary

This project is an invoice automation AI agent for the AI Legends 2026 track. It extracts invoice data, validates the extracted fields against master data, flags risks, decides whether an invoice should be auto-posted or reviewed, and exports reviewable CSV outputs.

## Workflow

1. Detect invoice files automatically from the input folder.
2. Extract structured fields from each invoice.
3. Normalize the extracted data.
4. Validate vendor registration, bank account, date consistency, duplicate history, and math correctness.
5. Assign `AUTO_POST`, `HUMAN_APPROVAL`, or `DENY`.
6. Export `final_results.csv`, `failed_files.csv`, and `aggregate_answers.csv`.

## Stage 1 capability

The project supports:

- invoice-level structured results
- `final_results.csv` as the single source of truth
- aggregate Q&A across the full batch
- selected-invoice fact-check Q&A
- failed file tracking
- checkpoint saving during processing
- a demo Gradio interface

## Notes

- `final_results.csv` is the canonical output for aggregate reasoning.
- The project is designed to be reproducible in local and Kaggle-style environments.
- The demo UI is intentionally separate from the core engine.
