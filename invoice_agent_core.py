from __future__ import annotations

import base64
import io
import json
import os
import re
import sqlite3
import time
import traceback
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from PIL import Image
from rapidfuzz import fuzz, process

try:
    import fitz  # type: ignore
except Exception:  # pragma: no cover - optional dependency in local environments
    fitz = None

try:
    from groq import Groq  # type: ignore
except Exception:  # pragma: no cover - optional dependency in local environments
    Groq = None


ALLOWED_FILE_SUFFIXES = {".pdf", ".jpg", ".jpeg", ".png"}
GROQ_VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
DEFAULT_MAX_PDF_PAGES = 2
LOW_CONFIDENCE_THRESHOLD = 0.60
REQUIRED_RISK_FLAGS = [
    "AMOUNT_MISMATCH",
    "UNREGISTERED_VENDOR",
    "INVALID_DATE",
    "BANK_ACCOUNT_MISMATCH",
    "DUPLICATE",
    "HANDWRITTEN_IMAGE",
    "LOW_CONFIDENCE_EXTRACTION",
    "MISSING_REQUIRED_FIELD",
]
DENY_FLAGS = {"AMOUNT_MISMATCH", "BANK_ACCOUNT_MISMATCH", "DUPLICATE", "INVALID_DATE"}
HUMAN_APPROVAL_FLAGS = {
    "UNREGISTERED_VENDOR",
    "HANDWRITTEN_IMAGE",
    "LOW_CONFIDENCE_EXTRACTION",
    "MISSING_REQUIRED_FIELD",
}
FINAL_RESULT_COLUMNS = [
    "file_name",
    "file_path",
    "file_type",
    "is_image",
    "is_pdf",
    "is_handwritten_image",
    "invoice_number",
    "vendor_name",
    "invoice_date",
    "due_date",
    "category",
    "quantity",
    "unit_price",
    "calculated_total",
    "extracted_total",
    "math_is_correct",
    "bank_name",
    "bank_account",
    "bank_account_registered",
    "vendor_registered",
    "is_duplicate",
    "is_correct_invoice",
    "is_suspicious",
    "risk_flags",
    "error_types",
    "final_decision",
    "decision_reason",
    "human_approval_required",
    "processing_status",
    "extraction_confidence",
    "raw_extracted_text",
]
REQUIRED_FIELDS_FOR_RISK = [
    "invoice_number",
    "vendor_name",
    "invoice_date",
    "due_date",
    "extracted_total",
    "bank_name",
    "bank_account",
]
CATEGORY_KEYWORDS = {
    "Түрээсийн зардал": ["түрээс", "warehouse", "office rent", "агуулах", "оффис түрээс"],
    "Ашиглалтын зардал": ["цахилгаан", "дулаан", "ус", "цэвэрлэгээ", "ашиглалт", "харуул"],
    "Мэдээллийн технологийн зардал": [
        "сервер",
        "hosting",
        "ssl",
        "software",
        "domain",
        "cloud",
        "api",
        "license",
        "лиценз",
        "it",
        "кибер",
        "вэб",
        "интернет",
    ],
    "Маркетинг, сурталчилгааны зардал": ["marketing", "advertising", "сурталчилгаа", "постер", "video", "дизайн"],
    "Ложистик, тээврийн зардал": ["тээвэр", "логистик", "delivery", "courier", "shipping"],
    "Хөдөлмөр, гэрээт үйлчилгээний зардал": ["consulting", "training", "service", "audit", "хөлс", "үйлчилгээ"],
}
FACT_CHECK_SUPPORTED_QUESTIONS = [
    "final decision юу вэ?",
    "duplicate мөн үү?",
    "vendor-ийн нэр юу вэ?",
    "ямар category-д ангилагдсан бэ?",
    "due date хэд вэ?",
    "bank account бүртгэлтэй эсэх?",
    "яагаад deny болсон бэ?",
    "ямар төрлийн алдаа илэрсэн бэ?",
    "human approval авах ёстой юу?",
    "математик тооцоолол зөв үү?",
]
AGGREGATE_QUESTIONS = [
    "Нийт хэдэн invoice байна вэ?",
    "Хэдэн invoice зөв invoice вэ?",
    "Хэдэн invoice сэжигтэй вэ?",
    "Хэдэн invoice duplicate вэ?",
    "Хэдэн invoice математик тооцооллын алдаатай вэ?",
    "Хэдэн invoice бүртгэлгүй vendor-той вэ?",
    "Хэдэн invoice буруу огноотой вэ?",
    "Хэдэн invoice банкны мэдээллийн зөрүүтэй вэ?",
    "Хэдэн invoice зураг хэлбэртэй вэ?",
    "Хэдэн invoice гар бичмэлтэй зураг вэ?",
    "Хэдэн invoice HUMAN_APPROVAL авах ёстой вэ?",
    "Хэдэн invoice DENY болох ёстой вэ?",
]


@dataclass
class ProjectPaths:
    data_root: Path
    output_dir: Path
    db_path: Optional[Path]
    final_results_path: Path
    failed_files_path: Path
    aggregate_answers_path: Path


@dataclass
class MasterData:
    raw_tables: Dict[str, pd.DataFrame]
    vendors_df: Optional[pd.DataFrame]
    items_df: Optional[pd.DataFrame]
    categories_df: Optional[pd.DataFrame]
    historical_invoices_df: Optional[pd.DataFrame]


def normalize_text(value: Any) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return ""
    return re.sub(r"\s+", " ", str(value).strip().lower())


def normalize_number(value: Any) -> Optional[float]:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    text = str(value).strip()
    if not text:
        return None
    text = text.replace(",", "").replace("₮", "").replace("MNT", "").replace("mnt", "")
    text = re.sub(r"[^0-9.\-]", "", text)
    if text in {"", "-", ".", "-."}:
        return None
    try:
        return float(text)
    except Exception:
        return None


def normalize_bool(value: Any) -> Optional[bool]:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return value
    text = normalize_text(value)
    if text in {"true", "1", "yes", "y", "тийм", "үнэн"}:
        return True
    if text in {"false", "0", "no", "n", "үгүй", "худал"}:
        return False
    return None


def normalize_date(value: Any) -> Optional[str]:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    text = str(value).strip()
    if not text:
        return None

    cleaned = text
    cleaned = cleaned.replace("он", "-").replace("сар", "-").replace("өдөр", "")
    cleaned = cleaned.replace("year", "-").replace("month", "-").replace("day", "")
    cleaned = re.sub(r"[./]", "-", cleaned)
    cleaned = re.sub(r"\s+", "", cleaned)
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")

    candidates = [cleaned]
    match = re.search(r"(20\d{2}|19\d{2})[-]?(\d{1,2})[-]?(\d{1,2})", cleaned)
    if match:
        candidates.insert(0, f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}")

    for candidate in candidates:
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y", "%Y-%d-%m"):
            try:
                return datetime.strptime(candidate, fmt).date().isoformat()
            except Exception:
                continue
        try:
            return pd.to_datetime(candidate, errors="raise").date().isoformat()
        except Exception:
            continue
    return None


def round_or_none(value: Optional[float], digits: int = 2) -> Optional[float]:
    if value is None:
        return None
    return round(float(value), digits)


def split_pipe_values(value: Any) -> List[str]:
    if value is None or value == "" or (isinstance(value, float) and np.isnan(value)):
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    text = str(value)
    return [item.strip() for item in text.split("|") if item.strip()]


def join_pipe_values(values: Sequence[str]) -> str:
    unique_values: List[str] = []
    for value in values:
        if value and value not in unique_values:
            unique_values.append(value)
    return "|".join(unique_values)


def add_unique(values: List[str], value: Optional[str]) -> None:
    if value and value not in values:
        values.append(value)


def find_column(df: Optional[pd.DataFrame], candidates: Sequence[str]) -> Optional[str]:
    if df is None or df.empty:
        return None
    lowered = {str(column).lower(): column for column in df.columns}
    for candidate in candidates:
        if candidate.lower() in lowered:
            return lowered[candidate.lower()]
    for column in df.columns:
        normalized_column = normalize_text(column).replace("_", "").replace(" ", "")
        for candidate in candidates:
            normalized_candidate = normalize_text(candidate).replace("_", "").replace(" ", "")
            if normalized_candidate in normalized_column or normalized_column in normalized_candidate:
                return column
    return None


def get_table(raw_tables: Dict[str, pd.DataFrame], possible_names: Sequence[str]) -> Optional[pd.DataFrame]:
    if not raw_tables:
        return None
    lowered = {table_name.lower(): table_name for table_name in raw_tables}
    for name in possible_names:
        if name.lower() in lowered:
            return raw_tables[lowered[name.lower()]]
    for table_name, table_df in raw_tables.items():
        table_name_lower = table_name.lower()
        if any(name.lower() in table_name_lower for name in possible_names):
            return table_df
    return None


def is_kaggle_runtime() -> bool:
    return Path("/kaggle").exists()


def discover_output_dir(preferred_output_dir: Optional[Path] = None) -> Path:
    if preferred_output_dir is not None:
        output_dir = Path(preferred_output_dir)
    elif Path("/kaggle/working").exists():
        output_dir = Path("/kaggle/working")
    else:
        output_dir = Path("./outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def discover_search_roots(preferred_input_root: Optional[Path] = None) -> List[Path]:
    roots: List[Path] = []
    candidates = [
        preferred_input_root,
        Path("./invoice") if Path("./invoice").exists() else None,
        Path("./invoices") if Path("./invoices").exists() else None,
        Path("/kaggle/input") if Path("/kaggle/input").exists() else None,
        Path("./data/invoices") if Path("./data/invoices").exists() else None,
        Path("."),
    ]
    for candidate in candidates:
        if candidate is None:
            continue
        resolved = Path(candidate).resolve()
        if resolved.exists() and resolved not in roots:
            roots.append(resolved)
    return roots


def scan_invoice_files(search_roots: Sequence[Path], max_files: Optional[int] = None) -> List[Path]:
    files: List[Path] = []
    excluded_parts = {"outputs", "docs", "notebooks", ".ipynb_checkpoints", "__pycache__"}
    for root in search_roots:
        for suffix in ALLOWED_FILE_SUFFIXES:
            for file_path in root.rglob(f"*{suffix}"):
                lower_parts = {part.lower() for part in file_path.parts}
                if lower_parts.intersection(excluded_parts):
                    continue
                files.append(file_path.resolve())
            for file_path in root.rglob(f"*{suffix.upper()}"):
                lower_parts = {part.lower() for part in file_path.parts}
                if lower_parts.intersection(excluded_parts):
                    continue
                files.append(file_path.resolve())
    unique_files = sorted({file_path for file_path in files})
    if max_files is not None:
        unique_files = unique_files[:max_files]
    return unique_files


def discover_database_path(search_roots: Sequence[Path]) -> Optional[Path]:
    preferred_names = [
        "master_invoices_database.db",
        "master_invoices_database.sqlite",
        "master_invoices_database.sqlite3",
    ]
    candidates: List[Path] = []
    for root in search_roots:
        for preferred_name in preferred_names:
            preferred_path = root / preferred_name
            if preferred_path.exists():
                return preferred_path.resolve()
        for pattern in ("*.db", "*.sqlite", "*.sqlite3"):
            candidates.extend(path.resolve() for path in root.rglob(pattern))
    if not candidates:
        return None
    candidates = sorted({path for path in candidates})
    return candidates[0]


def build_project_paths(
    preferred_input_root: Optional[Path] = None,
    preferred_output_dir: Optional[Path] = None,
) -> ProjectPaths:
    search_roots = discover_search_roots(preferred_input_root=preferred_input_root)
    data_root = search_roots[0] if search_roots else Path(".").resolve()
    output_dir = discover_output_dir(preferred_output_dir=preferred_output_dir)
    db_path = discover_database_path(search_roots)
    return ProjectPaths(
        data_root=data_root,
        output_dir=output_dir,
        db_path=db_path,
        final_results_path=output_dir / "final_results.csv",
        failed_files_path=output_dir / "failed_files.csv",
        aggregate_answers_path=output_dir / "aggregate_answers.csv",
    )


def load_groq_api_keys() -> List[str]:
    keys: List[str] = []
    # Keep compatibility with the notebook config, which advertises a generic
    # `API` fallback in addition to the explicit Groq names.
    secret_names = [f"GROQ_API_KEY_{index}" for index in range(1, 6)] + ["GROQ_API_KEY", "API"]

    try:
        from kaggle_secrets import UserSecretsClient  # type: ignore

        user_secrets = UserSecretsClient()
        for secret_name in secret_names:
            try:
                value = user_secrets.get_secret(secret_name)
            except Exception:
                value = None
            if value and value not in keys:
                keys.append(value)
    except Exception:
        pass

    for secret_name in secret_names:
        value = os.environ.get(secret_name)
        if value and value not in keys:
            keys.append(value)

    return keys


def load_sqlite_database(db_path: Optional[Path]) -> Dict[str, pd.DataFrame]:
    tables: Dict[str, pd.DataFrame] = {}
    if db_path is None or not Path(db_path).exists():
        return tables

    connection = sqlite3.connect(str(db_path))
    try:
        table_names = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;",
            connection,
        )["name"].tolist()
        for table_name in table_names:
            try:
                tables[table_name] = pd.read_sql_query(f'SELECT * FROM "{table_name}"', connection)
            except Exception:
                continue
    finally:
        connection.close()
    return tables


def load_master_data(db_path: Optional[Path]) -> MasterData:
    raw_tables = load_sqlite_database(db_path)
    return MasterData(
        raw_tables=raw_tables,
        vendors_df=get_table(raw_tables, ["Vendors", "Vendor", "Suppliers"]),
        items_df=get_table(raw_tables, ["Items", "Item"]),
        categories_df=get_table(raw_tables, ["InvoiceCategories", "Categories", "Category"]),
        historical_invoices_df=get_table(raw_tables, ["Invoices", "Invoice", "HistoricalInvoices"]),
    )


def image_to_data_url(image: Image.Image, max_size: int = 1600) -> str:
    image = image.convert("RGB")
    width, height = image.size
    scale = min(max_size / max(width, height), 1.0)
    if scale < 1.0:
        image = image.resize((int(width * scale), int(height * scale)))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=90)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


def file_to_images(file_path: Path, max_pdf_pages: int = DEFAULT_MAX_PDF_PAGES) -> List[Image.Image]:
    suffix = file_path.suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png"}:
        return [Image.open(file_path).convert("RGB")]

    if suffix == ".pdf":
        if fitz is None:
            raise RuntimeError("PyMuPDF (fitz) байхгүй тул PDF image render хийх боломжгүй байна.")
        document = fitz.open(str(file_path))
        images: List[Image.Image] = []
        try:
            page_limit = min(len(document), max_pdf_pages)
            for page_index in range(page_limit):
                page = document[page_index]
                pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                images.append(Image.open(io.BytesIO(pixmap.tobytes("png"))).convert("RGB"))
        finally:
            document.close()
        return images

    raise ValueError(f"Unsupported file type: {file_path.suffix}")


def extract_pdf_text(file_path: Path, max_pdf_pages: int = DEFAULT_MAX_PDF_PAGES) -> str:
    if file_path.suffix.lower() != ".pdf":
        return ""
    if fitz is None:
        return ""
    document = fitz.open(str(file_path))
    try:
        text_chunks = []
        for page_index in range(min(len(document), max_pdf_pages)):
            text_chunks.append(document[page_index].get_text("text"))
        return "\n".join(text_chunks).strip()
    finally:
        document.close()


def extract_json_from_text(text: str) -> Dict[str, Any]:
    if not text:
        return {}
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {}

    candidate = match.group(0)
    try:
        return json.loads(candidate)
    except Exception:
        return {}


def call_groq_with_fallback(
    messages: List[Dict[str, Any]],
    api_keys: Sequence[str],
    model: str = GROQ_VISION_MODEL,
    max_tokens: int = 2400,
) -> str:
    if Groq is None:
        raise RuntimeError("groq package install хийгдээгүй байна.")
    if not api_keys:
        raise RuntimeError("Groq API key олдсонгүй.")

    last_error: Optional[Exception] = None
    for api_key in api_keys:
        try:
            client = Groq(api_key=api_key, max_retries=1, timeout=60)
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0,
                max_completion_tokens=max_tokens,
            )
            return response.choices[0].message.content or ""
        except Exception as error:  # pragma: no cover - external API call
            last_error = error
            time.sleep(1.5)
    raise RuntimeError(f"Бүх Groq API key амжилтгүй боллоо: {last_error}")


EXTRACTION_SYSTEM_PROMPT = """
You are an invoice extraction and validation assistant.
Read the invoice image carefully and return ONLY valid JSON.
No markdown. No explanation.
If a value is unknown, use null.
"""

EXTRACTION_USER_PROMPT = """
Extract the invoice into this exact JSON schema:
{
  "invoice_number": null,
  "vendor_name": null,
  "invoice_date": null,
  "due_date": null,
  "bank_name": null,
  "bank_account": null,
  "quantity": null,
  "unit_price": null,
  "extracted_total": null,
  "items": [
    {
      "description": null,
      "quantity": null,
      "unit_price": null,
      "line_total": null
    }
  ],
  "is_handwritten_image": false,
  "is_correct_invoice": true,
  "extraction_confidence": 0.0,
  "raw_extracted_text": ""
}

Rules:
- Preserve Mongolian vendor names exactly as written.
- Convert money, quantity, and unit_price to numbers when possible.
- Dates should be ISO format YYYY-MM-DD when possible.
- Set is_handwritten_image=true only if handwriting is clearly visible.
- Set is_correct_invoice=true only if the document is actually an invoice/bill.
- raw_extracted_text should contain the important invoice text content you used.
- Return JSON only.
"""


def extract_invoice_with_groq(
    file_path: Path,
    api_keys: Sequence[str],
    pdf_text_hint: Optional[str] = None,
    max_pdf_pages: int = DEFAULT_MAX_PDF_PAGES,
) -> Dict[str, Any]:
    images = file_to_images(file_path, max_pdf_pages=max_pdf_pages)
    content: List[Dict[str, Any]] = [{"type": "text", "text": EXTRACTION_USER_PROMPT}]
    if pdf_text_hint:
        content.append(
            {
                "type": "text",
                "text": f"Optional text hint extracted from the file:\n{pdf_text_hint[:5000]}",
            }
        )
    for image in images:
        content.append({"type": "image_url", "image_url": {"url": image_to_data_url(image)}})

    raw_response = call_groq_with_fallback(
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        api_keys=api_keys,
    )
    parsed = extract_json_from_text(raw_response)
    parsed["_raw_model_response"] = raw_response
    parsed["_extraction_source"] = "groq_vision"
    parsed["_json_parse_failed"] = not bool(parsed)
    return parsed


def regex_search(patterns: Sequence[str], text: str) -> Optional[str]:
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
    return None


def parse_items_from_pdf_lines(lines: Sequence[str]) -> List[Dict[str, Any]]:
    start_index = None
    total_label_index = None
    for index, line in enumerate(lines):
        normalized_line = normalize_text(line)
        if normalized_line == "нийт":
            start_index = index + 1
        if "нийт төлбөр" in normalized_line:
            total_label_index = index
            break
    if start_index is None or total_label_index is None or total_label_index <= start_index:
        return []

    item_lines = [line for line in lines[start_index:total_label_index] if line.strip()]
    items: List[Dict[str, Any]] = []
    for chunk_start in range(0, len(item_lines), 4):
        chunk = item_lines[chunk_start : chunk_start + 4]
        if len(chunk) < 4:
            continue
        items.append(
            {
                "description": chunk[0],
                "quantity": normalize_number(chunk[1]),
                "unit_price": normalize_number(chunk[2]),
                "line_total": normalize_number(chunk[3]),
            }
        )
    return items


def heuristic_extract_from_pdf_text(file_path: Path, pdf_text: str) -> Dict[str, Any]:
    lines = [line.strip() for line in pdf_text.splitlines() if line.strip()]
    items = parse_items_from_pdf_lines(lines)

    invoice_number = regex_search(
        [r"Нэхэмжлэл\s*#:\s*([^\n]+)", r"Invoice\s*#:\s*([^\n]+)"],
        pdf_text,
    )
    vendor_name = None
    for index, line in enumerate(lines):
        if "vendor" in normalize_text(line) or "нэхэмжлэгч" in normalize_text(line):
            if index + 1 < len(lines):
                vendor_name = lines[index + 1]
            break

    quantity = None
    unit_price = None
    if items:
        quantity = sum(item["quantity"] for item in items if item.get("quantity") is not None)
        unit_prices = [item["unit_price"] for item in items if item.get("unit_price") is not None]
        unit_price = unit_prices[0] if unit_prices else None

    essential_hits = sum(
        1
        for value in [
            invoice_number,
            vendor_name,
            regex_search([r"Нэхэмжлэлийн огноо:\s*([^\n]+)", r"Invoice Date:\s*([^\n]+)"], pdf_text),
            regex_search([r"Төлөх хугацаа:\s*([^\n]+)", r"Due Date:\s*([^\n]+)"], pdf_text),
            regex_search([r"Банк:\s*([^\n]+)", r"Bank:\s*([^\n]+)"], pdf_text),
            regex_search([r"Данс:\s*([^\n]+)", r"Account:\s*([^\n]+)"], pdf_text),
            regex_search([r"НИЙТ ТӨЛБӨР:\s*([^\n]+)", r"TOTAL:\s*([^\n]+)"], pdf_text),
        ]
        if value
    )
    confidence = 0.50 + min(essential_hits, 7) * 0.06

    return {
        "invoice_number": invoice_number,
        "vendor_name": vendor_name,
        "invoice_date": regex_search([r"Нэхэмжлэлийн огноо:\s*([^\n]+)", r"Invoice Date:\s*([^\n]+)"], pdf_text),
        "due_date": regex_search([r"Төлөх хугацаа:\s*([^\n]+)", r"Due Date:\s*([^\n]+)"], pdf_text),
        "bank_name": regex_search([r"Банк:\s*([^\n]+)", r"Bank:\s*([^\n]+)"], pdf_text),
        "bank_account": regex_search([r"Данс:\s*([^\n]+)", r"Account:\s*([^\n]+)"], pdf_text),
        "quantity": quantity,
        "unit_price": unit_price,
        "extracted_total": regex_search([r"НИЙТ ТӨЛБӨР:\s*([^\n]+)", r"TOTAL:\s*([^\n]+)"], pdf_text),
        "items": items,
        "is_handwritten_image": False,
        "is_correct_invoice": any(token in normalize_text(pdf_text) for token in ["нэхэмжлэл", "invoice"]),
        "extraction_confidence": round(min(confidence, 0.96), 2),
        "raw_extracted_text": pdf_text,
        "_raw_model_response": None,
        "_extraction_source": "pdf_text_rule",
        "_json_parse_failed": False,
    }


def fallback_extraction(file_path: Path, pdf_text: str = "") -> Dict[str, Any]:
    return {
        "invoice_number": file_path.stem,
        "vendor_name": None,
        "invoice_date": None,
        "due_date": None,
        "bank_name": None,
        "bank_account": None,
        "quantity": None,
        "unit_price": None,
        "extracted_total": None,
        "items": [],
        "is_handwritten_image": False,
        "is_correct_invoice": bool(pdf_text and any(token in normalize_text(pdf_text) for token in ["invoice", "нэхэмжлэл"])),
        "extraction_confidence": 0.20 if pdf_text else 0.10,
        "raw_extracted_text": pdf_text,
        "_raw_model_response": None,
        "_extraction_source": "fallback",
        "_fallback_mode": True,
        "_json_parse_failed": False,
    }


def extract_invoice_payload(
    file_path: Path,
    api_keys: Sequence[str],
    max_pdf_pages: int = DEFAULT_MAX_PDF_PAGES,
) -> Dict[str, Any]:
    pdf_text = extract_pdf_text(file_path, max_pdf_pages=max_pdf_pages)
    if file_path.suffix.lower() == ".pdf" and pdf_text:
        heuristic_result = heuristic_extract_from_pdf_text(file_path, pdf_text)
        if heuristic_result.get("extraction_confidence", 0) >= 0.72:
            return heuristic_result

    if api_keys:
        result = extract_invoice_with_groq(
            file_path=file_path,
            api_keys=api_keys,
            pdf_text_hint=pdf_text or None,
            max_pdf_pages=max_pdf_pages,
        )
        if pdf_text and not result.get("raw_extracted_text"):
            result["raw_extracted_text"] = pdf_text
        return result

    return fallback_extraction(file_path, pdf_text=pdf_text)


def normalize_items(items: Any) -> List[Dict[str, Any]]:
    if not isinstance(items, list):
        return []
    normalized_items: List[Dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        quantity = normalize_number(item.get("quantity"))
        unit_price = normalize_number(item.get("unit_price"))
        line_total = normalize_number(item.get("line_total"))
        calculated_line_total = quantity * unit_price if quantity is not None and unit_price is not None else None
        normalized_items.append(
            {
                "description": item.get("description"),
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": line_total,
                "calculated_line_total": calculated_line_total,
            }
        )
    return normalized_items


def looks_like_invoice(file_path: Path, raw: Dict[str, Any]) -> bool:
    explicit_flag = normalize_bool(raw.get("is_correct_invoice"))
    if explicit_flag is not None:
        return explicit_flag
    raw_text = normalize_text(raw.get("raw_extracted_text") or "")
    if raw_text:
        return any(token in raw_text for token in ["invoice", "нэхэмжлэл", "bill"])
    return file_path.stem.lower().startswith("invoice")


def normalize_invoice_data(raw: Dict[str, Any], file_path: Path) -> Dict[str, Any]:
    items = normalize_items(raw.get("items"))
    quantity_from_items = sum(item["quantity"] for item in items if item.get("quantity") is not None) if items else None
    unit_price_from_items = next((item["unit_price"] for item in items if item.get("unit_price") is not None), None)
    line_totals = [item.get("line_total") for item in items if item.get("line_total") is not None]
    calculated_line_totals = [
        item.get("calculated_line_total") for item in items if item.get("calculated_line_total") is not None
    ]
    calculated_total = sum(line_totals) if line_totals else sum(calculated_line_totals) if calculated_line_totals else None

    raw_quantity = normalize_number(raw.get("quantity"))
    raw_unit_price = normalize_number(raw.get("unit_price"))
    direct_calculated_total = normalize_number(raw.get("calculated_total"))
    if direct_calculated_total is not None:
        calculated_total = direct_calculated_total
    elif calculated_total is None and raw_quantity is not None and raw_unit_price is not None:
        calculated_total = raw_quantity * raw_unit_price

    normalized: Dict[str, Any] = {
        "file_name": file_path.name,
        "file_path": str(file_path),
        "file_type": file_path.suffix.lower().replace(".", ""),
        "is_image": file_path.suffix.lower() in {".jpg", ".jpeg", ".png"},
        "is_pdf": file_path.suffix.lower() == ".pdf",
        "is_handwritten_image": normalize_bool(raw.get("is_handwritten_image")),
        "invoice_number": (str(raw.get("invoice_number")).strip() if raw.get("invoice_number") else file_path.stem),
        "vendor_name": raw.get("vendor_name"),
        "invoice_date": normalize_date(raw.get("invoice_date")),
        "due_date": normalize_date(raw.get("due_date")),
        "category": raw.get("category"),
        "quantity": raw_quantity if raw_quantity is not None else quantity_from_items,
        "unit_price": raw_unit_price if raw_unit_price is not None else unit_price_from_items,
        "calculated_total": round_or_none(calculated_total),
        "extracted_total": round_or_none(
            normalize_number(raw.get("extracted_total"))
            or normalize_number(raw.get("total_amount"))
            or normalize_number(raw.get("grand_total"))
        ),
        "math_is_correct": None,
        "bank_name": raw.get("bank_name"),
        "bank_account": str(raw.get("bank_account")).strip() if raw.get("bank_account") else None,
        "bank_account_registered": None,
        "vendor_registered": None,
        "is_duplicate": False,
        "is_correct_invoice": looks_like_invoice(file_path, raw),
        "is_suspicious": False,
        "risk_flags": [],
        "error_types": [],
        "final_decision": None,
        "decision_reason": None,
        "human_approval_required": False,
        "processing_status": "SUCCESS",
        "extraction_confidence": round_or_none(normalize_number(raw.get("extraction_confidence")), 2),
        "raw_extracted_text": raw.get("raw_extracted_text") or raw.get("_raw_model_response") or "",
        "_items": items,
        "_raw_invoice_date": raw.get("invoice_date"),
        "_raw_due_date": raw.get("due_date"),
        "_raw_model_response": raw.get("_raw_model_response"),
        "_extraction_source": raw.get("_extraction_source", "unknown"),
        "_fallback_mode": bool(raw.get("_fallback_mode", False)),
        "_json_parse_failed": bool(raw.get("_json_parse_failed", False)),
        "_error_message": None,
    }

    if normalized["is_image"] and normalized["is_handwritten_image"] is None:
        normalized["is_handwritten_image"] = False
    if normalized["extraction_confidence"] is None:
        normalized["extraction_confidence"] = 0.25 if normalized["_fallback_mode"] else 0.70
    return normalized


def build_category_lookup(master_data: MasterData) -> Dict[Any, str]:
    lookup: Dict[Any, str] = {}
    categories_df = master_data.categories_df
    if categories_df is None or categories_df.empty:
        return lookup
    id_column = find_column(categories_df, ["ID", "CategoryID"])
    name_column = find_column(categories_df, ["Name", "CategoryName"])
    if not id_column or not name_column:
        return lookup
    for _, row in categories_df.iterrows():
        lookup[row.get(id_column)] = str(row.get(name_column))
    return lookup


def historical_category_match(invoice: Dict[str, Any], master_data: MasterData) -> Optional[str]:
    invoices_df = master_data.historical_invoices_df
    if invoices_df is None or invoices_df.empty or not invoice.get("vendor_name"):
        return None

    vendor_column = find_column(invoices_df, ["VendorName", "Vendor", "vendor_name", "Name"])
    category_column = find_column(invoices_df, ["Category", "CategoryName"])
    category_id_column = find_column(invoices_df, ["InvoiceCategoryID", "CategoryID"])
    if not vendor_column:
        return None

    category_lookup = build_category_lookup(master_data)
    target_vendor = normalize_text(invoice.get("vendor_name"))
    scores = invoices_df[vendor_column].astype(str).apply(lambda value: fuzz.token_sort_ratio(target_vendor, normalize_text(value)))
    best_index = scores.idxmax() if not scores.empty else None
    if best_index is None or scores.loc[best_index] < 85:
        return None

    if category_column and pd.notna(invoices_df.loc[best_index, category_column]):
        return str(invoices_df.loc[best_index, category_column])
    if category_id_column:
        category_id = invoices_df.loc[best_index, category_id_column]
        if category_id in category_lookup:
            return category_lookup[category_id]
    return None


def keyword_category_match(invoice: Dict[str, Any]) -> str:
    text = " ".join(
        [
            str(invoice.get("vendor_name") or ""),
            str(invoice.get("raw_extracted_text") or ""),
        ]
    )
    normalized = normalize_text(text)
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return category
    return "Other"


def classify_category(invoice: Dict[str, Any], master_data: MasterData) -> str:
    direct_category = invoice.get("category")
    if direct_category:
        return str(direct_category)
    historical_category = historical_category_match(invoice, master_data)
    if historical_category:
        return historical_category
    return keyword_category_match(invoice)


def validate_registered_vendor(vendor_name: Any, master_data: MasterData) -> Tuple[Optional[bool], Optional[str], float]:
    vendors_df = master_data.vendors_df
    if vendors_df is None or vendors_df.empty:
        return None, None, 0.0
    if not vendor_name:
        return None, None, 0.0
    name_column = find_column(vendors_df, ["Name", "VendorName", "Vendor", "vendor_name"])
    if not name_column:
        return None, None, 0.0
    choices = vendors_df[name_column].dropna().astype(str).tolist()
    if not choices:
        return None, None, 0.0
    match = process.extractOne(str(vendor_name), choices, scorer=fuzz.token_sort_ratio)
    if not match:
        return False, None, 0.0
    matched_name, score = match[0], float(match[1])
    return score >= 80, matched_name, score


def get_vendor_row(master_data: MasterData, matched_vendor_name: Optional[str]) -> Optional[pd.Series]:
    vendors_df = master_data.vendors_df
    if vendors_df is None or vendors_df.empty or not matched_vendor_name:
        return None
    name_column = find_column(vendors_df, ["Name", "VendorName", "Vendor", "vendor_name"])
    if not name_column:
        return None
    matches = vendors_df[vendors_df[name_column].astype(str) == str(matched_vendor_name)]
    if matches.empty:
        return None
    return matches.iloc[0]


def validate_bank_account(invoice: Dict[str, Any], vendor_row: Optional[pd.Series]) -> Optional[bool]:
    if vendor_row is None:
        return None
    account_column = None
    for column_name in vendor_row.index:
        if normalize_text(column_name) in {"account", "bank account", "bankaccount", "accountnumber", "данс"}:
            account_column = column_name
            break
    if account_column is None:
        return None

    invoice_account = re.sub(r"\D", "", str(invoice.get("bank_account") or ""))
    master_account = re.sub(r"\D", "", str(vendor_row.get(account_column) or ""))
    if not invoice_account or not master_account:
        return None
    return invoice_account == master_account


def validate_date_pair(invoice: Dict[str, Any]) -> Optional[bool]:
    invoice_date = invoice.get("invoice_date")
    due_date = invoice.get("due_date")
    if not invoice_date or not due_date:
        return None
    try:
        invoice_dt = datetime.fromisoformat(str(invoice_date)).date()
        due_dt = datetime.fromisoformat(str(due_date)).date()
    except Exception:
        return False

    if invoice_dt > date.today():
        return False
    if due_dt < invoice_dt:
        return False
    return True


def validate_math(invoice: Dict[str, Any], tolerance: float = 1.0) -> Optional[bool]:
    extracted_total = invoice.get("extracted_total")
    calculated_total = invoice.get("calculated_total")
    if extracted_total is None or calculated_total is None:
        return None
    return abs(float(extracted_total) - float(calculated_total)) <= tolerance


def detect_historical_duplicate(invoice: Dict[str, Any], master_data: MasterData) -> bool:
    invoices_df = master_data.historical_invoices_df
    if invoices_df is None or invoices_df.empty:
        return False

    invoice_number_column = find_column(invoices_df, ["InvoiceNumber", "invoice_number", "Number", "ID"])
    vendor_column = find_column(invoices_df, ["VendorName", "Vendor", "vendor_name", "Name"])
    total_column = find_column(invoices_df, ["GrandTotal", "TotalAmount", "total_amount", "Amount"])
    date_column = find_column(invoices_df, ["InvoiceDate", "Date", "invoice_date"])

    target_invoice_number = normalize_text(invoice.get("invoice_number"))
    if invoice_number_column and target_invoice_number:
        historical_numbers = invoices_df[invoice_number_column].astype(str).apply(normalize_text)
        if historical_numbers.eq(target_invoice_number).any():
            return True

    target_vendor = normalize_text(invoice.get("vendor_name"))
    target_total = invoice.get("extracted_total")
    target_date = invoice.get("invoice_date")
    if not (vendor_column and total_column and target_vendor and target_total is not None):
        return False

    for _, row in invoices_df.iterrows():
        vendor_score = fuzz.token_sort_ratio(target_vendor, normalize_text(row.get(vendor_column)))
        historical_total = normalize_number(row.get(total_column))
        totals_match = historical_total is not None and abs(target_total - historical_total) <= 1
        dates_match = True
        if date_column and target_date:
            dates_match = normalize_date(row.get(date_column)) == target_date
        if vendor_score >= 85 and totals_match and dates_match:
            return True
    return False


def detect_missing_required_fields(invoice: Dict[str, Any]) -> List[str]:
    missing_fields: List[str] = []
    for field_name in REQUIRED_FIELDS_FOR_RISK:
        value = invoice.get(field_name)
        if value is None:
            missing_fields.append(field_name)
            continue
        if isinstance(value, str) and not value.strip():
            missing_fields.append(field_name)
    return missing_fields


def evaluate_invoice(invoice: Dict[str, Any], master_data: MasterData) -> Dict[str, Any]:
    invoice["category"] = classify_category(invoice, master_data)

    risk_flags: List[str] = split_pipe_values(invoice.get("risk_flags"))
    error_types: List[str] = split_pipe_values(invoice.get("error_types"))

    vendor_registered, matched_vendor_name, vendor_score = validate_registered_vendor(invoice.get("vendor_name"), master_data)
    vendor_row = get_vendor_row(master_data, matched_vendor_name)
    bank_registered = validate_bank_account(invoice, vendor_row)
    math_is_correct = validate_math(invoice)
    date_is_valid = validate_date_pair(invoice)
    historical_duplicate = detect_historical_duplicate(invoice, master_data)
    missing_fields = detect_missing_required_fields(invoice)

    invoice["vendor_registered"] = vendor_registered
    invoice["bank_account_registered"] = bank_registered
    invoice["math_is_correct"] = math_is_correct
    invoice["_vendor_match_name"] = matched_vendor_name
    invoice["_vendor_match_score"] = vendor_score
    invoice["_historical_duplicate"] = historical_duplicate
    invoice["_missing_required_fields"] = missing_fields

    if vendor_registered is False:
        add_unique(risk_flags, "UNREGISTERED_VENDOR")
    if bank_registered is False:
        add_unique(risk_flags, "BANK_ACCOUNT_MISMATCH")
    if math_is_correct is False:
        add_unique(risk_flags, "AMOUNT_MISMATCH")
    if historical_duplicate:
        add_unique(risk_flags, "DUPLICATE")
    if invoice.get("is_handwritten_image") is True:
        add_unique(risk_flags, "HANDWRITTEN_IMAGE")
    if invoice.get("extraction_confidence") is not None and float(invoice["extraction_confidence"]) < LOW_CONFIDENCE_THRESHOLD:
        add_unique(risk_flags, "LOW_CONFIDENCE_EXTRACTION")
    if missing_fields:
        add_unique(risk_flags, "MISSING_REQUIRED_FIELD")

    raw_invoice_date = invoice.get("_raw_invoice_date")
    raw_due_date = invoice.get("_raw_due_date")
    if raw_invoice_date and not invoice.get("invoice_date"):
        add_unique(risk_flags, "INVALID_DATE")
        add_unique(error_types, "INVOICE_DATE_PARSE_FAILED")
    if raw_due_date and not invoice.get("due_date"):
        add_unique(risk_flags, "INVALID_DATE")
        add_unique(error_types, "DUE_DATE_PARSE_FAILED")
    if date_is_valid is False:
        add_unique(risk_flags, "INVALID_DATE")
    if invoice.get("_json_parse_failed"):
        add_unique(error_types, "JSON_PARSE_FAILED")
    if invoice.get("_fallback_mode"):
        add_unique(error_types, "FALLBACK_EXTRACTION_USED")
    if not invoice.get("is_correct_invoice", True):
        add_unique(error_types, "NOT_AN_INVOICE")
    if missing_fields:
        for missing_field in missing_fields:
            add_unique(error_types, f"MISSING_{missing_field.upper()}")

    invoice["risk_flags"] = order_flags(risk_flags)
    invoice["error_types"] = error_types
    invoice["is_suspicious"] = len(invoice["risk_flags"]) > 0
    apply_final_decision(invoice)
    return invoice


def order_flags(flags: Iterable[str]) -> List[str]:
    flag_set = {flag for flag in flags if flag}
    ordered = [flag for flag in REQUIRED_RISK_FLAGS if flag in flag_set]
    extras = sorted(flag for flag in flag_set if flag not in REQUIRED_RISK_FLAGS)
    return ordered + extras


def flag_descriptions(flags: Sequence[str]) -> List[str]:
    descriptions = {
        "AMOUNT_MISMATCH": "invoice дээрх дүн ба тооцоолсон дүн зөрсөн",
        "UNREGISTERED_VENDOR": "vendor master database-д бүртгэлгүй",
        "INVALID_DATE": "invoice date эсвэл due date хүчингүй",
        "BANK_ACCOUNT_MISMATCH": "банк/дансны мэдээлэл master database-тэй зөрсөн",
        "DUPLICATE": "давхардсан invoice илэрсэн",
        "HANDWRITTEN_IMAGE": "гар бичмэлтэй зураг тул хүний review шаардлагатай",
        "LOW_CONFIDENCE_EXTRACTION": "extraction confidence бага",
        "MISSING_REQUIRED_FIELD": "шаардлагатай талбар дутуу",
    }
    return [descriptions.get(flag, flag) for flag in flags]


def apply_final_decision(invoice: Dict[str, Any]) -> None:
    flags = set(split_pipe_values(invoice.get("risk_flags")))
    if flags.intersection(DENY_FLAGS):
        invoice["final_decision"] = "DENY"
    elif flags.intersection(HUMAN_APPROVAL_FLAGS):
        invoice["final_decision"] = "HUMAN_APPROVAL"
    else:
        invoice["final_decision"] = "AUTO_POST"

    invoice["human_approval_required"] = invoice["final_decision"] == "HUMAN_APPROVAL"
    descriptions = flag_descriptions(order_flags(flags))
    if not descriptions:
        invoice["decision_reason"] = "Ноцтой risk илрээгүй. final_results.csv дээр AUTO_POST гэж тэмдэглэгдэнэ."
    else:
        invoice["decision_reason"] = f"{invoice['final_decision']} шалтгаан: " + "; ".join(descriptions)


def normalize_result_record(record: Dict[str, Any]) -> Dict[str, Any]:
    normalized_record: Dict[str, Any] = {}
    for column in FINAL_RESULT_COLUMNS:
        normalized_record[column] = record.get(column)

    normalized_record["risk_flags"] = join_pipe_values(order_flags(split_pipe_values(normalized_record.get("risk_flags"))))
    normalized_record["error_types"] = join_pipe_values(split_pipe_values(normalized_record.get("error_types")))
    normalized_record["is_image"] = bool(normalized_record.get("is_image"))
    normalized_record["is_pdf"] = bool(normalized_record.get("is_pdf"))
    normalized_record["human_approval_required"] = bool(normalized_record.get("human_approval_required"))

    for numeric_column in ["quantity", "unit_price", "calculated_total", "extracted_total", "extraction_confidence"]:
        normalized_record[numeric_column] = round_or_none(normalize_number(normalized_record.get(numeric_column)))

    for boolean_column in [
        "is_handwritten_image",
        "math_is_correct",
        "bank_account_registered",
        "vendor_registered",
        "is_duplicate",
        "is_correct_invoice",
        "is_suspicious",
    ]:
        normalized_record[boolean_column] = normalize_bool(normalized_record.get(boolean_column))

    for date_column in ["invoice_date", "due_date"]:
        normalized_record[date_column] = normalize_date(normalized_record.get(date_column))

    normalized_record["processing_status"] = normalized_record.get("processing_status") or "SUCCESS"
    normalized_record["raw_extracted_text"] = normalized_record.get("raw_extracted_text") or ""
    return normalized_record


def build_empty_result(file_path: Path, error_message: str, error_types: Optional[Sequence[str]] = None) -> Dict[str, Any]:
    result = {
        "file_name": file_path.name,
        "file_path": str(file_path),
        "file_type": file_path.suffix.lower().replace(".", ""),
        "is_image": file_path.suffix.lower() in {".jpg", ".jpeg", ".png"},
        "is_pdf": file_path.suffix.lower() == ".pdf",
        "is_handwritten_image": False,
        "invoice_number": file_path.stem,
        "vendor_name": None,
        "invoice_date": None,
        "due_date": None,
        "category": "Unknown",
        "quantity": None,
        "unit_price": None,
        "calculated_total": None,
        "extracted_total": None,
        "math_is_correct": None,
        "bank_name": None,
        "bank_account": None,
        "bank_account_registered": None,
        "vendor_registered": None,
        "is_duplicate": False,
        "is_correct_invoice": False,
        "is_suspicious": True,
        "risk_flags": join_pipe_values(["LOW_CONFIDENCE_EXTRACTION", "MISSING_REQUIRED_FIELD"]),
        "error_types": join_pipe_values(list(error_types or ["PROCESSING_EXCEPTION"])),
        "final_decision": "HUMAN_APPROVAL",
        "decision_reason": f"HUMAN_APPROVAL шалтгаан: боловсруулалтын алдаа гарсан ({error_message})",
        "human_approval_required": True,
        "processing_status": "FAILED",
        "extraction_confidence": 0.0,
        "raw_extracted_text": "",
        "_error_message": error_message,
    }
    return result


def post_process_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    duplicate_mask = pd.Series(False, index=df.index)

    invoice_numbers = df["invoice_number"].astype(str).apply(normalize_text)
    non_empty_invoice_numbers = invoice_numbers[invoice_numbers.ne("")]
    duplicate_invoice_numbers = set(non_empty_invoice_numbers[non_empty_invoice_numbers.duplicated(keep=False)].tolist())
    duplicate_mask |= invoice_numbers.isin(duplicate_invoice_numbers)

    signature_df = pd.DataFrame(
        {
            "vendor": df["vendor_name"].astype(str).apply(normalize_text),
            "date": df["invoice_date"].fillna("").astype(str),
            "total": df["extracted_total"].apply(lambda value: round(float(value), 2) if pd.notna(value) else np.nan),
        }
    )
    signature_mask = signature_df["vendor"].ne("") & signature_df["date"].ne("") & signature_df["total"].notna()
    if signature_mask.any():
        duplicate_mask |= signature_df[signature_mask].duplicated(keep=False).reindex(df.index, fill_value=False)

    if "_historical_duplicate" in df.columns:
        duplicate_mask |= df["_historical_duplicate"].fillna(False).astype(bool)

    df = df.copy()
    df["is_duplicate"] = duplicate_mask

    for index, row in df.iterrows():
        flags = order_flags(split_pipe_values(row.get("risk_flags")))
        if df.at[index, "is_duplicate"]:
            add_unique(flags, "DUPLICATE")
        else:
            flags = [flag for flag in flags if flag != "DUPLICATE"]
        df.at[index, "risk_flags"] = join_pipe_values(order_flags(flags))
        df.at[index, "is_suspicious"] = len(split_pipe_values(df.at[index, "risk_flags"])) > 0

        mutable_row = row.to_dict()
        mutable_row["risk_flags"] = split_pipe_values(df.at[index, "risk_flags"])
        mutable_row["is_duplicate"] = bool(df.at[index, "is_duplicate"])
        apply_final_decision(mutable_row)
        df.at[index, "final_decision"] = mutable_row["final_decision"]
        df.at[index, "decision_reason"] = mutable_row["decision_reason"]
        df.at[index, "human_approval_required"] = mutable_row["human_approval_required"]

    return df


def final_results_dataframe(records: Sequence[Dict[str, Any]]) -> pd.DataFrame:
    normalized_rows = [normalize_result_record(record) for record in records]
    if not normalized_rows:
        return pd.DataFrame(columns=FINAL_RESULT_COLUMNS)
    df = pd.DataFrame(normalized_rows)
    for column in FINAL_RESULT_COLUMNS:
        if column not in df.columns:
            df[column] = None
    return df[FINAL_RESULT_COLUMNS]


def failed_files_dataframe(records: Sequence[Dict[str, Any]]) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    for record in records:
        if record.get("processing_status") == "FAILED":
            rows.append(
                {
                    "file_name": record.get("file_name"),
                    "file_path": record.get("file_path"),
                    "processing_status": record.get("processing_status"),
                    "error_types": join_pipe_values(split_pipe_values(record.get("error_types"))),
                    "error_message": record.get("_error_message") or record.get("decision_reason"),
                }
            )
    return pd.DataFrame(rows, columns=["file_name", "file_path", "processing_status", "error_types", "error_message"])


def export_dataframe(df: pd.DataFrame, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    return output_path


def count_flag(df: pd.DataFrame, flag: str) -> int:
    if df.empty or "risk_flags" not in df.columns:
        return 0
    return int(df["risk_flags"].apply(lambda value: flag in split_pipe_values(value)).sum())


def count_boolean(df: pd.DataFrame, column_name: str, expected_value: bool = True) -> int:
    if df.empty or column_name not in df.columns:
        return 0
    normalized_series = df[column_name].apply(normalize_bool)
    return int((normalized_series == expected_value).sum())


def generate_aggregate_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary_rows = [
        {
            "metric_key": "total_invoices",
            "question": "Нийт хэдэн invoice байна вэ?",
            "count": int(len(df)),
            "answer": f"Нийт {len(df)} invoice байна.",
        },
        {
            "metric_key": "correct_invoices",
            "question": "Хэдэн invoice зөв invoice вэ?",
            "count": count_boolean(df, "is_correct_invoice", True),
            "answer": f"{count_boolean(df, 'is_correct_invoice', True)} invoice зөв invoice гэж тэмдэглэгдсэн байна.",
        },
        {
            "metric_key": "suspicious_invoices",
            "question": "Хэдэн invoice сэжигтэй вэ?",
            "count": count_boolean(df, "is_suspicious", True),
            "answer": f"{count_boolean(df, 'is_suspicious', True)} invoice сэжигтэй байна.",
        },
        {
            "metric_key": "duplicate_invoices",
            "question": "Хэдэн invoice duplicate вэ?",
            "count": count_boolean(df, "is_duplicate", True),
            "answer": f"{count_boolean(df, 'is_duplicate', True)} invoice duplicate байна.",
        },
        {
            "metric_key": "math_errors",
            "question": "Хэдэн invoice математик тооцооллын алдаатай вэ?",
            "count": count_flag(df, "AMOUNT_MISMATCH"),
            "answer": f"{count_flag(df, 'AMOUNT_MISMATCH')} invoice дээр математик тооцооллын зөрүү илэрсэн.",
        },
        {
            "metric_key": "unregistered_vendors",
            "question": "Хэдэн invoice бүртгэлгүй vendor-той вэ?",
            "count": count_flag(df, "UNREGISTERED_VENDOR"),
            "answer": f"{count_flag(df, 'UNREGISTERED_VENDOR')} invoice бүртгэлгүй vendor-той байна.",
        },
        {
            "metric_key": "invalid_dates",
            "question": "Хэдэн invoice буруу огноотой вэ?",
            "count": count_flag(df, "INVALID_DATE"),
            "answer": f"{count_flag(df, 'INVALID_DATE')} invoice буруу огноотой байна.",
        },
        {
            "metric_key": "bank_mismatches",
            "question": "Хэдэн invoice банкны мэдээллийн зөрүүтэй вэ?",
            "count": count_flag(df, "BANK_ACCOUNT_MISMATCH"),
            "answer": f"{count_flag(df, 'BANK_ACCOUNT_MISMATCH')} invoice банкны мэдээллийн зөрүүтэй байна.",
        },
        {
            "metric_key": "image_invoices",
            "question": "Хэдэн invoice зураг хэлбэртэй вэ?",
            "count": count_boolean(df, "is_image", True),
            "answer": f"{count_boolean(df, 'is_image', True)} invoice зураг хэлбэртэй байна.",
        },
        {
            "metric_key": "handwritten_images",
            "question": "Хэдэн invoice гар бичмэлтэй зураг вэ?",
            "count": count_boolean(df, "is_handwritten_image", True),
            "answer": f"{count_boolean(df, 'is_handwritten_image', True)} invoice гар бичмэлтэй зураг байна.",
        },
        {
            "metric_key": "human_approval",
            "question": "Хэдэн invoice HUMAN_APPROVAL авах ёстой вэ?",
            "count": int((df.get("final_decision") == "HUMAN_APPROVAL").sum()) if "final_decision" in df.columns else 0,
            "answer": f"{int((df.get('final_decision') == 'HUMAN_APPROVAL').sum()) if 'final_decision' in df.columns else 0} invoice HUMAN_APPROVAL авах ёстой байна.",
        },
        {
            "metric_key": "deny",
            "question": "Хэдэн invoice DENY болох ёстой вэ?",
            "count": int((df.get("final_decision") == "DENY").sum()) if "final_decision" in df.columns else 0,
            "answer": f"{int((df.get('final_decision') == 'DENY').sum()) if 'final_decision' in df.columns else 0} invoice DENY болох ёстой байна.",
        },
    ]
    return pd.DataFrame(summary_rows, columns=["metric_key", "question", "count", "answer"])


def aggregate_answer(question: str, df: pd.DataFrame) -> str:
    normalized_question = normalize_text(question).replace("?", "")
    summary_df = generate_aggregate_summary(df)
    question_map: Dict[str, str] = {}
    for _, row in summary_df.iterrows():
        key = normalize_text(row["question"]).replace("?", "")
        question_map[key] = row["answer"]
        if normalized_question == key:
            return row["answer"]

    fallbacks = {
        "нийт": "Нийт хэдэн invoice байна вэ?",
        "total": "Нийт хэдэн invoice байна вэ?",
        "зөв invoice": "Хэдэн invoice зөв invoice вэ?",
        "сэжигтэй": "Хэдэн invoice сэжигтэй вэ?",
        "duplicate": "Хэдэн invoice duplicate вэ?",
        "математик": "Хэдэн invoice математик тооцооллын алдаатай вэ?",
        "бүртгэлгүй vendor": "Хэдэн invoice бүртгэлгүй vendor-той вэ?",
        "огноо": "Хэдэн invoice буруу огноотой вэ?",
        "банк": "Хэдэн invoice банкны мэдээллийн зөрүүтэй вэ?",
        "зураг": "Хэдэн invoice зураг хэлбэртэй вэ?",
        "гар бичмэл": "Хэдэн invoice гар бичмэлтэй зураг вэ?",
        "human approval": "Хэдэн invoice HUMAN_APPROVAL авах ёстой вэ?",
        "deny": "Хэдэн invoice DENY болох ёстой вэ?",
    }
    for token, mapped_question in fallbacks.items():
        if token in normalized_question:
            return question_map[normalize_text(mapped_question).replace("?", "")]

    if "invoice" in normalized_question:
        return question_map[normalize_text("Нийт хэдэн invoice байна вэ?").replace("?", "")]

    supported = "\n".join(f"- {question_text}" for question_text in AGGREGATE_QUESTIONS)
    return "Дэмжигдсэн aggregate асуултууд:\n" + supported


def export_aggregate_answers(df: pd.DataFrame, output_path: Path) -> Path:
    summary_df = generate_aggregate_summary(df)
    return export_dataframe(summary_df, output_path)


def load_final_results(final_results_path: Path) -> pd.DataFrame:
    if not Path(final_results_path).exists():
        return pd.DataFrame(columns=FINAL_RESULT_COLUMNS)
    df = pd.read_csv(final_results_path, keep_default_na=False)
    for column in FINAL_RESULT_COLUMNS:
        if column not in df.columns:
            df[column] = None
    return df[FINAL_RESULT_COLUMNS]


def resolve_invoice_record(invoice_identifier: str, df: pd.DataFrame) -> Optional[pd.Series]:
    if df.empty:
        return None
    identifier = normalize_text(invoice_identifier)
    if not identifier:
        return None

    exact_masks = [
        df["file_name"].astype(str).apply(normalize_text).eq(identifier),
        df["invoice_number"].astype(str).apply(normalize_text).eq(identifier),
        df["file_path"].astype(str).apply(normalize_text).eq(identifier),
        df["file_name"].astype(str).apply(lambda value: normalize_text(Path(value).stem)).eq(identifier),
    ]
    for mask in exact_masks:
        matched = df[mask]
        if not matched.empty:
            return matched.iloc[0]

    choices: Dict[str, int] = {}
    for index, row in df.iterrows():
        for candidate in [row.get("file_name"), row.get("invoice_number"), Path(str(row.get("file_name"))).stem]:
            candidate_text = str(candidate or "").strip()
            if candidate_text:
                choices[candidate_text] = index
    if not choices:
        return None
    match = process.extractOne(invoice_identifier, list(choices.keys()), scorer=fuzz.token_sort_ratio)
    if match and match[1] >= 75:
        return df.iloc[choices[match[0]]]
    return None


def bool_to_mongolian(value: Any) -> str:
    normalized = normalize_bool(value)
    if normalized is True:
        return "Тийм"
    if normalized is False:
        return "Үгүй"
    return "Тодорхойгүй"


def fact_check_invoice(invoice_identifier: str, question: str, df: pd.DataFrame) -> str:
    row = resolve_invoice_record(invoice_identifier, df)
    if row is None:
        supported = "\n".join(f"- {item}" for item in FACT_CHECK_SUPPORTED_QUESTIONS)
        return (
            f"'{invoice_identifier}' гэсэн invoice олдсонгүй.\n"
            f"Дэмжигдсэн fact-check асуултууд:\n{supported}"
        )

    normalized_question = normalize_text(question)
    file_label = row.get("file_name") or row.get("invoice_number") or invoice_identifier

    if "final decision" in normalized_question:
        return f"{file_label} invoice-ийн final decision: {row.get('final_decision')}"
    if "duplicate" in normalized_question:
        return f"{file_label} duplicate мөн эсэх: {bool_to_mongolian(row.get('is_duplicate'))}"
    if "vendor" in normalized_question and "нэр" in normalized_question:
        return f"{file_label} invoice-ийн vendor нэр: {row.get('vendor_name') or 'Тодорхойгүй'}"
    if "category" in normalized_question:
        return f"{file_label} invoice-ийн ангилал: {row.get('category') or 'Тодорхойгүй'}"
    if "due date" in normalized_question or "due" in normalized_question:
        return f"{file_label} invoice-ийн due date: {row.get('due_date') or 'Тодорхойгүй'}"
    if "bank account" in normalized_question or "данс" in normalized_question:
        return f"{file_label} invoice-ийн bank account бүртгэлтэй эсэх: {bool_to_mongolian(row.get('bank_account_registered'))}"
    if "яагаад deny" in normalized_question or ("deny" in normalized_question and "яагаад" in normalized_question):
        if row.get("final_decision") != "DENY":
            return f"{file_label} invoice DENY биш. Одоогийн decision: {row.get('final_decision')}"
        return f"{file_label} invoice DENY болсон шалтгаан: {row.get('decision_reason')}"
    if "ямар төрлийн алдаа" in normalized_question or "алдаа" in normalized_question:
        errors = row.get("error_types") or row.get("risk_flags") or "Алдаа тэмдэглэгдээгүй"
        return f"{file_label} invoice дээр илэрсэн алдаа: {errors}"
    if "human approval" in normalized_question or "human" in normalized_question:
        return f"{file_label} invoice human approval авах эсэх: {bool_to_mongolian(row.get('human_approval_required'))}"
    if "математик" in normalized_question or "math" in normalized_question:
        return f"{file_label} invoice-ийн математик тооцоолол зөв эсэх: {bool_to_mongolian(row.get('math_is_correct'))}"

    supported = "\n".join(f"- {item}" for item in FACT_CHECK_SUPPORTED_QUESTIONS)
    return f"Дэмжигдсэн fact-check асуултууд:\n{supported}"


def export_checkpoint(records: Sequence[Dict[str, Any]], project_paths: ProjectPaths) -> Tuple[Path, Path]:
    final_df = final_results_dataframe(records)
    failed_df = failed_files_dataframe(records)
    export_dataframe(final_df, project_paths.final_results_path)
    export_dataframe(failed_df, project_paths.failed_files_path)
    return project_paths.final_results_path, project_paths.failed_files_path


def process_single_invoice(
    file_path: Path,
    api_keys: Sequence[str],
    master_data: MasterData,
    max_pdf_pages: int = DEFAULT_MAX_PDF_PAGES,
) -> Dict[str, Any]:
    try:
        raw_payload = extract_invoice_payload(file_path=file_path, api_keys=api_keys, max_pdf_pages=max_pdf_pages)
        normalized_invoice = normalize_invoice_data(raw_payload, file_path)
        evaluated_invoice = evaluate_invoice(normalized_invoice, master_data)
        return evaluated_invoice
    except Exception as error:
        failed = build_empty_result(
            file_path=file_path,
            error_message=str(error),
            error_types=["PROCESSING_EXCEPTION", "LOW_CONFIDENCE_EXTRACTION"],
        )
        failed["_traceback"] = traceback.format_exc()
        return failed


def process_invoices_pipeline(
    preferred_input_root: Optional[Path] = None,
    preferred_output_dir: Optional[Path] = None,
    max_files: Optional[int] = None,
    checkpoint_every: int = 10,
    max_pdf_pages: int = DEFAULT_MAX_PDF_PAGES,
) -> Dict[str, Any]:
    project_paths = build_project_paths(
        preferred_input_root=preferred_input_root,
        preferred_output_dir=preferred_output_dir,
    )
    search_roots = discover_search_roots(preferred_input_root=preferred_input_root)
    invoice_files = scan_invoice_files(search_roots, max_files=max_files)
    api_keys = load_groq_api_keys()
    master_data = load_master_data(project_paths.db_path)

    records: List[Dict[str, Any]] = []
    for index, file_path in enumerate(invoice_files, start=1):
        record = process_single_invoice(
            file_path=file_path,
            api_keys=api_keys,
            master_data=master_data,
            max_pdf_pages=max_pdf_pages,
        )
        records.append(record)
        if checkpoint_every and index % checkpoint_every == 0:
            export_checkpoint(records, project_paths)

    raw_df = pd.DataFrame(records)
    if not raw_df.empty:
        raw_df = post_process_duplicates(raw_df)
        for column in raw_df.columns:
            raw_df[column] = raw_df[column]
        records = raw_df.to_dict(orient="records")

    final_df = final_results_dataframe(records)
    failed_df = failed_files_dataframe(records)
    export_dataframe(final_df, project_paths.final_results_path)
    export_dataframe(failed_df, project_paths.failed_files_path)

    reloaded_final_df = load_final_results(project_paths.final_results_path)
    export_aggregate_answers(reloaded_final_df, project_paths.aggregate_answers_path)
    aggregate_df = pd.read_csv(project_paths.aggregate_answers_path) if project_paths.aggregate_answers_path.exists() else pd.DataFrame()

    return {
        "project_paths": project_paths,
        "api_key_count": len(api_keys),
        "invoice_files": invoice_files,
        "master_data": master_data,
        "final_df": reloaded_final_df,
        "failed_df": failed_df,
        "aggregate_df": aggregate_df,
    }


def build_processing_summary_text(final_df: pd.DataFrame, failed_df: pd.DataFrame, project_paths: ProjectPaths) -> str:
    summary_df = generate_aggregate_summary(final_df)
    lines = [
        "Invoice processing summary",
        f"- final_results.csv: {project_paths.final_results_path}",
        f"- failed_files.csv: {project_paths.failed_files_path}",
        f"- aggregate_answers.csv: {project_paths.aggregate_answers_path}",
        f"- Нийт invoice: {len(final_df)}",
        f"- FAILED files: {len(failed_df)}",
    ]
    for _, row in summary_df.iterrows():
        lines.append(f"- {row['question']} {row['count']}")
    return "\n".join(lines)


__all__ = [
    "AGGREGATE_QUESTIONS",
    "DEFAULT_MAX_PDF_PAGES",
    "FACT_CHECK_SUPPORTED_QUESTIONS",
    "FINAL_RESULT_COLUMNS",
    "ProjectPaths",
    "aggregate_answer",
    "build_processing_summary_text",
    "build_project_paths",
    "count_flag",
    "export_aggregate_answers",
    "fact_check_invoice",
    "generate_aggregate_summary",
    "load_final_results",
    "load_groq_api_keys",
    "load_master_data",
    "process_invoices_pipeline",
    "scan_invoice_files",
]
