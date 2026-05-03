# Invoice Automation AI Agent

## AI Legends 2026 — AI Agents Automation Competition

PDF болон зураг хэлбэрийн invoice файлуудыг автоматаар уншиж, invoice-ийн бүтэцтэй мэдээллийг AI vision model-оор гарган авч, master SQLite database-тай тулган шалгаж, сэжигтэй invoice илрүүлж, эцсийн бизнес шийдвэр гаргадаг AI agent pipeline.

Энэхүү repository нь **AI Legends 2026 — AI Agents Automation** track-д зориулан бүтээгдсэн.

---

## Public Links

| Resource | Link |
|---|---|
| Kaggle Notebook | https://www.kaggle.com/code/temuulenmunkhochir/ai-legends-2026-final-ipynb |
| GitHub Repository | https://github.com/Temukk-dev/AI_Legends_2026 |
| Demo Video | - |
| Kaggle Writeup | - |
| Demo Website | - |

---

## Агуулга

1. [Төслийн хураангуй](#төслийн-хураангуй)
2. [Асуудлын тодорхойлолт](#асуудлын-тодорхойлолт)
3. [Үндсэн боломжууд](#үндсэн-боломжууд)
4. [Тэмцээний шаардлагатай уялдсан байдал](#тэмцээний-шаардлагатай-уялдсан-байдал)
5. [Одоогийн repository бүтэц](#одоогийн-repository-бүтэц)
6. [Notebook section map](#notebook-section-map)
7. [Системийн архитектур](#системийн-архитектур)
8. [Бүрэн processing pipeline](#бүрэн-processing-pipeline)
9. [Input data](#input-data)
10. [Master database tables](#master-database-tables)
11. [Extracted invoice schema](#extracted-invoice-schema)
12. [Field normalization](#field-normalization)
13. [Category classification](#category-classification)
14. [Validation rules](#validation-rules)
15. [Risk flags](#risk-flags)
16. [Final decision logic](#final-decision-logic)
17. [Output files](#output-files)
18. [Output table details](#output-table-details)
19. [Current notebook run result](#current-notebook-run-result)
20. [Mini Q&A Agent](#mini-qa-agent)
21. [How to use on Kaggle](#how-to-use-on-kaggle)
22. [How to run locally](#how-to-run-locally)
23. [Demo UI](#demo-ui)
24. [Configuration](#configuration)
25. [Dependencies](#dependencies)
26. [Cache system](#cache-system)
27. [Failure handling](#failure-handling)
28. [Security notes](#security-notes)
29. [Known limitations](#known-limitations)
30. [Future improvements](#future-improvements)
31. [Submission checklist](#submission-checklist)
32. [Recommended demo video script outline](#recommended-demo-video-script-outline)
33. [Project status](#project-status)
34. [Author](#author)
35. [Notes for judges](#notes-for-judges)

---

## Төслийн хураангуй

**Invoice Automation AI Agent** нь санхүүгийн invoice review ажлыг автоматжуулах зорилготой AI agent pipeline юм.

Систем дараах үндсэн хэсгүүдийг нэгтгэн ажиллуулна:

- multimodal invoice input handling,
- PDF/JPG/PNG file discovery,
- PDF to image conversion,
- Groq Vision model ашигласан field extraction,
- structured JSON parsing,
- extracted data cleaning and normalization,
- SQLite master database validation,
- deterministic business rule checking,
- suspicious invoice detection,
- final decision routing,
- CSV output export,
- aggregate болон invoice-level Q&A.

Дэмжих invoice file төрлүүд:

| File Type | Supported | Тайлбар |
|---|---|---|
| PDF | Yes | Digital эсвэл scanned invoice PDF |
| JPG | Yes | Invoice image |
| JPEG | Yes | Invoice image |
| PNG | Yes | Invoice image |

Notebook нь Kaggle runtime дээр ажиллахаар зохион байгуулагдсан. Input folder дотроос invoice file болон `master_invoices_database.db` database-ийг автоматаар илрүүлнэ.

---

## Асуудлын тодорхойлолт

Manual invoice processing нь удаан, алдаа гарах магадлал өндөр ажил. Санхүүгийн ажилтан invoice бүр дээр дараах зүйлсийг шалгах шаардлагатай болдог:

- invoice бодит invoice мөн эсэх,
- vendor бүртгэлтэй эсэх,
- invoice amount математик тооцооллын хувьд зөв эсэх,
- invoice date болон due date зөв эсэх,
- invoice дээрх bank account нь vendor database дээрх account-той таарч байгаа эсэх,
- invoice өмнө нь орсон duplicate invoice мөн эсэх,
- invoice автоматаар батлагдах уу, хүний review хэрэгтэй юу, эсвэл deny болох уу.

Энэхүү project нь дээрх manual workflow-г AI agent pipeline болгон автоматжуулсан.

---

## Үндсэн боломжууд

| Feature | Тайлбар |
|---|---|
| Multi-format invoice support | PDF, JPG, JPEG, PNG invoice файлуудыг боловсруулна |
| Automatic file discovery | Kaggle input folders дотроос invoice файлуудыг автоматаар хайж олно |
| PDF to image conversion | PDF invoice page-ийг PyMuPDF ашиглан image болгон хөрвүүлнэ |
| Vision-language extraction | Groq Vision model ашиглан invoice fields-ийг JSON хэлбэрээр extract хийнэ |
| Multiple API key fallback | Batch processing тогтвортой болгохын тулд олон Groq API key fallback дэмжинэ |
| Cache system | Давтан API call хийхгүй байхын тулд боловсруулсан invoice result-ийг cache-д хадгална |
| Master database validation | SQLite tables уншиж extracted fields-ийг тулган шалгана |
| Vendor validation | Extracted vendor name нь registered vendor table-д байгаа эсэхийг шалгана |
| Bank account validation | Invoice дээрх bank account vendor database дахь account-той таарч байгаа эсэхийг шалгана |
| Amount validation | Quantity болон unit price дээр үндэслэн нийт дүнг дахин тооцно |
| Date validation | Огноо хоосон, буруу, inconsistent эсэхийг шалгана |
| Duplicate detection | Historical invoice records-той харьцуулж duplicate илрүүлнэ |
| Category classification | Historical data болон keyword rule ашиглан invoice category онооно |
| Risk flagging | Сэжигтэй invoice-д structured risk flags онооно |
| Business decision routing | `AUTO_POST`, `HUMAN_APPROVAL`, `DENY` шийдвэр гаргана |
| Output export | Final CSV files гаргаж хадгална |
| Mini Q&A agent | Aggregate болон selected invoice fact-check questions-д хариулна |
| Optional Gradio UI | Presentation/demo-д ашиглах боломжтой demo interface өгнө |

---

## Тэмцээний шаардлагатай уялдсан байдал

| Competition Requirement | Project Implementation |
|---|---|
| Invoice images болон PDFs боловсруулах | PDF/JPG/PNG scanner + image conversion helpers |
| Invoice information extract хийх | Groq Vision JSON extraction |
| Invoice data validation хийх | SQLite master database validation |
| Suspicious invoice илрүүлэх | Amount mismatch, invalid date, bank mismatch, duplicate гэх мэт risk flags |
| Final decision оноох | `AUTO_POST`, `HUMAN_APPROVAL`, `DENY` decision engine |
| Aggregate questions-д хариулах | `final_results_df` болон `summary_df` дээр deterministic Mini Q&A Agent |
| Selected invoice questions-д хариулах | File name ашигласан invoice-level fact-check Q&A |
| Results export хийх | `/kaggle/working/` дотор CSV files |
| Reproducibility | Clear notebook sections, dependency install, config, output verification |
| Public project link | GitHub repository |
| Public notebook | Kaggle notebook link |

---

## Одоогийн repository бүтэц

Repository-ийн үндсэн бүтэц:

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

### File purpose

| File / Folder | Үүрэг |
|---|---|
| `README.md` | Main project documentation |
| `SUBMISSION_CHECKLIST.md` | Competition submission checklist |
| `ai-legends-2026.ipynb` | Kaggle / Jupyter notebook version of the pipeline |
| `invoice-automation-ai-agent-v3-ipynb.ipynb` | Repository доторх нэмэлт/final notebook version |
| `invoice_agent_core.py` | Reusable core Python pipeline logic |
| `app.py` | Demo UI entry point |
| `requirements.txt` | Python dependency list |
| `docs/` | Extra documentation and submission materials |

---

## Notebook Section Map

Uploaded notebook нь end-to-end pipeline агуулсан. Үндсэн section-үүд:

| Section | Name | Purpose |
|---|---|---|
| 1 | Competition Requirement Mapping | Competition requirement-ийг notebook section-тэй уялдуулна |
| 2 | Install Dependencies | Шаардлагатай Python libraries суулгана |
| 3 | Import Libraries | Python, data, image, AI packages import хийнэ |
| 4 | Configuration | Input path, output path, model name, limits тохируулна |
| 5 | Load Multiple Groq API Keys | Kaggle Secrets-ээс олон API key уншина |
| 6 | Auto-detect Dataset Files | Invoice files болон database files автоматаар илрүүлнэ |
| 7 | Load Master Database | SQLite tables-ийг pandas DataFrames болгон уншина |
| 8 | Master Data Helpers | Flexible column matching болон normalization helpers өгнө |
| 9 | Image/PDF Conversion Helpers | PDF page болон image-ийг model input-д бэлдэнэ |
| 10 | Vision-based Invoice Extraction | Groq Vision ашиглан structured invoice JSON гаргана |
| 11 | Field Normalization | Date, number, item, text fields цэвэрлэнэ |
| 12 | Category Classification | Historical болон keyword rules ашиглан category онооно |
| 13 | Validation Rules | Vendor, amount, date, bank, duplicate шалгана |
| 14 | Risk Flagging and Final Decision Logic | Validation result-ийг risk flags болон decision болгоно |
| 15 | Single Invoice Processing Function | Нэг invoice file-ийг end-to-end боловсруулна |
| 16 | Fast + Safe Batch Processing | Cache, failure handling ашиглан олон invoice боловсруулна |
| 17 | Result Consolidation and Output Export | Final CSV outputs үүсгэнэ |
| 18 | Mini Q&A Agent | Aggregate болон invoice-level questions-д хариулна |
| 19 | Final Output Verification | Output files, columns, consistency шалгана |
| 20 | Downloadable Final Output Package | Final CSV outputs агуулсан ZIP package үүсгэнэ |
| 21 | Optional Interactive Mini Q&A Chatbots | Optional console/Gradio demo interface |

---

## Системийн архитектур

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

## Бүрэн Processing Pipeline

### Pipeline overview

| Step | Module | Input | Processing | Output |
|---|---|---|---|---|
| 1 | File discovery | Kaggle input directory | `.pdf`, `.jpg`, `.jpeg`, `.png` хайна | Invoice file list |
| 2 | File filtering | Detected files | Evaluation folder байвал түүнийг сонгоно | Processing target list |
| 3 | Database discovery | Kaggle input directory | `master_invoices_database.db` хайна | SQLite database path |
| 4 | Database loading | SQLite file | pandas ашиглан бүх table уншина | Master dataframes |
| 5 | PDF/image conversion | Invoice file | PDF page-ийг image болгох эсвэл image file нээх | PIL image |
| 6 | Base64 encoding | PIL image | Image-ийг data URL болгоно | Vision model input |
| 7 | Vision extraction | Image data | Groq Vision model invoice fields extract хийнэ | Raw JSON |
| 8 | JSON parsing | Model response | Model output-оос valid JSON салган авна | Parsed dictionary |
| 9 | Field normalization | Raw fields | Dates, numbers, item lines, totals normalize хийнэ | Clean invoice dictionary |
| 10 | Category classification | Vendor/items/text | Historical invoice data болон keyword rules ашиглана | Category |
| 11 | Vendor validation | Vendor name | `Vendors` table-тэй fuzzy match хийнэ | Vendor registered status |
| 12 | Amount validation | Quantity, unit price, total | Amount дахин тооцож extracted total-той харьцуулна | Math correctness flag |
| 13 | Date validation | Invoice date, due date | Missing эсвэл invalid date шалгана | Date valid flag |
| 14 | Bank validation | Bank/account/vendor | Extracted bank account-ийг vendor master data-тай харьцуулна | Bank match flag |
| 15 | Duplicate detection | Invoice fields | Historical `Invoices` table-тэй харьцуулна | Duplicate flag |
| 16 | Risk flagging | Validation results | Risk flags онооно | Risk list |
| 17 | Decision routing | Risk flags | Business rules хэрэглэнэ | Final decision |
| 18 | Batch processing | All selected invoices | Cache болон failure handling-тэй боловсруулна | `results_df` |
| 19 | Consolidation | Batch dataframe | Judge-friendly flags болон summary columns нэмнэ | `final_results_df` |
| 20 | Export | Final dataframes | CSV files хадгална | Output files |
| 21 | Q&A agent | Final results | Aggregate болон invoice-specific questions-д хариулна | Text answers |
| 22 | Verification | Output files | Shape, count, consistency шалгана | Submission readiness status |

---

## Input Data

### Invoice files

Pipeline дараах extension-тэй invoice файлуудыг илрүүлнэ:

| Extension | Meaning |
|---|---|
| `.pdf` | PDF invoice |
| `.jpg` | JPEG invoice image |
| `.jpeg` | JPEG invoice image |
| `.png` | PNG invoice image |

### Auto-detected input locations

Project дараах location-уудаас invoice болон database хайна:

| Location | Purpose |
|---|---|
| `/kaggle/input` | Main Kaggle input root |
| `/kaggle/input/competitions/ai-legends-2026-ai-agents-automation` | Competition dataset directory |
| `eval_agent/eval_agent` | Final evaluation invoice folder байвал preferred folder |
| `./invoice` | Local invoice folder |
| `./invoices` | Local invoice folder |
| `./data/invoices` | Local data folder |
| `.` | Fallback current directory |

### Current notebook dataset detection

Uploaded notebook run дээр:

| Item | Value |
|---|---:|
| Detected invoice files | 200 |
| Detected database/data files | 1 |
| Preferred processing source | `eval_agent/eval_agent` |
| Selected processing files | 100 |

---

## Master Database Tables

Project дараах database ашиглана:

```text
master_invoices_database.db
```

Notebook дараах SQLite tables илрүүлсэн:

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

`Vendors` table нь бүртгэлтэй vendor мэдээллийг хадгална.

| Column | Description |
|---|---|
| `ID` | Unique vendor ID |
| `Name` | Registered vendor name |
| `Bank` | Registered bank name |
| `Account` | Registered bank account number |
| `Email` | Vendor email address |
| `RegisteredDate` | Vendor registration date |
| `Status` | Vendor status, жишээ нь active/inactive |

Example rows:

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

`Items` table нь item болон service нэр, category, unit price хадгална.

| Column | Description |
|---|---|
| `ID` | Unique item ID |
| `ItemName` | Registered item or service name |
| `UnitPrice` | Reference unit price |

Used for:

- extracted item description normalization,
- category classification,
- amount reasonableness check,
- historical item comparison.

Example item types:

| Item Type | Example |
|---|---|
| IT service | Server rental |
| Security service | SSL certificate |
| Office service | Office rental |
| Digital service | Software subscription |
| Maintenance | Technical support / repair |

---

### InvoiceCategories Table

`InvoiceCategories` table нь invoice category definition хадгална.

| Column | Description |
|---|---|
| `ID` | Unique category ID |
| `CategoryName` | Category name |
| `Description` | Category description |

Used for:

- category label mapping,
- historical category inference,
- keyword-based fallback classification.

Possible category examples:

| Category | Meaning |
|---|---|
| IT Services | Server, software, cloud, hosting, SSL |
| Office Expense | Rent, supplies, office services |
| Maintenance | Repair, support, technical service |
| Marketing | Advertisement, design, media service |
| Other | Uncategorized or unclear invoice type |

---

### Invoices Table

`Invoices` table нь historical invoice records хадгална. Энэ нь duplicate detection болон historical validation-д ашиглагдана.

| Column | Description |
|---|---|
| `ID` | Unique invoice record ID |
| `VendorName` | Vendor name |
| `InvoiceDate` | Invoice issue date |
| `DueDate` | Payment due date |
| `GrandTotal` | Final invoice total |
| `Category` | Invoice category |
| Other fields | Historical invoice metadata |

Validation usage:

| Check | Description |
|---|---|
| Duplicate check | Шинэ invoice-г historical records-той харьцуулна |
| Vendor history check | Vendor өмнө нь invoice өгч байсан эсэхийг шалгана |
| Amount comparison | Grand total historical invoice data-тай сэжигтэй эсэхийг харьцуулна |
| Category inference | Vendor болон item history дээр үндэслэн category санал болгоно |

---

### InvoiceLines Table

`InvoiceLines` table нь invoice line item records хадгална.

| Column | Description |
|---|---|
| `ID` | Unique line ID |
| `InvoiceID` | Parent invoice ID |
| `ItemID` | Linked item ID |
| `Quantity` | Item quantity |
| `UnitPrice` | Unit price |
| `LineTotal` | Line total amount |

Used for:

- line-level amount validation,
- item price comparison,
- item/category relation,
- historical invoice line checking.

---

## Extracted Invoice Schema

Vision model-оос дараах structured invoice fields гаргахыг зорьдог.

### Target extraction fields

| Field | Description |
|---|---|
| `invoice_number` | Invoice дугаар |
| `invoice_date` | Invoice гаргасан огноо |
| `due_date` | Төлбөр төлөх эцсийн огноо |
| `vendor_name` | Vendor/company нэр |
| `bank_name` | Invoice дээр бичигдсэн bank name |
| `bank_account` / `account_number` | Bank account number |
| `email` | Vendor email |
| `category` | Invoice category |
| `items` | Line items list |
| `quantity` | Quantity value |
| `unit_price` | Unit price value |
| `total_amount` / `grand_total` | Invoice total amount |
| `currency` | Currency, жишээ нь MNT |
| `notes` | Нэмэлт тайлбар эсвэл extracted note |

### Item schema

Each invoice item дараах бүтэцтэй байж болно:

| Field | Description |
|---|---|
| `description` | Item/service description |
| `quantity` | Quantity |
| `unit_price` | Unit price |
| `line_total` | Quantity × unit price |

---

## Field Normalization

Raw model output нь format-ийн хувьд тогтворгүй байж болно. Иймээс notebook дараах normalization хийнэ:

| Field Type | Normalization |
|---|---|
| Text | Extra spaces, quote, newline цэвэрлэнэ |
| Numbers | Comma, currency text, whitespace арилгаж float/int болгоно |
| Dates | Different date format-уудыг standard format болгоно |
| Vendor name | Fuzzy matching хийхэд бэлэн болгож normalize хийнэ |
| Bank account | Digit-only comparison хийхээр цэвэрлэнэ |
| Items | Single item болон list item format-ыг unified list болгоно |
| Missing values | Empty/null/unknown утгуудыг consistent байдлаар тэмдэглэнэ |

---

## Category Classification

Category classification нь 2 үндсэн эх үүсвэр ашиглана:

1. Historical invoice database дахь vendor/category information.
2. Extracted item text болон invoice text дээр keyword rule ашиглах.

### Category keyword examples

| Keyword Group | Possible Category |
|---|---|
| server, hosting, cloud, SSL, domain | IT Services |
| office, rent, supply, stationery | Office Expense |
| repair, maintenance, support | Maintenance |
| design, marketing, advertisement | Marketing |
| unknown / unclear | Other |

Category classification нь validation биш, харин invoice-г санхүүгийн ангилалд оруулах туслах layer юм.

---

## Validation Rules

Validation engine нь extracted invoice record-ийг master database болон deterministic business rules-тэй тулган шалгана.

---

### Vendor Validation

Vendor validation нь extracted vendor name-ийг `Vendors` table-тэй харьцуулна.

| Result | Meaning |
|---|---|
| `vendor_registered = True` | Vendor database-д бүртгэлтэй |
| `vendor_registered = False` | Vendor database-д олдоогүй |

Fuzzy matching ашигласнаар жижиг typo, spacing, OCR/model extraction variation-ийг тэсвэрлэнэ.

---

### Amount Validation

Amount validation нь line item эсвэл extracted numeric fields дээр үндэслэн total amount-г дахин тооцно.

Basic formula:

```text
calculated_total = quantity × unit_price
```

Дараа нь:

```text
calculated_total ≈ extracted_total_amount
```

| Result | Meaning |
|---|---|
| `math_correct = True` | Тооцоолол зөв эсвэл acceptable tolerance дотор байна |
| `math_correct = False` | Amount mismatch илэрсэн |

Amount mismatch нь `AMOUNT_MISMATCH` risk flag үүсгэнэ.

---

### Date Validation

Date validation дараах асуудлуудыг шалгана:

| Check | Description |
|---|---|
| Missing invoice date | Invoice date хоосон эсэх |
| Missing due date | Due date хоосон эсэх |
| Invalid date format | Огноо parse хийх боломжгүй эсэх |
| Due date before invoice date | Due date нь invoice date-ээс өмнө эсэх |
| Suspicious future/past date | Хэт сэжигтэй огноо эсэх |

Invalid date илэрвэл `INVALID_DATE` risk flag үүснэ.

---

### Bank Account Validation

Bank validation нь extracted bank account-ийг registered vendor database дахь bank/account мэдээлэлтэй харьцуулна.

| Result | Meaning |
|---|---|
| `bank_account_match = True` | Bank account vendor database-тэй таарч байна |
| `bank_account_match = False` | Bank account mismatch байна |
| `bank_account_match = Unknown` | Bank/account мэдээлэл дутуу байна |

Bank mismatch нь finance automation-д өндөр эрсдэлтэй тул `BANK_ACCOUNT_MISMATCH` risk flag онооно.

---

### Duplicate Detection

Duplicate detection нь шинэ invoice-г historical `Invoices` table-тэй харьцуулна.

Possible matching fields:

| Field | Purpose |
|---|---|
| `invoice_number` | Шууд duplicate илрүүлэх |
| `vendor_name` | Vendor context шалгах |
| `invoice_date` | Same period invoice шалгах |
| `grand_total` | Same amount invoice шалгах |
| `category` | Нэмэлт context |

Duplicate invoice нь `DUPLICATE` risk flag үүсгэнэ.

---

## Risk Flags

Risk flags нь invoice дээр илэрсэн асуудлыг standardized label хэлбэрээр хадгална.

| Risk Flag | Meaning |
|---|---|
| `NONE` | Илэрсэн risk байхгүй |
| `LOW_CONFIDENCE_EXTRACTION` | Extraction result итгэл багатай эсвэл incomplete |
| `EXTRACTION_FAILED` | AI extraction амжилтгүй болсон |
| `UNREGISTERED_VENDOR` | Vendor database-д бүртгэлгүй |
| `AMOUNT_MISMATCH` | Calculated amount болон extracted amount зөрсөн |
| `INVALID_DATE` | Date missing, invalid, эсвэл inconsistent |
| `BANK_ACCOUNT_MISMATCH` | Bank account vendor database-тэй таарахгүй |
| `DUPLICATE` | Invoice duplicate байж болзошгүй |

---

## Final Decision Logic

System invoice бүрт эцсийн decision онооно.

| Final Decision | Meaning | Typical Condition |
|---|---|---|
| `AUTO_POST` | Invoice автоматаар process хийж болно | Risk flag байхгүй, extraction амжилттай |
| `HUMAN_APPROVAL` | Хүний manual review хэрэгтэй | Extraction failed, low confidence, unregistered vendor, amount mismatch, uncertain data |
| `DENY` | Invoice автоматаар approve хийхгүй | Bank mismatch, duplicate гэх мэт serious risk |

### Current notebook consolidation-д ашигласан decision logic

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

Энэ logic нь uncertain invoice-г шууд approve хийхгүй, хүний review рүү шилжүүлдэг тул finance automation-д илүү аюулгүй.

---

## Output Files

Notebook final output-уудыг дараах folder дотор export хийнэ:

```text
/kaggle/working/
```

### Main output files

| File | Purpose |
|---|---|
| `all_results.csv` | Бүх processed invoice агуулсан main source-of-truth table |
| `clean_invoices.csv` | Зөвхөн `AUTO_POST` буюу clean invoices |
| `suspicious_invoices.csv` | Review эсвэл denial хэрэгтэй invoices |
| `failed_files.csv` | Extraction failed болсон боловч track хийсэн files |
| `aggregate_summary.csv` | Evaluation/report-д зориулсан one-row summary |
| `invoice_automation_final_outputs.zip` | Final CSV outputs агуулсан татаж авах ZIP package |

---

## Output Table Details

### `all_results.csv`

Энэ нь final result-ийн хамгийн гол table.

| Column | Description |
|---|---|
| `file_name` | Invoice file name |
| `file_path` | Full invoice file path |
| `file_type` | File extension, жишээ нь pdf/png/jpg |
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
| `extraction_status` | `SUCCESS` эсвэл `FAILED` |
| `final_decision` | `AUTO_POST`, `HUMAN_APPROVAL`, эсвэл `DENY` |
| `risk_flags` | Invoice дээр илэрсэн risk flags |
| `error_types` | Error/risk type summary |
| `denial_reason` | Denied invoice-ийн тайлбар |
| `failure_reason` | Extraction failed болсон шалтгаан |
| `vendor_registered` | Vendor бүртгэлтэй эсэх |
| `bank_account_match` | Bank account vendor database-тэй таарч байгаа эсэх |
| `math_correct` | Amount calculation зөв эсэх |
| `date_valid` | Date fields зөв эсэх |
| `is_duplicate` | Duplicate invoice эсэх |
| `needs_human_approval` | Human approval хэрэгтэй эсэх |
| `loaded_from_cache` | Result cache-ээс уншигдсан эсэх |
| `processed_at` | Processing timestamp |
| `has_amount_mismatch` | Amount mismatch boolean flag |
| `has_unregistered_vendor` | Unregistered vendor boolean flag |
| `has_invalid_date` | Invalid date boolean flag |
| `has_bank_account_mismatch` | Bank mismatch boolean flag |
| `has_duplicate` | Duplicate boolean flag |
| `has_extraction_failed` | Extraction failure boolean flag |
| `is_clean` | Clean invoice flag |
| `is_suspicious` | Suspicious invoice flag |

---

### `clean_invoices.csv`

Дараах нөхцлийг хангасан invoice-уудыг агуулна:

```text
final_decision == AUTO_POST
risk_flags == NONE
extraction_status != FAILED
```

Энэ file нь system автоматаар process хийж болно гэж үзсэн invoice-уудыг review хийхэд ашиглагдана.

---

### `suspicious_invoices.csv`

Дараах нөхцлүүдийн аль нэгийг хангасан invoice-уудыг агуулна:

```text
final_decision != AUTO_POST
risk_flags != NONE
extraction_status == FAILED
```

Энэ file нь manual review болон error analysis-д ашиглагдана.

---

### `failed_files.csv`

Extraction failed болсон эсвэл required fields найдвартай extract хийгдээгүй invoice-уудыг хадгална.

Important behavior:

- failed files ignore хийгдэхгүй,
- failed files final result table-д хадгалагдана,
- failed files `HUMAN_APPROVAL` рүү route хийгдэнэ.

Энэ нь finance automation system-д чухал. Учир нь system уншиж чадаагүй invoice-г алга болгох биш, human review рүү шилжүүлэх ёстой.

---

### `aggregate_summary.csv`

Aggregate count-ууд агуулсан one-row table.

| Column | Meaning |
|---|---|
| `total_invoices` | Нийт processed invoice count |
| `correct_invoices` | Correct/clean invoice count |
| `clean_invoices` | Clean invoice count |
| `suspicious_invoices` | Suspicious invoice count |
| `failed_files` | Failed extraction count |
| `auto_post_count` | `AUTO_POST` decision count |
| `human_approval_count` | `HUMAN_APPROVAL` decision count |
| `deny_count` | `DENY` decision count |
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

Uploaded notebook дээрх final verification result.

> Эдгээр count нь current notebook run-ийн үр дүн. Full dataset, private test files, API output, эсвэл config өөрчлөгдвөл өөрчлөгдөж болно.

### Processing summary

| Metric | Count |
|---|---:|
| Total selected invoices processed | 100 |
| Clean / correct invoices | 68 |
| Suspicious invoices | 32 |
| Failed extraction invoices | 6 |
| PDF invoices | 70 |
| Image invoices | 30 |
| Handwritten image invoices | 0 |

### Decision summary

| Final Decision | Count |
|---|---:|
| `AUTO_POST` | 68 |
| `HUMAN_APPROVAL` | 15 |
| `DENY` | 17 |
| Total | 100 |

### Risk summary

| Risk Type | Count |
|---|---:|
| Duplicate invoices | 10 |
| Amount mismatch | 6 |
| Unregistered vendor | 0 |
| Invalid date | 3 |
| Bank account mismatch | 8 |

### Output file shapes

| File | Shape |
|---|---:|
| `all_results.csv` | 100 rows × 58 columns |
| `clean_invoices.csv` | 68 rows × 58 columns |
| `suspicious_invoices.csv` | 32 rows × 58 columns |
| `failed_files.csv` | 6 rows × 58 columns |
| `aggregate_summary.csv` | 1 row × 16 columns |

### Final verification status

```text
FINAL STATUS: READY FOR SUBMISSION
```

---

## Mini Q&A Agent

Notebook дотор deterministic Mini Q&A Agent бий.

Энэ agent external LLM call хийхгүй. Хариултаа шууд дараах structured dataframe-үүдээс гаргана:

```text
final_results_df
summary_df
```

Иймээс Q&A output нь:

- stable,
- reproducible,
- exported CSV files-тай consistent,
- competition evaluation-д тохиромжтой.

### Supported aggregate questions

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

### Supported invoice-level fact check questions

Q&A agent нь file name ашиглан selected invoice асуултад хариулна.

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

### 1. Kaggle Notebook нээх

Public notebook:

```text
https://www.kaggle.com/code/temuulenmunkhochir/ai-legends-2026-final-ipynb
```

### 2. Competition Dataset нэмэх

Competition dataset notebook-д attached байгаа эсэхийг шалгана.

Expected input root:

```text
/kaggle/input/competitions/ai-legends-2026-ai-agents-automation
```

Notebook автоматаар дараах files хайна:

```text
.pdf
.jpg
.jpeg
.png
.db
.sqlite
.sqlite3
```

### 3. Groq API Keys-г Kaggle Secrets-д нэмэх

Uploaded notebook дараах secret names ашигласан:

| Secret Name |
|---|
| `groq_API_1_new` |
| `groq_API_2_new` |
| `groq_API_3_new` |
| `groq_API_4_new` |
| `groq_API_5_new` |

Recommended fallback names:

| Secret / Environment Name |
|---|
| `GROQ_API_KEY_1` |
| `GROQ_API_KEY_2` |
| `GROQ_API_KEY_3` |
| `GROQ_API_KEY_4` |
| `GROQ_API_KEY_5` |
| `GROQ_API_KEY` |
| `API` |

API key-г notebook code дотор шууд бичихгүй.

### 4. Run All Cells хийх

Notebook-ийг дээрээс нь доош нь run хийнэ.

Notebook дараах ажлуудыг хийнэ:

1. dependencies install хийнэ,
2. libraries import хийнэ,
3. input dataset scan хийнэ,
4. database load хийнэ,
5. invoice files сонгоно,
6. Groq Vision extraction ажиллуулна,
7. fields normalize хийнэ,
8. validation rules хэрэглэнэ,
9. risk flags онооно,
10. final decision гаргана,
11. CSV files export хийнэ,
12. Mini Q&A Agent ажиллуулна,
13. final output verification хийнэ.

### 5. Outputs татах

Kaggle output folder:

```text
/kaggle/working/
```

Download хийх гол files:

```text
all_results.csv
clean_invoices.csv
suspicious_invoices.csv
failed_files.csv
aggregate_summary.csv
invoice_automation_final_outputs.zip
```

---

## How to Run Locally

### 1. Repository clone хийх

```bash
git clone https://github.com/Temukk-dev/AI_Legends_2026.git
cd AI_Legends_2026
```

### 2. Virtual environment үүсгэх

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Dependencies install хийх

```bash
pip install -r requirements.txt
```

Хэрэв notebook дотор ажиллуулах бол dependency section-ийг run хийнэ.

### 4. API key тохируулах

Environment variable ашиглана:

Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your_groq_api_key_here"
```

Linux / macOS:

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

### 5. Local data folder бэлдэх

Жишээ бүтэц:

```text
AI_Legends_2026/
│
├── data/
│   ├── invoices/
│   │   ├── invoice_001.pdf
│   │   ├── invoice_002.jpg
│   │   └── invoice_003.png
│   │
│   └── master_invoices_database.db
```

### 6. Core pipeline ажиллуулах

Хэрэв `invoice_agent_core.py` entry point бэлэн бол:

```bash
python invoice_agent_core.py
```

Эсвэл Jupyter Notebook ашиглана:

```bash
jupyter notebook
```

Дараа нь notebook файлыг нээж бүх cell-ийг run хийнэ.

### 7. Demo app ажиллуулах

Хэрэв `app.py` Gradio/Streamlit UI ашиглаж байгаа бол:

```bash
python app.py
```

Browser дээр гарсан local URL-ийг нээнэ.

---

## Demo UI

Repository дотор optional demo UI entry file:

```text
app.py
```

Demo UI-ийн зорилго:

- project workflow-г visual байдлаар харуулах,
- invoice automation agent-ийн pipeline тайлбарлах,
- sample result preview харуулах,
- GitHub/Kaggle/Writeup/Demo links байрлуулах,
- presentation болон demo video-д ашиглах.

Possible UI sections:

| Section | Purpose |
|---|---|
| Hero section | Project title, subtitle, main callout |
| Pipeline section | PDF/JPG/PNG → Groq Vision → Validation → Decision |
| Metrics section | Total invoices, clean, suspicious, deny, human approval |
| Output preview | CSV result table preview |
| Q&A section | Aggregate question examples |
| Links section | Kaggle Notebook, GitHub, Demo Video, Writeup |

---

## Configuration

### Main notebook config

Typical config variables:

| Config | Purpose |
|---|---|
| `INPUT_ROOT` | Kaggle/local input root |
| `OUTPUT_DIR` | CSV output folder |
| `MODEL_NAME` | Groq vision model name |
| `MAX_INVOICES` | Processing limit |
| `CACHE_DIR` | Cache directory |
| `USE_CACHE` | Cache ашиглах эсэх |
| `API_KEY_NAMES` | Kaggle Secrets key names |
| `SUPPORTED_EXTENSIONS` | Supported invoice file extensions |

Example:

```python
SUPPORTED_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png"]
OUTPUT_DIR = "/kaggle/working"
```

---

## Dependencies

Main libraries:

| Package | Purpose |
|---|---|
| `pandas` | DataFrame processing and CSV export |
| `numpy` | Numeric operations |
| `sqlite3` | SQLite database loading |
| `Pillow` | Image file handling |
| `PyMuPDF` / `fitz` | PDF to image conversion |
| `groq` | Groq API client |
| `json` | JSON parsing |
| `base64` | Image encoding for vision API |
| `pathlib` | File path handling |
| `datetime` | Timestamp and date handling |
| `difflib` | Fuzzy matching helpers |
| `gradio` | Optional demo UI |

Install example:

```bash
pip install pandas numpy pillow pymupdf groq gradio
```

---

## Cache System

### Purpose

Cache system нь өмнө боловсруулсан invoice result-ийг хадгалж, дахин run хийх үед API call багасгана.

### Cache location

Typical cache folder:

```text
/kaggle/working/invoice_cache
```

эсвэл local:

```text
./cache
```

### Cache behavior

| Behavior | Description |
|---|---|
| Cache hit | Өмнө боловсруулсан result cache-ээс уншина |
| Cache miss | Invoice-г Groq Vision model руу илгээнэ |
| Loaded from cache flag | `loaded_from_cache` column-д хадгална |
| Safe rerun | Notebook дахин run хийхэд time болон API usage буурна |

---

## Failure Handling

System extraction failed болсон invoice-ийг алгасахгүй.

| Failure Case | Handling |
|---|---|
| API error | Error message хадгалж failed record үүсгэнэ |
| Invalid JSON | Parsing failure гэж тэмдэглэнэ |
| Image conversion error | File conversion failure гэж тэмдэглэнэ |
| Missing required fields | Low confidence/incomplete extraction гэж тэмдэглэнэ |
| Unknown file issue | `failure_reason` column-д тайлбар хадгална |

Final behavior:

```text
Failed invoice → final_decision = HUMAN_APPROVAL
```

Энэ нь safety-oriented design юм. Систем уншиж чадаагүй invoice-г автоматаар approve хийхгүй.

---

## Security Notes

| Security Area | Practice |
|---|---|
| API keys | Kaggle Secrets эсвэл environment variables ашиглана |
| Hardcoded secrets | Repository болон notebook дотор API key шууд бичихгүй |
| Output data | CSV files нь structured invoice result тул public хийхээс өмнө шалгана |
| Private dataset | Competition private data-г repository-д upload хийхгүй |
| Cache files | Sensitive extraction result агуулах боломжтой тул public repo-д commit хийхгүй |
| Database file | Хэрэв competition dataset private бол database file-г repo-д оруулахгүй |

Recommended `.gitignore`:

```gitignore
.env
*.key
cache/
outputs/
*.db
*.sqlite
*.sqlite3
/kaggle/
__pycache__/
.ipynb_checkpoints/
```

---

## Known Limitations

| Limitation | Description |
|---|---|
| Vision model dependency | Extraction quality нь Groq Vision model output-оос хамаарна |
| API rate limit | Олон invoice боловсруулах үед API limit нөлөөлж болно |
| OCR/layout complexity | Маш муу scan, handwritten, blurred invoice дээр extraction алдаа гарч болно |
| Database schema variation | Column нэр өөрчлөгдвөл helper logic update шаардлагатай байж болно |
| Category ambiguity | Зарим invoice category keyword/history дутуугаас unclear байж болно |
| Bank validation | Vendor database-д bank data дутуу бол validation uncertain болно |
| Duplicate detection | Perfect duplicate detection хийхэд илүү олон unique keys хэрэгтэй |
| Handwritten invoices | Current run дээр handwritten image count 0 байсан |

---

## Future Improvements

| Improvement | Benefit |
|---|---|
| Stronger OCR fallback | Vision extraction failed үед backup extraction нэмнэ |
| Layout-aware extraction | Table/line item extraction илүү сайжирна |
| Confidence scoring | Field-level confidence score хадгална |
| Better duplicate algorithm | Invoice number, vendor, amount, date similarity-г weighted score болгоно |
| More detailed denial reasons | Finance user-д ойлгомжтой reason generation сайжирна |
| Web dashboard | CSV result-ийг interactive dashboard дээр үзүүлнэ |
| Human review workflow | Manual approval UI нэмнэ |
| Audit trail | Decision бүрийн rule trace хадгална |
| Multi-language support | Mongolian/English invoice field extraction сайжруулна |
| Unit tests | Validation functions дээр tests нэмнэ |

---

## Submission Checklist

Competition submission-д шаардлагатай гол зүйлс:

| Requirement | Status | Notes |
|---|---|---|
| Public Kaggle Notebook | Ready | Notebook link provided |
| Public GitHub Repository | Ready | Repository link provided |
| Kaggle Writeup | Pending | Writeup link нэмэх шаардлагатай |
| Demo Video | Pending | 3 минут хүртэл YouTube/Loom video link нэмэх шаардлагатай |
| Demo Website / Project Link | Optional/Pending | GitHub repo project link-ийн үүргийг гүйцэтгэж болно |
| CSV Outputs | Ready in notebook | `/kaggle/working/` дотор үүснэ |
| Aggregate Q&A | Ready | Mini Q&A Agent section |
| Invoice-level Q&A | Ready | File-specific fact-check questions |
| Validation Logic | Ready | Vendor, amount, date, bank, duplicate checks |
| Final Decision Logic | Ready | AUTO_POST / HUMAN_APPROVAL / DENY |

---

## Recommended Demo Video Script Outline

3 минут хүртэл demo video-д дараах бүтэц тохиромжтой.

### 0:00–0:20 — Introduction

```text
Hello, this is my project for AI Legends 2026.
The project name is Invoice Automation AI Agent.
It processes PDF and image invoices, extracts structured data, validates them against a master database, detects risks, and gives final decisions.
```

### 0:20–0:55 — Pipeline explanation

```text
The pipeline starts from PDF, JPG, and PNG invoice files.
The system converts files into model-ready images, sends them to Groq Vision for field extraction, normalizes the extracted data, and validates the result against the SQLite master database.
```

### 0:55–1:40 — Validation and decision

```text
The validation engine checks registered vendors, bank account mismatches, date problems, duplicate invoices, and amount calculation errors.
Based on the risk flags, the system assigns AUTO_POST, HUMAN_APPROVAL, or DENY.
```

### 1:40–2:20 — Results

```text
In the current notebook run, the system processed 100 selected invoices.
68 invoices were clean, 32 were suspicious, 15 required human approval, and 17 were denied.
The system also exported CSV files for all results, clean invoices, suspicious invoices, failed files, and aggregate summary.
```

### 2:20–2:50 — Q&A and reproducibility

```text
The notebook includes a mini Q&A agent that answers aggregate questions and selected invoice fact-check questions directly from the final results dataframe.
This makes the answers consistent with the exported CSV files.
```

### 2:50–3:00 — Closing

```text
The public notebook and source code are available through Kaggle and GitHub.
Thank you.
```

---

## Project Status

| Area | Status |
|---|---|
| Invoice file detection | Complete |
| PDF/image conversion | Complete |
| Groq Vision extraction | Complete |
| Field normalization | Complete |
| SQLite database loading | Complete |
| Vendor validation | Complete |
| Amount validation | Complete |
| Date validation | Complete |
| Bank account validation | Complete |
| Duplicate detection | Complete |
| Risk flagging | Complete |
| Final decision routing | Complete |
| CSV export | Complete |
| Mini Q&A Agent | Complete |
| Final output verification | Complete |
| README documentation | Complete |
| Demo video | Pending |
| Kaggle writeup | Pending |

---

## Author

**Temukk-dev**

Project repository:

```text
https://github.com/Temukk-dev/AI_Legends_2026
```

Kaggle notebook:

```text
https://www.kaggle.com/code/temuulenmunkhochir/ai-legends-2026-final-ipynb
```

---

## License

This repository is created for educational and competition purposes.

If reused, please cite the project repository and original author.

---

## Notes for Judges

This project focuses on building a reproducible finance automation agent rather than only a single extraction script.

Main design priorities:

- safe invoice processing,
- structured result consistency,
- database-backed validation,
- deterministic risk detection,
- explainable final decisions,
- reproducible CSV outputs,
- aggregate and invoice-level Q&A support.

The system intentionally routes uncertain or failed invoices to `HUMAN_APPROVAL` instead of silently ignoring them or automatically approving them. This makes the workflow safer for real finance automation scenarios.
