import logging
import pandas as pd
import hashlib
from extract.fetch_jobs import get_job_data
from datetime import datetime

logger = logging.getLogger(__name__)

def extract_seniority(title: str) -> str:
    if not title:
        return "unspecified"
    
    title_lower = title.lower()
    
    if any(x in title_lower for x in ["fresher","intern", "internship", "trainee"]):
        return "intern"
    elif any(x in title_lower for x in ["junior", "jr.", "jr ", "entry"]):
        return "junior"
    elif any(x in title_lower for x in ["mid", "mid-level", "intermediate"]):
        return "mid"
    elif any(x in title_lower for x in ["architect", "contract","senior", "sr.", "sr ", "lead", "principal","consultant","engineer","specialist"]):
        return "senior"
    else:
        return "unspecified"

def extract_job_type(title: str) -> str:
    if not title:
        return "unspecified"
    
    title_lower = title.lower()

    if any(x in title_lower for x in ["sqa", "qa"]):
        return "SQA Automation/Testing"
    elif any(x in title_lower for x in ["python", "django", "dotnet","full","stack","angular", "web", "mern", "node.js", "react.js", "wordpress", ".net"]):
        return "Full Stack Developer"
    elif any(x in title_lower for x in ["ai", "ml", "ai/ml","machine learning","ai engineer"]):
        return "AI/ML Engineer"
    elif any(x in title_lower for x in ["cybersecurity", "soc", "penetration", "threat", "cyber","security"]):
        return "CyberSecurity"
    elif any(x in title_lower for x in ["sap","abap"]):
        return "SAP Consultancy"
    elif any(x in title_lower for x in ["odoo"]):
        return "Odoo Functional Consultant"
    elif any(x in title_lower for x in ["erp"]):
        return "ERP Specialist"
    elif any(x in title_lower for x in ["cloud","ops","devops","ci","cd"]):
        return "DevOps/MLOps"
    elif any(x in title_lower for x in ["networking", "it","troubleshooting","ccna"]):
        return "IT/Networking"
    else:
        return "unspecified"


def generate_job_id(title: str, company: str, location: str, date_posted: str, apply_link: str) -> str:
    """
    Generate a unique job ID based on key attributes.
    """
    # Create a unique string from the job's attributes
    unique_string = f"{title}_{company}_{location}_{date_posted}_{apply_link}"
    
    # Generate a SHA-256 hash
    hash_object = hashlib.sha256(unique_string.encode())
    job_id = hash_object.hexdigest()[:16]  # Take first 16 characters for brevity
    
    return job_id

def get_transformed_data() -> pd.DataFrame:
    try:
        jobs_data = get_job_data()
    except Exception as e:
        logger.error(f"Exception occured due to {e}")
        raise

    df = pd.DataFrame(jobs_data)
    df.drop(['salary_min', 'salary_max'], axis=1, inplace=True)
    df['date_posted'] = pd.to_datetime(df['date_posted'], errors='coerce')
    df['date_posted'] = df['date_posted'].dt.tz_localize(None)
    df['date_posted'] = df['date_posted'].astype('datetime64[ns]')
    df['date_posted_month'] = df['date_posted'].dt.month
    df['date_posted_year'] = df['date_posted'].dt.year
    df['seniority'] = df["title"].apply(extract_seniority)
    df['job_type'] = df["title"].apply(extract_job_type)
    df['load_date'] = datetime.now()
    df['job_id'] = df.apply(
        lambda row: generate_job_id(row['title'], row['company'], row['location'], row['date_posted'], row['apply_link']),
        axis=1
    )

    final_col_order = [
        "job_id",
        "title",
        "job_type",
        "company",
        "location",
        "country",
        "employment_type",
        "date_posted",
        "date_posted_month",
        "date_posted_year",
        "is_remote",
        "seniority",
        "apply_link",
        "load_date"
    ]

    df_final = df[final_col_order]
    df_final = df_final.drop_duplicates("job_id", keep="last")
    return df_final
