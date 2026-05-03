# Invoice Automation AI Agent

## AI Legends 2026 — AI Agents Automation Competition

A reproducible AI agent pipeline for processing invoice documents, extracting structured invoice data from PDF and image files, validating the extracted information against a master SQLite database, detecting suspicious invoices, and producing final business decisions.

This repository is built for the **AI Legends 2026 — AI Agents Automation** track.

---

## Public Links

| Resource | Link |
|---|---|
| Kaggle Notebook | https://www.kaggle.com/code/temuulenmunkhochir/ai-legends-2026-final-ipynb |
| GitHub Repository | https://github.com/Temukk-dev/AI_Legends_2026 |
| Demo Video | TODO |
| Kaggle Writeup | https://www.kaggle.com/competitions/ai-legends-2026-ai-agents-automation/writeups/invoice-automation-ai-agent-ctr-audit |
| Demo Website | https://temukk-dev.github.io/AI_Legends_2026/ |
| Outputs Folder | [outputs/](outputs/) |

---

## Table of Contents

1. [Project Summary](#project-summary)
2. [Problem Statement](#problem-statement)
3. [Core Features](#core-features)
4. [Competition Requirement Mapping](#competition-requirement-mapping)
5. [Current Repository Structure](#current-repository-structure)
6. [Notebook Section Map](#notebook-section-map)
7. [System Architecture](#system-architecture)
8. [Full Processing Pipeline](#full-processing-pipeline)
9. [Input Data](#input-data)
10. [Master Database Tables](#master-database-tables)
11. [Extracted Invoice Schema](#extracted-invoice-schema)
12. [Validation Rules](#validation-rules)
13. [Risk Flags](#risk-flags)
14. [Final Decision Logic](#final-decision-logic)
15. [Output Files](#output-files)
16. [Current Notebook Run Result](#current-notebook-run-result)
17. [Mini Q&A Agent](#mini-qa-agent)
18. [How to Use on Kaggle](#how-to-use-on-kaggle)
19. [How to Run Locally](#how-to-run-locally)
20. [Demo UI](#demo-ui)
21. [Configuration](#configuration)
22. [Security Notes](#security-notes)
23. [Known Limitations](#known-limitations)
24. [Future Improvements](#future-improvements)
25. [Submission Checklist](#submission-checklist)

---

## Project Summary

The **Invoice Automation AI Agent** automates invoice review by combining:

- multimodal invoice input handling,
- Groq Vision-based field extraction,
- SQLite master database validation,
- deterministic business rule validation,
- suspicious invoice detection,
- final decision routing,
- CSV output generation,
- aggregate and invoice-level Q&A.

The system supports invoice files in:

| File Type | Supported |
|---|---|
| PDF | Yes |
| JPG | Yes |
| JPEG | Yes |
| PNG | Yes |

The notebook is designed to work in the Kaggle runtime and can automatically detect invoice files and the master database from the Kaggle input directory.

---

## Problem Statement

Manual invoice processing is slow and error-prone. A finance team usually needs to check:

- whether the invoice is a real invoice,
- whether the vendor is registered,
- whether the invoice amount is mathematically correct,
- whether the due date and invoice date are valid,
- whether the bank account matches the registered vendor,
- whether the invoice is duplicated,
- whether the invoice should be automatically posted, manually reviewed, or denied.

This project converts that manual workflow into an automated AI agent pipeline.

---

## Core Features

| Feature | Description |
|---|---|
| Multi-format invoice support | Processes PDF, JPG, JPEG, and PNG files |
| Automatic file discovery | Scans Kaggle input folders and detects invoice files automatically |
| PDF to image conversion | Converts PDF invoice pages into images using PyMuPDF |
| Vision-language extraction | Uses Groq Vision model to extract invoice fields as JSON |
| Multiple API key fallback | Supports multiple Groq API keys for more stable batch processing |
| Cache system | Saves processed invoice results to avoid repeated API calls |
| Master database validation | Loads SQLite tables and validates extracted fields |
| Vendor validation | Checks if the extracted vendor exists in the registered vendor table |
| Bank account validation | Compares extracted bank account with registered vendor data |
| Amount validation | Recalculates total values from quantity and unit price |
| Date validation | Checks invalid, missing, or inconsistent invoice dates |
| Duplicate detection | Compares new invoices with historical invoice records |
| Category classification | Classifies invoices using historical data and keyword rules |
| Risk flagging | Assigns structured risk flags for suspicious cases |
| Business decision routing | Produces `AUTO_POST`, `HUMAN_APPROVAL`, or `DENY` |
| Output export | Saves final CSV files for judging and review |
| Mini Q&A agent | Answers aggregate and selected invoice fact-check questions |
| Optional Gradio UI | Provides an optional demo interface for presentation |

---

## Competition Requirement Mapping

| Competition Requirement | Project Implementation |
|---|---|
| Process invoice images and PDFs | PDF/JPG/PNG scanner + image conversion helpers |
| Extract invoice information | Groq Vision JSON extraction |
| Validate invoice data | SQLite master database validation |
| Detect suspicious invoices | Risk flags: amount mismatch, invalid date, bank mismatch, duplicate, etc. |
| Assign final decision | `AUTO_POST`, `HUMAN_APPROVAL`, `DENY` decision engine |
| Answer aggregate questions | Deterministic Mini Q&A Agent over `final_results_df` and `summary_df` |
| Answer selected invoice questions | Invoice-level fact-check Q&A by file name |
| Export results | CSV files in `/kaggle/working/` |
| Reproducibility | Clear notebook sections, dependency installation, config, output verification |
| Public project link | GitHub repository |
| Public notebook | Kaggle notebook link |

---

## Current Repository Structure

The current GitHub repository contains the following main files and folders:

```text
AI_Legends_2026/
│
├── docs/
│   └── project documentation files
│
├── README.md
├── SUBMISSION_CHECKLIST.md
├── ai-legends-2026.ipynb
├── invoice-automation-ai-agent-v3-ipynb.ipynb
├── invoice_agent_core.py
├── app.py
└── requirements.txt
```

### File Purpose

| File / Folder | Purpose |
|---|---|
| `README.md` | Main project documentation |
| `SUBMISSION_CHECKLIST.md` | Competition submission checklist |
| `ai-legends-2026.ipynb` | Kaggle / Jupyter notebook version of the pipeline |
| `invoice-automation-ai-agent-v3-ipynb.ipynb` | Additional/final notebook version in the repository |
| `invoice_agent_core.py` | Core reusable Python pipeline logic |
| `app.py` | Demo UI entry point |
| `requirements.txt` | Python dependency list |
| `docs/` | Extra documentation and submission materials |
| `outputs/` | Exported CSV files from the final verified notebook run |
| `website/` | Static React + Vite frontend presentation demo for GitHub Pages |

---

## Notebook Section Map

The uploaded notebook contains a full end-to-end pipeline. The main sections are:

| Section | Name | Purpose |
|---|---|---|
| 1 | Competition Requirement Mapping | Maps competition needs to notebook sections |
| 2 | Install Dependencies | Installs required Python libraries |
| 3 | Import Libraries | Imports Python, data, image, and AI packages |
| 4 | Configuration | Sets input path, output path, model name, and limits |
| 5 | Load Multiple Groq API Keys | Loads multiple API keys from Kaggle Secrets |
| 6 | Auto-detect Dataset Files | Finds invoice files and database files automatically |
| 7 | Load Master Database | Reads SQLite tables into pandas DataFrames |
| 8 | Master Data Helpers | Provides flexible column matching and normalization helpers |
| 9 | Image/PDF Conversion Helpers | Converts PDF pages and images for model input |
| 10 | Vision-based Invoice Extraction | Extracts structured invoice JSON using Groq Vision |
| 11 | Field Normalization | Cleans dates, numbers, items, and text fields |
| 12 | Category Classification | Assigns financial category using historical and keyword rules |
| 13 | Validation Rules | Checks vendor, amount, date, bank, and duplicates |
| 14 | Risk Flagging and Final Decision Logic | Converts validation results into risk flags and decisions |
| 15 | Single Invoice Processing Function | Processes one invoice file end-to-end |
| 16 | Fast + Safe Batch Processing | Processes many invoices with cache and failure handling |
| 17 | Result Consolidation and Output Export | Builds final CSV outputs |
| 18 | Mini Q&A Agent | Answers aggregate and invoice-level questions |
| 19 | Final Output Verification | Checks output files, columns, and consistency |
| 20 | Downloadable Final Output Package | Creates a ZIP package of outputs |
| 21 | Optional Interactive Mini Q&A Chatbots | Optional console/Gradio demo interfaces |

---

## System Architecture

```text
                  ┌─────────────────────────────┐
                  │      Invoice Documents       │
                  │   PDF / JPG / JPEG / PNG     │
                  └──────────────┬──────────────┘
                                 │
                                 v
                  ┌─────────────────────────────┐
                  │    File Discovery Layer      │
                  │  Auto-scan Kaggle input root │
                  └──────────────┬──────────────┘
                                 │
                                 v
                  ┌─────────────────────────────┐
                  │  Image/PDF Conversion Layer  │
                  │   PIL + PyMuPDF rendering    │
                  └──────────────┬──────────────┘
                                 │
                                 v
                  ┌─────────────────────────────┐
                  │    Groq Vision Extraction    │
                  │  Vision model returns JSON   │
                  └──────────────┬──────────────┘
                                 │
                                 v
                  ┌─────────────────────────────┐
                  │  Normalization + Cleaning    │
                  │ Dates, numbers, text, items  │
                  └──────────────┬──────────────┘
                                 │
                                 v
      ┌──────────────────────────┴──────────────────────────┐
      │                                                     │
      v                                                     v
┌─────────────────────────────┐              ┌─────────────────────────────┐
│   SQLite Master Database     │              │   Extracted Invoice Record  │
│ Vendors / Items / Invoices   │              │ Vendor / Date / Total / Bank│
└──────────────┬──────────────┘              └──────────────┬──────────────┘
               │                                            │
               └──────────────────┬─────────────────────────┘
                                  v
                  ┌─────────────────────────────┐
                  │      Validation Engine       │
                  │ Vendor / Bank / Date / Math │
                  └──────────────┬──────────────┘
                                 │
                                 v
                  ┌─────────────────────────────┐
                  │      Risk Flagging Layer     │
                  │ Duplicate / mismatch / error │
                  └──────────────┬──────────────┘
                                 │
                                 v
                  ┌─────────────────────────────┐
                  │     Final Decision Engine    │
                  │ AUTO_POST / HUMAN / DENY     │
                  └──────────────┬──────────────┘
                                 │
                                 v
                  ┌─────────────────────────────┐
                  │ CSV Outputs + Q&A Agent      │
                  │ Summary + fact-check answers │
                  └─────────────────────────────┘
```

---

## Full Processing Pipeline

### Pipeline Overview

| Step | Module | Input | Processing | Output |
|---|---|---|---|---|
| 1 | File discovery | Kaggle input directory | Searches for `.pdf`, `.jpg`, `.jpeg`, `.png` | Invoice file list |
| 2 | File filtering | Detected files | Selects preferred evaluation folder if available | Processing target list |
| 3 | Database discovery | Kaggle input directory | Finds `master_invoices_database.db` | SQLite database path |
| 4 | Database loading | SQLite file | Reads all tables using pandas | Master dataframes |
| 5 | PDF/image conversion | Invoice file | Converts PDF page to image or opens image file | PIL image |
| 6 | Base64 encoding | PIL image | Converts image to data URL | Vision model input |
| 7 | Vision extraction | Image data | Groq Vision model extracts invoice fields | Raw JSON |
| 8 | JSON parsing | Model response | Extracts valid JSON from model output | Parsed dictionary |
| 9 | Field normalization | Raw fields | Normalizes dates, numbers, item lines, totals | Clean invoice dictionary |
| 10 | Category classification | Vendor/items/text | Uses historical invoice data and keyword rules | Category |
| 11 | Vendor validation | Vendor name | Fuzzy matches against `Vendors` table | Vendor registered status |
| 12 | Amount validation | Quantity, unit price, total | Recalculates amount and compares with extracted total | Math correctness flag |
| 13 | Date validation | Invoice date, due date | Checks missing or invalid date values | Date valid flag |
| 14 | Bank validation | Bank/account/vendor | Compares extracted bank account to vendor master data | Bank match flag |
| 15 | Duplicate detection | Invoice fields | Compares with historical `Invoices` table | Duplicate flag |
| 16 | Risk flagging | Validation results | Assigns risk flags | Risk list |
| 17 | Decision routing | Risk flags | Applies business rules | Final decision |
| 18 | Batch processing | All selected invoices | Processes files with cache and failure handling | `results_df` |
| 19 | Consolidation | Batch dataframe | Adds judge-friendly flags and summary columns | `final_results_df` |
| 20 | Export | Final dataframes | Saves CSV files | Output files |
| 21 | Q&A agent | Final results | Answers aggregate and invoice-specific questions | Text answers |
| 22 | Verification | Output files | Checks shapes, counts, and consistency | Submission readiness status |

---

## Input Data

### Invoice Files

The pipeline detects invoice files with these extensions:

| Extension | Meaning |
|---|---|
| `.pdf` | PDF invoice |
| `.jpg` | JPEG invoice image |
| `.jpeg` | JPEG invoice image |
| `.png` | PNG invoice image |

### Auto-detected Input Locations

The project can search these locations:

| Location | Purpose |
|---|---|
| `/kaggle/input` | Main Kaggle input root |
| `/kaggle/input/competitions/ai-legends-2026-ai-agents-automation` | Competition dataset directory |
| `eval_agent/eval_agent` | Preferred final evaluation invoice folder when available |
| `./invoice` | Local invoice folder |
| `./invoices` | Local invoice folder |
| `./data/invoices` | Local data folder |
| `.` | Fallback current directory |

### Current Notebook Dataset Detection

In the uploaded notebook run:

| Item | Value |
|---|---:|
| Detected invoice files | 200 |
| Detected database/data files | 1 |
| Preferred processing source | `eval_agent/eval_agent` |
| Selected processing files | 100 |

---

## Master Database Tables

The project uses:

```text
master_invoices_database.db
```

The notebook detected the following SQLite tables:

| Table | Shape in Current Notebook Run | Purpose |
|---|---:|---|
| `Vendors` | 10 rows × 7 columns | Registered vendor master data |
| `sqlite_sequence` | 5 rows × 2 columns | SQLite internal sequence table |
| `Items` | 50 rows × 3 columns | Master item/service catalog |
| `InvoiceCategories` | 10 rows × 3 columns | Financial invoice category definitions |
| `Invoices` | 596 rows × 8 columns | Historical invoice records |
| `InvoiceLines` | 719 rows × 6 columns | Historical invoice line items |

---

### Vendors Table

The `Vendors` table stores registered vendor information.

| Column | Description |
|---|---|
| `ID` | Unique vendor ID |
| `Name` | Registered vendor name |
| `Bank` | Registered bank name |
| `Account` | Registered bank account number |
| `Email` | Vendor email address |
| `RegisteredDate` | Vendor registration date |
| `Status` | Vendor status, such as active/inactive |

Example rows from the current notebook preview:

| ID | Name | Bank | Account | Email | RegisteredDate | Status |
|---:|---|---|---|---|---|---|
| 1 | Демо Компани-1 | Демо Банк 1 | 5001122334 | finance@demo1.mn | 2021-01-24 | active |
| 2 | Демо Компани-2 | Демо Банк 1 | 1102003004 | billing@demo2.mn | 2023-11-16 | active |
| 3 | Демо Компани-3 | Демо Банк 1 | 4001122334 | accounts@demo3.mn | 2023-09-05 | active |

Used for:

- vendor registration validation,
- fuzzy vendor matching,
- bank account validation,
- bank mismatch detection.

---

### Items Table

The `Items` table stores item and service names with unit prices.

| Column | Description |
|---|---|
| `ID` | Unique item ID |
| `ItemName` | Registered item or service name |
| `UnitPrice` | Reference unit price |

Example rows from the current notebook preview:

| ID | ItemName | UnitPrice |
|---:|---|---:|
| 1 | Сервер түрээс (сарын) | 850000 |
| 2 | Вэб байршуулалт (сарын) | 120000 |
| 3 | Домэйн сунгалт (жилийн) | 25000 |
| 4 | SSL сертификат (жилийн) | 45000 |
| 5 | Интернэт (Шилэн кабель, сарын) | 150000 |

Used for:

- invoice item interpretation,
- item/category reasoning,
- expected price comparison in future improvements.

---

### InvoiceCategories Table

The `InvoiceCategories` table stores financial category definitions.

| Column | Description |
|---|---|
| `ID` | Unique category ID |
| `Name` | Category name |
| `Description` | Explanation and examples for the category |

Example categories from the current notebook preview:

| ID | Name | Description Summary |
|---:|---|---|
| 1 | Түрээсийн зардал | Office, server room, warehouse, parking, forklift rental |
| 2 | Ашиглалтын зардал | Electricity, heating, water, cleaning, security, ventilation |
| 3 | Мэдээллийн технологийн зардал | Server, internet, license, software, cybersecurity, domain, SSL, backup |
| 4 | Тоног төхөөрөмж | Monitor, printer, IP camera, network cable installation |
| 5 | Тээвэр, логистик | Cargo transport, fuel, delivery, customs cost, GPS tracker |

Used for:

- category assignment,
- financial reporting,
- validation of extracted invoice category.

---

### Invoices Table

The `Invoices` table stores historical invoice records.

| Column | Description |
|---|---|
| `ID` | Historical invoice ID |
| `VendorName` | Vendor name |
| `InvoiceDate` | Invoice issue date |
| `DueDate` | Due date |
| `GrandTotal` | Total amount |
| `InvoiceCategoryID` | Linked category ID |
| `Status` | Historical approval/payment status |
| `ApprovedDate` | Approval date |

Example rows from the current notebook preview:

| ID | VendorName | InvoiceDate | DueDate | GrandTotal | InvoiceCategoryID | Status | ApprovedDate |
|---:|---|---|---|---:|---:|---|---|
| 1 | Демо Компани-10 | 2025-12-09 | 2025-12-24 | 280000 | 5 | approved | 2025-12-26 |
| 2 | Демо Компани-3 | 2026-03-06 | 2026-03-21 | 1760000 | 4 | approved | 2026-03-25 |
| 3 | Демо Компани-10 | 2025-05-15 | 2025-05-30 | 150000 | 9 | approved | 2025-06-06 |

Used for:

- duplicate detection,
- vendor history matching,
- historical category matching,
- amount/date comparison.

---

### InvoiceLines Table

The `InvoiceLines` table stores line-level invoice records.

| Column | Description |
|---|---|
| `ID` | Unique invoice line ID |
| `InvoiceID` | Related invoice ID |
| `ItemID` | Related item ID |
| `Qty` | Quantity |
| `UnitPrice` | Unit price |
| `Total` | Line total |

Example rows from the current notebook preview:

| ID | InvoiceID | ItemID | Qty | UnitPrice | Total |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 38 | 1 | 280000 | 280000 |
| 2 | 2 | 10 | 4 | 280000 | 1120000 |
| 3 | 2 | 11 | 2 | 320000 | 640000 |
| 4 | 3 | 47 | 1 | 150000 | 150000 |
| 5 | 4 | 46 | 1 | 320000 | 320000 |

Used for:

- future line-item validation,
- total amount checking,
- item-level audit support.

---

## Extracted Invoice Schema

The Groq Vision extraction prompt asks the model to return valid JSON with invoice fields.

### Target Extraction Fields

| Field | Description |
|---|---|
| `invoice_number` | Invoice number or document ID |
| `vendor_name` | Vendor/company name |
| `invoice_date` | Invoice issue date |
| `due_date` | Payment due date |
| `bank_name` | Bank name shown on invoice |
| `bank_account` | Bank account number shown on invoice |
| `email` | Vendor email if available |
| `currency` | Currency, usually `MNT` |
| `subtotal` | Subtotal before tax if available |
| `tax` | Tax/VAT if available |
| `total_amount` | Extracted final invoice amount |
| `items` | List of invoice line items |
| `raw_model_response` | Raw model output for debugging |
| `fallback_mode` | Whether fallback extraction was used |

### Item Schema

Each invoice line item may contain:

| Field | Description |
|---|---|
| `description` | Item/service description |
| `quantity` | Quantity |
| `unit_price` | Unit price |
| `line_total` | Extracted line total |
| `calculated_line_total` | Recalculated quantity × unit price |

---

## Field Normalization

The notebook normalizes extracted fields before validation.

| Normalization Type | Purpose |
|---|---|
| Text normalization | Lowercase, strip extra spaces, handle empty/null values |
| Number normalization | Remove currency symbols, commas, text noise, convert to float |
| Date normalization | Convert dates to ISO format where possible |
| Item normalization | Convert item quantities, prices, totals into numeric values |
| Boolean normalization | Convert string values such as yes/no, true/false into booleans |
| Risk flag normalization | Convert lists or empty values into stable risk flag strings |

---

## Category Classification

The project uses a rule-based and historical matching approach instead of training a new custom ML model.

Reason:

- the evaluation dataset may change,
- the system needs to be explainable,
- rules are easier to verify in a competition notebook,
- historical invoice records already provide useful category signals.

### Category Keyword Examples

| Category | Keywords |
|---|---|
| Software / IT | server, hosting, SSL, software, domain, cloud, API, license |
| Office Supplies | office, paper, printer, supplies |
| Utilities | electricity, water, heating, internet |
| Travel Expense | hotel, taxi, flight, travel |
| Maintenance | repair, support, maintenance |
| Training / Consulting | consulting, training, workshop |

---

## Validation Rules

The validation engine checks extracted invoice data against the master database and business rules.

### Vendor Validation

| Item | Description |
|---|---|
| Input | Extracted `vendor_name` |
| Reference | `Vendors.Name` |
| Method | Fuzzy matching using RapidFuzz |
| Output | `vendor_registered`, `matched_vendor_name`, `vendor_match_score` |
| Risk if failed | `UNREGISTERED_VENDOR` |

---

### Amount Validation

| Item | Description |
|---|---|
| Input | Quantity, unit price, extracted total |
| Method | Recalculate expected total and compare with extracted total |
| Output | `math_correct`, `calculated_total` |
| Risk if failed | `AMOUNT_MISMATCH` |

Example:

```text
quantity = 2
unit_price = 150000
calculated_total = 300000
extracted_total = 300000
math_correct = True
```

If the extracted total is different from the calculated total, the invoice is flagged.

---

### Date Validation

| Item | Description |
|---|---|
| Input | `invoice_date`, `due_date` |
| Method | Normalize to ISO date and check validity |
| Output | `date_valid` |
| Risk if failed | `INVALID_DATE` |

Typical suspicious cases:

- missing invoice date,
- missing due date,
- unreadable date,
- due date before invoice date,
- invalid date format.

---

### Bank Account Validation

| Item | Description |
|---|---|
| Input | Extracted bank account and matched vendor |
| Reference | `Vendors.Account` |
| Method | Exact normalized account comparison |
| Output | `bank_account_match` |
| Risk if failed | `BANK_ACCOUNT_MISMATCH` |

This check is important because a valid vendor name with a wrong bank account can indicate fraud or payment risk.

---

### Duplicate Detection

| Item | Description |
|---|---|
| Input | Invoice number, vendor, amount, invoice date |
| Reference | Historical `Invoices` table |
| Method | Invoice ID match or vendor + amount + date fallback match |
| Output | `is_duplicate` |
| Risk if failed | `DUPLICATE` |

---

## Risk Flags

Risk flags explain why an invoice is suspicious.

| Risk Flag | Meaning |
|---|---|
| `NONE` | No risk detected |
| `AMOUNT_MISMATCH` | Extracted amount does not match calculated amount |
| `UNREGISTERED_VENDOR` | Vendor is not found in the registered vendor database |
| `INVALID_DATE` | Invoice date or due date is missing, invalid, or inconsistent |
| `BANK_ACCOUNT_MISMATCH` | Extracted bank account does not match the registered vendor account |
| `DUPLICATE` | Invoice appears to already exist in historical records |
| `LOW_CONFIDENCE_EXTRACTION` | Extraction was incomplete or unreliable |
| `EXTRACTION_FAILED` | File could not be processed successfully |
| `HANDWRITTEN_IMAGE` | Handwritten content detected or suspected |
| `MISSING_REQUIRED_FIELD` | Required invoice field is missing |

---

## Final Decision Logic

The system assigns one final decision to each invoice.

| Final Decision | Meaning | Typical Condition |
|---|---|---|
| `AUTO_POST` | The invoice can be automatically processed | No risk flags and extraction succeeded |
| `HUMAN_APPROVAL` | The invoice needs manual review | Extraction failed, low confidence, unregistered vendor, amount mismatch, or uncertain data |
| `DENY` | The invoice should not be approved automatically | Serious risk such as bank mismatch or duplicate |

### Decision Logic Used in the Current Notebook Consolidation

```text
If extraction_status == FAILED:
    final_decision = HUMAN_APPROVAL

Else if risk_flags == NONE:
    final_decision = AUTO_POST

Else if risk_flags contains BANK_ACCOUNT_MISMATCH or DUPLICATE:
    final_decision = DENY

Else if risk_flags contains LOW_CONFIDENCE_EXTRACTION, EXTRACTION_FAILED,
UNREGISTERED_VENDOR, or AMOUNT_MISMATCH:
    final_decision = HUMAN_APPROVAL

Else:
    final_decision = HUMAN_APPROVAL
```

This makes the final output safer for finance automation because uncertain cases are sent to human review instead of being automatically posted.

---

## Output Files

The notebook exports final outputs to:

```text
/kaggle/working/
```

### Main Output Files

| File | Purpose |
|---|---|
| `outputs/all_results.csv` | Main source-of-truth table containing all processed invoices |
| `outputs/final_results.csv` | Final verified batch output used by the web demo and Mini Q&A examples |
| `outputs/clean_invoices.csv` | Only clean invoices with `AUTO_POST` |
| `outputs/suspicious_invoices.csv` | Invoices that require review or denial |
| `outputs/failed_files.csv` | Files that failed extraction but are still tracked |
| `outputs/aggregate_summary.csv` | One-row summary for evaluation and reporting |
| `outputs/invoice_automation_final_outputs.zip` | Downloadable package containing final CSV outputs |

---

## Output Table Details

### `outputs/all_results.csv`

`outputs/final_results.csv` is included in the repository as the same verified final batch table used by the web demo.

This is the main final result table.

Important columns include:

| Column | Description |
|---|---|
| `file_name` | Invoice file name |
| `file_path` | Full invoice file path |
| `file_type` | File extension such as pdf/png/jpg |
| `invoice_number` | Extracted invoice number |
| `vendor_name` | Extracted vendor name |
| `invoice_date` | Extracted and normalized invoice date |
| `due_date` | Extracted and normalized due date |
| `category` | Assigned invoice category |
| `bank_name` | Extracted bank name |
| `bank_account` / `account_number` | Extracted bank account number |
| `quantity` | Extracted quantity if available |
| `unit_price` | Extracted unit price if available |
| `total_amount` / `grand_total` | Extracted invoice total |
| `calculated_total` | Recalculated amount |
| `extraction_status` | `SUCCESS` or `FAILED` |
| `final_decision` | `AUTO_POST`, `HUMAN_APPROVAL`, or `DENY` |
| `risk_flags` | Risk flags detected for the invoice |
| `error_types` | Error/risk type summary |
| `denial_reason` | Explanation for denied invoices |
| `failure_reason` | Reason for failed extraction |
| `vendor_registered` | Whether vendor is registered |
| `bank_account_match` | Whether bank account matches vendor database |
| `math_correct` | Whether amount calculation is correct |
| `date_valid` | Whether date fields are valid |
| `is_duplicate` | Whether invoice is duplicate |
| `needs_human_approval` | Whether invoice needs human approval |
| `loaded_from_cache` | Whether result was loaded from cache |
| `processed_at` | Processing timestamp |
| `has_amount_mismatch` | Boolean flag for amount mismatch |
| `has_unregistered_vendor` | Boolean flag for unregistered vendor |
| `has_invalid_date` | Boolean flag for invalid date |
| `has_bank_account_mismatch` | Boolean flag for bank mismatch |
| `has_duplicate` | Boolean flag for duplicate |
| `has_extraction_failed` | Boolean flag for extraction failure |
| `is_clean` | Clean invoice flag |
| `is_suspicious` | Suspicious invoice flag |

---

### `outputs/clean_invoices.csv`

Contains only invoices that satisfy:

```text
final_decision == AUTO_POST
risk_flags == NONE
extraction_status != FAILED
```

Use this file to review invoices that the system considers safe for automatic processing.

---

### `outputs/suspicious_invoices.csv`

Contains invoices that satisfy at least one of these conditions:

```text
final_decision != AUTO_POST
risk_flags != NONE
extraction_status == FAILED
```

Use this file for manual review and error analysis.

---

### `outputs/failed_files.csv`

Contains invoices where extraction failed or the system could not confidently extract the required fields.

Important behavior:

- failed files are not ignored,
- failed files are preserved in the final result table,
- failed files are routed to `HUMAN_APPROVAL`.

This is important for a safe finance automation system.

---

### `outputs/aggregate_summary.csv`

Contains one row with aggregate counts.

| Column | Meaning |
|---|---|
| `total_invoices` | Total processed invoices |
| `correct_invoices` | Correct/clean invoice count |
| `clean_invoices` | Clean invoice count |
| `suspicious_invoices` | Suspicious invoice count |
| `failed_files` | Failed extraction count |
| `auto_post_count` | Number of `AUTO_POST` decisions |
| `human_approval_count` | Number of `HUMAN_APPROVAL` decisions |
| `deny_count` | Number of `DENY` decisions |
| `duplicate_count` | Duplicate invoice count |
| `amount_mismatch_count` | Amount mismatch count |
| `unregistered_vendor_count` | Unregistered vendor count |
| `invalid_date_count` | Invalid date count |
| `bank_account_mismatch_count` | Bank mismatch count |
| `image_invoice_count` | Image invoice count |
| `pdf_invoice_count` | PDF invoice count |
| `handwritten_image_invoice_count` | Handwritten image invoice count |

---

## Current Notebook Run Result

The uploaded notebook produced the following final verification result.

> These values describe the current notebook run. They may change if the full dataset, private test files, API outputs, or processing configuration changes.

### Processing Summary

| Metric | Count |
|---|---:|
| Total selected invoices processed | 100 |
| Clean / correct invoices | 68 |
| Suspicious invoices | 32 |
| Failed extraction invoices | 6 |
| PDF invoices | 70 |
| Image invoices | 30 |
| Handwritten image invoices | 0 |

### Decision Summary

| Final Decision | Count |
|---|---:|
| `AUTO_POST` | 68 |
| `HUMAN_APPROVAL` | 15 |
| `DENY` | 17 |
| Total | 100 |

### Risk Summary

| Risk Type | Count |
|---|---:|
| Duplicate invoices | 10 |
| Amount mismatch | 6 |
| Unregistered vendor | 0 |
| Invalid date | 3 |
| Bank account mismatch | 8 |

### Output File Shapes

| File | Shape |
|---|---:|
| `outputs/all_results.csv` | 100 rows × 58 columns |
| `outputs/final_results.csv` | 100 rows × 58 columns |
| `outputs/clean_invoices.csv` | 68 rows × 58 columns |
| `outputs/suspicious_invoices.csv` | 32 rows × 58 columns |
| `outputs/failed_files.csv` | 6 rows × 58 columns |
| `outputs/aggregate_summary.csv` | 1 row × 16 columns |

### Final Verification Status

```text
FINAL STATUS: READY FOR SUBMISSION
```

---

## Mini Q&A Agent

The notebook includes a deterministic Mini Q&A Agent.

It does not call an external LLM.  
It answers questions directly from:

```text
final_results_df
summary_df
```

This makes the Q&A output stable, reproducible, and consistent with exported CSV files.

---

### Supported Aggregate Questions

| Question Type | Example Question | Example Answer From Current Run |
|---|---|---|
| Total invoices | `Нийт хэдэн invoice байна вэ?` | `Нийт 100 invoice байна.` |
| Clean invoices | `Хэдэн invoice зөв invoice вэ?` | `Зөв буюу clean invoice: 68.` |
| Suspicious invoices | `Хэдэн invoice сэжигтэй вэ?` | `Сэжигтэй invoice: 32.` |
| Duplicate invoices | `Хэдэн invoice duplicate вэ?` | `Duplicate invoice: 10.` |
| Math errors | `Хэдэн invoice математик тооцооллын алдаатай вэ?` | `6` |
| Unregistered vendors | `Хэдэн invoice бүртгэлгүй vendor-той вэ?` | `0` |
| Invalid dates | `Хэдэн invoice буруу огноотой вэ?` | `3` |
| Bank mismatches | `Хэдэн invoice банкны мэдээллийн зөрүүтэй вэ?` | `8` |
| Image invoices | `Хэдэн invoice зураг хэлбэртэй вэ?` | `30` |
| Handwritten images | `Хэдэн invoice гар бичмэлтэй зураг вэ?` | `0` |
| Human approval | `Хэдэн invoice HUMAN_APPROVAL авах ёстой вэ?` | `15` |
| Deny | `Хэдэн invoice DENY болох ёстой вэ?` | `17` |

---

### Supported Invoice-Level Fact Check Questions

The Q&A agent can answer selected invoice questions by file name.

Example file:

```text
invoice_001.pdf
```

| Question | Example Answer From Current Run |
|---|---|
| `invoice_001.pdf final decision юу вэ?` | `HUMAN_APPROVAL` |
| `invoice_001.pdf duplicate мөн үү?` | `үгүй` |
| `invoice_001.pdf vendor-ийн нэр юу вэ?` | `Демо Компани-5` |
| `invoice_001.pdf ямар category-д ангилагдсан бэ?` | `7` |
| `invoice_001.pdf due date хэд вэ?` | `2026-03-17` |
| `invoice_001.pdf bank account бүртгэлтэй эсэх?` | `үгүй` |
| `invoice_001.pdf яагаад deny болсон бэ?` | `DENY болоогүй. Final decision: HUMAN_APPROVAL.` |
| `invoice_001.pdf ямар төрлийн алдаа илэрсэн бэ?` | `AMOUNT_MISMATCH` |
| `invoice_001.pdf human approval авах ёстой юу?` | `тийм` |
| `invoice_001.pdf математик тооцоолол зөв үү?` | `үгүй` |

---

## How to Use on Kaggle

### 1. Open the Kaggle Notebook

Use the public notebook:

```text
https://www.kaggle.com/code/temuulenmunkhochir/ai-legends-2026-final-ipynb
```

### 2. Add Competition Dataset

Make sure the competition dataset is attached to the notebook.

Expected input root:

```text
/kaggle/input/competitions/ai-legends-2026-ai-agents-automation
```

The notebook automatically scans for:

```text
.pdf
.jpg
.jpeg
.png
.db
.sqlite
.sqlite3
```

### 3. Add Groq API Keys to Kaggle Secrets

The uploaded notebook uses these secret names:

| Secret Name |
|---|
| `groq_API_1_new` |
| `groq_API_2_new` |
| `groq_API_3_new` |
| `groq_API_4_new` |
| `groq_API_5_new` |

Recommended additional fallback names for local/core compatibility:

| Secret / Environment Name |
|---|
| `GROQ_API_KEY_1` |
| `GROQ_API_KEY_2` |
| `GROQ_API_KEY_3` |
| `GROQ_API_KEY_4` |
| `GROQ_API_KEY_5` |
| `GROQ_API_KEY` |
| `API` |

Do not write API keys directly inside the notebook.

### 4. Run All Cells

Run the notebook from top to bottom.

The notebook will:

1. install dependencies,
2. import libraries,
3. load API keys,
4. detect invoice files,
5. load the master database,
6. convert PDF/images,
7. extract invoice fields,
8. validate invoices,
9. assign final decisions,
10. export CSV files,
11. verify output consistency,
12. create a downloadable ZIP package.

### 5. Download Outputs

After running the notebook, download:

```text
/kaggle/working/all_results.csv
/kaggle/working/clean_invoices.csv
/kaggle/working/suspicious_invoices.csv
/kaggle/working/failed_files.csv
/kaggle/working/aggregate_summary.csv
/kaggle/working/invoice_automation_final_outputs.zip
```

---

## How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Temukk-dev/AI_Legends_2026.git
cd AI_Legends_2026
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows
.venv\Scripts\activate
```

```bash
# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is incomplete, install the notebook dependencies directly:

```bash
pip install groq pymupdf pillow pandas numpy rapidfuzz gradio
```

### 4. Add API Key

Use environment variables.

```bash
# Windows PowerShell
setx GROQ_API_KEY "your_groq_api_key_here"
```

```bash
# macOS / Linux
export GROQ_API_KEY="your_groq_api_key_here"
```

### 5. Prepare Local Data Folder

Recommended local structure:

```text
AI_Legends_2026/
│
├── invoice/
│   ├── invoice_001.pdf
│   ├── invoice_002.png
│   └── ...
│
├── master_invoices_database.db
└── ...
```

Alternative supported folders:

```text
./invoice
./invoices
./data/invoices
```

### 6. Run the Core Pipeline

If using the reusable Python module:

```python
from pathlib import Path
from invoice_agent_core import process_invoices_pipeline

result = process_invoices_pipeline(
    input_root=Path("./invoice"),
    output_dir=Path("./outputs")
)
```

### 7. Run the Demo App

```bash
python app.py
```

---

## Demo UI

The repository includes a demo app entry point:

```text
app.py
```

The current repository README describes the demo UI as a 3-tab interface:

| Tab | Purpose |
|---|---|
| Process Invoices | Run or demonstrate invoice processing |
| Aggregate Q&A | Ask dataset-level count questions |
| Invoice Fact Check | Ask file-level validation questions |

Possible demo flow:

1. Show the project landing/demo UI.
2. Process sample invoice files.
3. Open aggregate Q&A.
4. Ask: `Нийт хэдэн invoice байна вэ?`
5. Ask: `Хэдэн invoice DENY болох ёстой вэ?`
6. Open invoice fact check.
7. Ask: `invoice_001.pdf final decision юу вэ?`
8. Show CSV outputs.

---

## Configuration

### Main Notebook Config

| Variable | Value / Meaning |
|---|---|
| `DEFAULT_INPUT_ROOT` | `/kaggle/input` |
| `COMPETITION_NAME` | `ai-legends-2026-ai-agents-automation` |
| `COMPETITION_DIR` | Competition dataset path |
| `OUTPUT_DIR` | `/kaggle/working` or `./outputs` |
| `GROQ_VISION_MODEL` | `meta-llama/llama-4-scout-17b-16e-instruct` |
| `MAX_FILES_TO_PROCESS` | `None` means no global limit in early config |
| `MAX_PDF_PAGES` | `2` |
| `QUICK_TEST` | `False` in final batch section |
| `PROCESS_LIMIT` | `10` only used when `QUICK_TEST=True` |
| `USE_CACHE` | `True` |
| `FORCE_REPROCESS` | `False` |
| `CACHE_DIR` | `/kaggle/working/invoice_cache` |
| `PREFERRED_FOLDER_KEYWORD` | `eval_agent/eval_agent` |

---

## Dependencies

Main dependencies:

| Package | Purpose |
|---|---|
| `groq` | Vision-language model API client |
| `pymupdf` | PDF rendering and text extraction |
| `pillow` | Image processing |
| `pandas` | DataFrame processing and CSV export |
| `numpy` | Numeric handling |
| `rapidfuzz` | Fuzzy matching for vendor validation |
| `gradio` | Optional demo chatbot/UI |
| `sqlite3` | Built-in Python SQLite database access |
| `pathlib` | Path handling |
| `json` | JSON parsing and cache storage |
| `base64` | Image encoding for vision model calls |

Install command:

```bash
pip install groq pymupdf pillow pandas numpy rapidfuzz gradio
```

---

## Cache System

The batch processor includes a JSON cache system.

### Purpose

| Benefit | Explanation |
|---|---|
| Reduces repeated API calls | Already processed invoice outputs can be loaded from cache |
| Saves runtime | Useful during Kaggle notebook reruns |
| Improves stability | If API limits happen later, existing cached results can still be used |
| Debug-friendly | Each invoice result is stored separately |

### Cache Location

```text
/kaggle/working/invoice_cache
```

### Cache Behavior

| Setting | Meaning |
|---|---|
| `USE_CACHE=True` | Load existing result if cache exists |
| `FORCE_REPROCESS=False` | Do not call API again if cache exists |
| `FORCE_REPROCESS=True` | Ignore cache and reprocess files |
| Cache clear cell | Optional cell deletes old cache before rerun |

---

## Failure Handling

The system does not drop failed files.

If extraction fails:

```text
extraction_status = FAILED
final_decision = HUMAN_APPROVAL
needs_human_approval = True
risk_flags = LOW_CONFIDENCE_EXTRACTION or EXTRACTION_FAILED
```

This is safer than ignoring failed documents because every invoice remains visible in the final output.

---

## Security Notes

Do not commit:

```text
.env
kaggle.json
raw private invoice files
API keys
cache files containing private data
large generated outputs if not required
```

Recommended `.gitignore` additions:

```gitignore
.env
kaggle.json
__pycache__/
.ipynb_checkpoints/
outputs/
invoice_cache/
*.zip
*.db
*.sqlite
*.sqlite3
```

If the competition dataset is private, do not upload raw invoice files into the public repository.

---

## Known Limitations

| Limitation | Explanation |
|---|---|
| Vision extraction can fail | API limit, image quality, or model response issues can cause failures |
| Some results depend on API output | Rerunning with a different model response may slightly change extracted fields |
| Rule-based category classification | Easier to explain but less flexible than a trained classifier |
| Handwriting detection is simple | Current implementation depends on model signal and rule flags |
| Vendor matching may need tuning | Fuzzy matching threshold may need adjustment for noisy OCR/vision output |
| Bank validation requires exact matching | Formatting differences in account numbers can cause mismatch flags |
| Q&A agent is deterministic | Reliable for supported questions but not a general free-form chatbot |
| Local run requires data | The repository does not include private Kaggle invoice data |

---

## Future Improvements

| Improvement | Benefit |
|---|---|
| Add OCR fallback | Improve extraction when vision API fails |
| Add stronger line-item validation | Compare every extracted item with `InvoiceLines` and `Items` |
| Add confidence scoring | Rank invoices by extraction confidence and business risk |
| Add better handwriting detection | More accurate handwritten invoice handling |
| Add trained category classifier | Improve category assignment beyond keyword rules |
| Add HTML dashboard | Visual charts for decisions, risks, vendors, and categories |
| Add Streamlit/Gradio file upload | Easier live demo and user interaction |
| Add unit tests | More reliable validation logic |
| Add schema validation | Ensure all output columns follow a stable contract |
| Add model fallback | Try another model if Groq Vision extraction fails |

---

## Submission Checklist

Before final submission, verify:

| Requirement | Status |
|---|---|
| Public Kaggle notebook exists | Done |
| Public GitHub repository exists | Done |
| README is detailed and updated | This file |
| CSV outputs are generated | Done in notebook |
| Final output verification passes | Done in notebook |
| Aggregate Q&A works | Done in notebook |
| Invoice-level fact-check Q&A works | Done in notebook |
| Kaggle writeup submitted | Pending |
| Demo video uploaded | Pending |
| Demo website or public project link available | GitHub Pages website configured |
| No API keys committed | Required |
| No private raw data committed | Required |

---

## Recommended Demo Video Script Outline

Use this project flow in a short demo video:

1. Introduce the project:
   - "This is an Invoice Automation AI Agent for AI Legends 2026."
2. Explain the input:
   - "It processes PDF and image invoices."
3. Explain extraction:
   - "The system uses Groq Vision to extract structured invoice data."
4. Explain validation:
   - "It validates vendor, amount, date, bank account, and duplicate status."
5. Explain decisions:
   - "Each invoice becomes AUTO_POST, HUMAN_APPROVAL, or DENY."
6. Show outputs:
   - `outputs/all_results.csv`
   - `outputs/clean_invoices.csv`
   - `outputs/suspicious_invoices.csv`
   - `outputs/aggregate_summary.csv`
7. Show Q&A:
   - "How many invoices are suspicious?"
   - "What is invoice_001.pdf final decision?"
8. End with public links:
   - Kaggle Notebook
   - GitHub Repository
   - Kaggle Writeup
   - Demo Video

---

## Project Status

Current status based on the uploaded notebook:

```text
Notebook pipeline: Complete
Batch processing: Complete
Output export: Complete
Output verification: Complete
Mini Q&A agent: Complete
GitHub repository: Public
README: Updated
Demo video: Pending
Kaggle writeup: Pending
Demo website: GitHub Pages
```

---

## Author

**Temuulen Munkhochir**  
GitHub: [Temukk-dev](https://github.com/Temukk-dev)

---

## License

No license file is currently specified.  
If this repository will remain public, consider adding one of the following:

| License | Use Case |
|---|---|
| MIT | Simple open-source reuse |
| Apache-2.0 | Open-source reuse with patent protection |
| No license | Default: all rights reserved |

---

## Notes for Judges

This project is designed to be easy to inspect:

- The notebook is sectioned from setup to final verification.
- The final CSV outputs are consistent with the aggregate summary.
- Failed files are tracked instead of ignored.
- Q&A answers come directly from processed structured results.
- The final decision logic is deterministic and explainable.
- The pipeline supports both image and PDF invoice formats.



