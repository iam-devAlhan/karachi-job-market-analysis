import json
import pandas as pd


jobs_data = []
with open("raw_jobs_2026-07-13.json","r") as f:
    jobs_data = json.load(f)

# COnverting into Dataframe and then appropriate SQL Table format for Data Warehouse Loading
