# Karachi Job Market Analysis

A Data Engineering project that collects job market data from the JSearch API, transforms it, and loads it into Google BigQuery for analysis.

## Project Goal

The purpose of this project was to just analyze two things:

- Which technology roles are currently opened and mostly hiring?
- What happened to job ratio for Senior, Mid, Junior, and Internship roles?

---

## Tech Stack

- Python
- Pandas
- Google BigQuery
- JSearch API
- Docker
- SQL
- Google Sheets (Connected Sheets)

---

## Project Structure

```
karachi-job-market-analysis/

├── extract/
│   └── fetch_jobs.py
│
├── transform/
│   └── preprocess_data.py
│
├── load/
│   ├── load_bigquery.py
│   └── merge_bigquery.py
│
├── sql/
│   ├── views/
│   └── analysis/
│
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

---

## ETL Pipeline

```
JSearch API
      │
      ▼
Extract
      │
      ▼
Transform
      │
      ▼
BigQuery Staging
      │
      ▼
BigQuery Production
      │
      ▼
SQL Views
      │
      ▼
Google Sheets Dashboard
```

---

## Features

- Fetches jobs from JSearch API
- Cleans and transforms raw data
- Generates unique job IDs
- Categorizes jobs by role and seniority
- Removes duplicate records
- Loads data into BigQuery staging
- MERGE support for production table
- Docker support
- SQL-based analytics

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/iam-devAlhan/karachi-job-market-analysis.git

cd karachi-job-market-analysis
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file.

```
PROJECT_ID=
DATASET_ID=
RAPID_API_KEY=
RAPID_API_HOST=
GOOGLE_APPLICATION_CREDENTIALS=
NUM_PAGES=2
```

---

### Run the pipeline

```bash
python main.py
```

---

## Docker

Build

```bash
docker build -t karachi-job-pipeline .
```

Run

```bash
docker run \
--rm \
--env-file .env \
-v $(pwd)/credentials.json:/app/credentials.json:ro \
-e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
karachi-job-pipeline
```

---

## Current Limitations

- BigQuery Sandbox does not support `MERGE` statements because DML operations require billing to be enabled.
- Analysis currently focuses on Karachi-based jobs.

---

## Future Improvements

- Apache Airflow orchestration
- Automatic scheduling
- BigQuery SQL Views
- Google Sheets Dashboard
- Looker Studio Dashboard
- CI/CD
- Unit Testing
- Monitoring and Logging

---

## License

MIT License
