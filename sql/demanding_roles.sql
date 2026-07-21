SELECT job_type, count(*) as job_openings 
FROM `data-engineering-bigquery.karachi_jobs_dataset.staging_jobs`
WHERE job_type!= 'unspecified'
GROUP BY job_type
ORDER BY job_type ASC;