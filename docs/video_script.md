# Video Script

## 1. Intro

State the project goal: invoice automation with extraction, validation, risk scoring, decisioning, and review support.

## 2. Notebook demo

- Open the notebook.
- Show the data scan step.
- Show structured extraction.
- Show validation and final decision logic.
- Show the export of `final_results.csv`.

## 3. Aggregate Q&A demo

- Open the demo app or the notebook output table.
- Ask: `Нийт хэдэн invoice байна вэ?`
- Ask: `Хэдэн invoice зөв invoice вэ?`
- Ask: `Хэдэн invoice DENY болох ёстой вэ?`
- Show that answers come from the batch results table.

## 4. Fact-check demo

- Pick one invoice.
- Ask: `final decision юу вэ?`
- Ask: `duplicate мөн үү?`
- Ask: `яагаад deny болсон бэ?`
- Ask: `math зөв үү?`
- Show the answer derived from the selected invoice row.

## 5. Closing

Summarize that the project exports structured results, supports batch reasoning, and provides both aggregate and invoice-level review.
