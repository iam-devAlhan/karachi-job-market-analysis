SELECT seniority, count(*) as job_openings 
FROM `data-engineering-bigquery.karachi_jobs_dataset.staging_jobs`
WHERE seniority != 'unspecified'
GROUP BY seniority
ORDER BY seniority ASC;