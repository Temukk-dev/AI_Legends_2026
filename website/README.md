# Invoice Automation AI Agent Website

Frontend presentation demo for the **AI Legends 2026 — AI Agents Automation** project.

Public links:

- Kaggle Notebook: https://www.kaggle.com/code/temuulenmunkhochir/ai-legends-2026-final-ipynb
- GitHub Repository: https://github.com/Temukk-dev/AI_Legends_2026
- Demo Video: TODO
- Kaggle Writeup: TODO

## Disclaimer

This website is a frontend presentation demo. The real invoice extraction, validation, decision logic, CSV export, and Mini Q&A Agent are implemented in the Kaggle notebook.

## What The Website Shows

- Problem statement and invoice automation workflow
- Risk detection rules and final decision logic
- Final verified notebook results
- Output files and project links
- Frontend-only upload demo
- Deterministic Mini Q&A Agent examples

## Final Verified Results

| Metric | Count |
|---|---:|
| Total invoices processed | 100 |
| Clean invoices | 68 |
| Suspicious invoices | 32 |
| Failed / low-confidence extraction | 6 |
| `AUTO_POST` | 68 |
| `HUMAN_APPROVAL` | 15 |
| `DENY` | 17 |
| Duplicate invoices | 10 |
| Amount mismatch | 6 |
| Unregistered vendor | 0 |
| Invalid date | 3 |
| Bank account mismatch | 8 |
| Image invoices | 30 |
| PDF invoices | 70 |
| Handwritten image invoices | 0 |

## Output Files

- `all_results.csv`
- `final_results.csv`
- `clean_invoices.csv`
- `suspicious_invoices.csv`
- `failed_files.csv`
- `aggregate_summary.csv`
- `invoice_automation_final_outputs.zip` when exported by the notebook

## Mini Q&A Agent

The Mini Q&A Agent is deterministic. It reads from `final_results_df` and `summary_df`, not from another LLM.

Example questions:

- Нийт хэдэн invoice байна вэ?
- niit heden invoice burtgesen be?
- Хэдэн invoice HUMAN_APPROVAL авах ёстой вэ?
- Хэдэн invoice DENY болох ёстой вэ?
- invoice_001.pdf final decision юу вэ?
- invoice_095.png extraction status юу вэ?

Example answers:

- Нийт 100 invoice байна.
- HUMAN_APPROVAL шаардлагатай invoice: 15.
- DENY болсон invoice: 17.
- `invoice_001.pdf`-ийн final decision: HUMAN_APPROVAL. Risk flags: AMOUNT_MISMATCH.

## Notebook Usage

1. Open the public Kaggle notebook.
2. Attach the competition dataset.
3. Add Groq API keys in Kaggle Secrets.
4. Run the notebook top to bottom.
5. Download the generated CSV files and ZIP bundle from `/kaggle/working`.

## Local Demo Usage

```bash
npm install
npm run dev
```

The web upload panel is demo-only and does not send files to a backend.

## Deployment

The Vite config uses `base: "./"` so the frontend can be published on GitHub Pages or any static host without path fixes.

```bash
npm run build
```

## Reproducibility Notes

- The notebook uses deterministic rule-based validation and final decision logic.
- The Mini Q&A Agent reads structured outputs instead of generating free-form answers from another LLM.
- Failed files are preserved in the final outputs instead of being dropped.

## Limitations

- The web app is not the processing engine.
- The browser upload area is a mock preview only.
- Demo video and Kaggle writeup links are still pending.

## Future Improvements

- Publish the demo video and writeup.
- Add richer charts for category, vendor, and risk distributions.
- Add a downloadable outputs panel wired to the exported ZIP bundle.

