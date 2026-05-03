# AI Legends 2026 Invoice Automation AI Agent

This project processes invoice images and PDFs, validates them against master data, flags risks, assigns a final business decision, and exports reviewable CSV outputs.

## Core workflow

1. Scan invoice files from the local `invoice/` folder or a Kaggle input root.
2. Extract structured invoice fields.
3. Normalize and validate invoice data against master database tables.
4. Assign `AUTO_POST`, `HUMAN_APPROVAL`, or `DENY`.
5. Export `final_results.csv` as the single source of truth.
6. Export `failed_files.csv` and `aggregate_answers.csv` for review.

## Key files

- `invoice_agent_core.py` contains the main pipeline logic.
- `app.py` provides a 3-tab demo UI:
  - Process Invoices
  - Aggregate Q&A
  - Invoice Fact Check
- `AI_Legends_2026_Final_Agent_v2.ipynb` is the current notebook.
- `AI_Legends_2026_Final_Agent_V3.ipynb` is the aligned final notebook filename expected by submission workflows.

## Stage 1 support

The project supports:

- invoice-level structured results
- `final_results.csv` as the source of truth
- `AUTO_POST` / `HUMAN_APPROVAL` / `DENY`
- aggregate Q&A
- selected-invoice fact-check Q&A
- failed file tracking
- checkpoint saving every 10 invoices
- `aggregate_answers.csv` export
- demo Gradio interface

## Outputs

Default outputs are written to `outputs/`:

- `final_results.csv`
- `failed_files.csv`
- `aggregate_answers.csv`

## Local data handling

The pipeline auto-detects invoice files under:

- `./invoice`
- `./data/invoices`
- `/kaggle/input`

It also finds `master_invoices_database.db` automatically when present.

## Run the demo UI

```bash
python app.py
```

## Run the core pipeline

Import `process_invoices_pipeline()` from `invoice_agent_core.py` and point it at your invoice folder if needed.

## Security

Do not commit raw invoice data, output caches, `.env`, or `kaggle.json` files. Add them to `.gitignore` before publishing.
