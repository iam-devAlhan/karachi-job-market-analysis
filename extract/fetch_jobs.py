import requests
import os
from dotenv import load_dotenv
import time
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY", "")
RAPID_API_HOST = os.getenv("RAPID_API_HOST", "")
REQUEST_DELAY = 1.0  # Seconds between requests

if not RAPID_API_KEY or not RAPID_API_HOST:
    logger.error("API credentials missing. Set RAPID_API_KEY and RAPID_API_HOST in .env")
    raise EnvironmentError("Missing API credentials")

URL = "https://jsearch.p.rapidapi.com/search"
HEADERS = {
    "x-rapidapi-key": RAPID_API_KEY,
    "x-rapidapi-host": RAPID_API_HOST,
    "Content-Type": "application/json"
}

ROLES = [
    "python developer in karachi",
    "ai engineer/ai automation in karachi",
    "full stack developer in karachi",
    "machine learning engineer role in karachi",
    "devops/cloud roles in karachi",
    "cybersecurity roles in karachi",
    "sap consultant roles in karachi",
    "odoo technical roles in karachi",
    "sqa/qa automation roles in karachi",
    "IT/Networking roles in karachi"
]

def fetch_jobs_for_role(role: str) -> list:
    """Fetch jobs for a single role. Raises exception on failure."""
    time.sleep(REQUEST_DELAY)
    params = {
        "query": role,
        "page": "1",
        "num_pages": "2",
        "country": "pk",
        "date_posted": "all"
    }
    
    try:
        response = requests.get(URL, headers=HEADERS, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as e:
        status_code = response.status_code if response else "unknown"
        logger.error(f"HTTP {status_code} for role '{role}': {e}")
        if status_code == 429:
            logger.error("Rate limit exceeded. Consider increasing REQUEST_DELAY.")
        elif status_code in (401, 403):
            logger.error("Authentication failed. Check your API key.")
        raise
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error for role '{role}': {e}")
        raise
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout error for role '{role}': {e}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for role '{role}': {e}")
        raise
    except ValueError as e:
        logger.error(f"Failed to parse JSON response for role '{role}': {e}")
        raise
    
    jobs = []
    for job in data.get("data", []):
        jobs.append({
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "location": job.get("job_city"),
            "country": job.get("job_country"),
            "salary_min": job.get("job_min_salary"),
            "salary_max": job.get("job_max_salary"),
            "employment_type": job.get("job_employment_type"),
            "date_posted": job.get("job_posted_at_datetime_utc"),
            "is_remote": job.get("job_is_remote"),
            "description": job.get("job_description", "")[:300],
            "apply_link": job.get("job_apply_link")
        })
    
    logger.info(f"Fetched {len(jobs)} jobs for role '{role}'")
    return jobs

def fetch_data() -> list:
    """Fetch jobs for all roles. Raises exception on any failure."""
    all_jobs = []
    for role in ROLES:
        try:
            role_jobs = fetch_jobs_for_role(role)
            all_jobs.extend(role_jobs)
        except Exception as e:
            logger.error(f"Pipeline stopped due to error for role '{role}': {e}")
            raise  # Propagate the error
    return all_jobs

def get_job_data() -> list:
    """Main entry point. Returns job data or raises exception."""
    start_time = time.perf_counter()
    logger.info("Starting job data fetch pipeline")
    
    try:
        all_jobs = fetch_data()
    except Exception as e:
        logger.error(f"Data fetch pipeline failed: {e}")
        raise  # Re-raise to signal failure
    
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    
    if not all_jobs:
        logger.error("No jobs were fetched. Aborting pipeline.")
        raise ValueError("No jobs data fetched")
    
    logger.info(f"Pipeline completed in {elapsed_time:.2f} seconds. Total jobs: {len(all_jobs)}")
    return all_jobs
