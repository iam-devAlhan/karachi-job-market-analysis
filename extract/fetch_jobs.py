import requests
import os
from dotenv import load_dotenv
import time
import json
from datetime import datetime


load_dotenv()

url = "https://jsearch.p.rapidapi.com/search"

rapid_api_key = os.getenv("RAPID_API_KEY", "")
rapid_api_host = os.getenv("RAPID_API_HOST", "")
headers = {
	"x-rapidapi-key": rapid_api_key,
	"x-rapidapi-host": rapid_api_host,
	"Content-Type": "application/json"
}

roles = [
    "python developer in karachi",
    "ai engineer/ai automation in karachi",
    "full stack developer in karachi",
    "machine learning engineer role in karachi",
    "devops/cloud roles in karachi",
    "cybersecurity roles in karachi",
    "sap consultant roles in karachi",
    "odoo technical roles in karachi",
    "sqa/qa automation roles in karachi"
]

def fetch_data() -> list:
    jobs = []
    for role in roles:
        time.sleep(1.0)
        params = {
            "query":role,
            "page":"1",
            "num_pages":"2",
            "country":"pk",
            "date_posted":"all"
        }
        

        response = requests.get(url, headers=headers, params=params)

        data = response.json()
        
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

    
    return jobs


all_jobs = []
start_time = time.perf_counter()
print(f"-> Starting job for Fetching Jobs Data")
jobs_data = fetch_data()
all_jobs.extend(jobs_data)


with open(f"raw_jobs_{datetime.now().strftime('%Y-%m-%d')}.json", "w") as f:
    json.dump(all_jobs, f, indent=2, default=str)

print("-> Raw Data Saved!")

end_time = time.perf_counter()
elapsed_time = end_time - start_time

print(f"-> Job Completed in total seconds: {elapsed_time:.2f} secs")
