## Project Overview

This project analyzes customer, product, and order data to identify revenue trends, data quality issues, and return-rate patterns. It combines SQL reporting, Python-based data cleaning and exploratory data analysis (EDA), data visualization, and AI-powered business narrative generation.

The final output is a Situation–Complication–Resolution (SCR) narrative that translates verified analytical findings into actionable insights for business and finance stakeholders.

## 📊 Dashboard Preview

The Power BI dashboard provides a visual overview of Mamaearth's sales performance and return patterns, highlighting key business metrics and trends.

It includes KPI cards and visualizations covering total revenue, total orders, return rates, monthly revenue trends, city-tier performance, product categories, and payment methods.
<img width="1527" height="859" alt="image" src="https://github.com/user-attachments/assets/35b3c064-12c2-4a76-81ce-fbe7937b9c48" />


## Repository Structure

```text
repo/
├── README.md
├── sql/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── reports.sql
├── data/
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
├── analysis/
│   ├── clean_and_eda.py
│   └── visualize.py
├── visualizations/
│   ├── return_rate_by_payment.png
│   └── monthly_revenue_trend.png
└── narrator/
    ├── findings.json
    └── generate_narrative.py
```

## Technology Stack

- **SQL:** Database schema creation, data loading, and analytical reporting
- **Python:** Data cleaning, exploratory analysis, metric calculation, and visualization
- **Pandas:** Data manipulation and analysis
- **Matplotlib:** Data visualization
- **Google Gemini API:** AI-powered business narrative generation
- **JSON:** Structured transfer of findings between the analysis and narrative layers

## Three-Layer Workflow

### Layer 1: SQL Reporting

**Files:** `sql/schema.sql`, `sql/seed_data.sql`, `sql/reports.sql`

1. Execute `sql/schema.sql` to create the required database tables.
2. Load the records from the CSV files in `data/` using the database loading method configured for the project.
3. Execute `sql/seed_data.sql` to insert any additional seed records required by the schema.
4. Run `sql/reports.sql` to generate the SQL reports.

**Output:** Structured SQL reports containing analytical results from the database.

### Layer 2: Python Data Analysis and Visualization

**Files:** `analysis/clean_and_eda.py`, `analysis/visualize.py`

1. Run `analysis/clean_and_eda.py` to load the CSV datasets, inspect data quality, handle duplicates, calculate analytical metrics, and perform exploratory analysis.
2. The cleaning and analysis script generates `narrator/findings.json`, a structured summary of the key findings used by the narrative generator.
3. Run `analysis/visualize.py` to generate the required visualizations:
   - `visualizations/return_rate_by_payment.png`
   - `visualizations/monthly_revenue_trend.png`

**Output:** Cleaned analytical results, structured findings in JSON format, and visualization files.

### Layer 3: AI-Powered Narrative Generation

**Files:** `narrator/findings.json`, `narrator/generate_narrative.py`

1. Run `narrator/generate_narrative.py` after `findings.json` has been generated.
2. The script reads the JSON findings and uses Google Gemini to generate a business-focused SCR narrative with three sections: Situation, Complication, and Resolution.
3. A validation checker verifies the presence of required financial figures and business metrics.
4. If the API key is unavailable or a Gemini request fails, the script uses the deterministic offline narrative generator.

**Output:** A validated SCR narrative based on the analytical findings.

## Data Flow

The three layers work together as follows:

```text
CSV Datasets
    |
    +----> SQL Schema and Data Loading
    |              |
    |              v
    |         SQL Reports
    |
    +----> Python Cleaning and EDA
                   |
                   +----> Visualizations
                   |
                   v
             findings.json
                   |
                   v
          Gemini / Offline Generator
                   |
                   v
            SCR Business Narrative
                   |
                   v
             Validation Checks
```

The SQL and Python layers use the same source datasets for complementary analysis. The JSON findings file acts as the structured interface between the Python analysis and the narrative generation layer.

## Setup and Execution

### Prerequisites

- Python 3.10 or a compatible version supported by the installed dependencies
- A configured SQL database compatible with the SQL scripts
- Python packages: `pandas`, `matplotlib`, and `google-genai`
- A Gemini API key for online narrative generation

Install the Python dependencies:

```bash
python -m pip install pandas matplotlib google-genai
```

### Execution Order

Run the project from the repository root.

**1. SQL layer**

Execute the schema, load the CSV data and any required seed records, then run the analytical reports. Follow the database-specific loading instructions for your SQL environment.

**2. Python analysis layer**

```bash
python analysis/clean_and_eda.py
python analysis/visualize.py
```

Confirm that `narrator/findings.json` and both visualization files have been generated.

**3. Narrative layer**

Configure the `GEMINI_API_KEY` environment variable, then run:

```bash
python narrator/generate_narrative.py
```

Review the generated narrative and confirm that the validation checker passes.

## API Key and Offline Mode

The Gemini API key should be configured as an environment variable rather than hardcoded in the source code. Never commit API keys or other credentials to the public repository.

When Gemini is available, the narrative generator uses the API to create the SCR report. If the API cannot be used, the offline fallback generates a deterministic report directly from `findings.json`, allowing the workflow to continue without an AI request.

## Reproducibility and Validation

The project separates database reporting, Python analysis, and narrative generation into distinct layers. This structure makes the workflow easier to reproduce, maintain, and debug.

The narrative validation checks confirm that key financial figures and analytical metrics are represented in the report. The structured JSON findings provide a consistent source of values for the final business narrative.

## Business Value

The project demonstrates how SQL reporting and Python analytics can be combined with generative AI to turn raw operational data into business-oriented insights. It emphasizes data quality, revenue reconciliation, return-rate analysis, reproducible workflows, and automated narrative generation.
