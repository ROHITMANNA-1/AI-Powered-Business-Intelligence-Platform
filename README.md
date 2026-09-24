# AI Analyst

AI Analyst is an industry-oriented business intelligence application for descriptive analytics, diagnostic analysis, SQL exploration, and evidence-backed business reporting. It is not a predictive machine learning project.

## Current status

The Streamlit entry point and project contract are in place. The selected starter dataset is the [UCI Online Retail dataset](https://archive.ics.uci.edu/dataset/352/online+retail), published under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The source contains 541,909 UK online-retail transactions from 2010-12-01 through 2011-12-09.

The source fields are invoice number, stock code, product description, quantity, invoice date, unit price, customer ID, and country. Revenue is derived as `Quantity * UnitPrice`. The source does not contain profit, product category, shipping mode, shipping cost, or delivery date; the application must report those metrics as unavailable rather than infer them.

## Planned architecture

```text
Streamlit UI
    -> data loading and cleaning
    -> profiling and EDA
    -> SQLAlchemy/MySQL read-only analysis
    -> validated LLM-generated SQL
    -> evidence-backed insight and report generation
```

The application includes upload and cleaning controls, profiling, KPI cards, interactive EDA, conservative natural-language SQL analysis, evidence-backed insights, Markdown/PDF reports, MySQL/SQLite helpers, tests, and a separate Power BI guide. An OpenAI API key enables optional SQL generation; without one, the deterministic analyst remains fully usable offline.

Uploaded files do not need the starter dataset's exact headings. The schema detector maps common alternatives such as `Sales Amount` to revenue, `Order Number` to order ID, `Qty` to quantity, `Transaction Date` to date, and `Client` to customer ID. Other headings remain available as dynamic dimensions for grouping and natural-language questions. Unsupported fields are reported as unavailable instead of guessed.

The UCI workbook is downloaded locally under `data/raw/` and excluded from Git. Generate the reproducible processed file with `python scripts/prepare_dataset.py`. Optional MySQL setup and loading commands are in [docs/mysql_setup.md](docs/mysql_setup.md). The Power BI guide provides the complete model and DAX; creating and publishing a `.pbix` file still requires Power BI Desktop.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

Open the local URL printed by Streamlit. API keys are optional for the initial scaffold and must only be provided through `.env` or Streamlit secrets.

## Implemented modules

- `src/data_loader.py`, `src/data_cleaning.py`, and `src/data_profiling.py`: load, normalize, clean, and profile CSV/Excel data.
- `src/kpis.py` and `src/eda.py`: shared measures, trends, and grouped comparisons.
- `src/database.py`, `src/sql_validator.py`, and `src/query_executor.py`: SQLAlchemy storage and read-only query boundary.
- `src/ai_analyst.py`: validated optional LLM SQL generation with offline fallback and result-grounded explanations.
- `src/insight_engine.py` and `src/report_generator.py`: evidence-backed findings and Markdown/PDF output.
- `scripts/prepare_dataset.py` and `scripts/load_mysql.py`: reproducible local data preparation and MySQL loading.
- `sql/`, `powerbi/`, `docs/`, and `tests/`: database setup, dashboard model, architecture, evaluation, and verification material.

## Testing

Run the test suite with:

```powershell
pytest -q
```

The selected VS Code Python environment should contain all packages from `requirements.txt`. If a terminal session reports missing packages after installation, activate the configured environment in a new terminal before running Streamlit.

## Attribution

Chen, D. (2015). *Online Retail*. UCI Machine Learning Repository. DOI: [10.24432/C5BW33](https://doi.org/10.24432/C5BW33). The dataset is licensed under CC BY 4.0. Follow the license terms and retain attribution when redistributing derived files.
