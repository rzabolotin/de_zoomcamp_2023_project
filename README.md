# de_zoomcamp_2023_project

My data engineering project at DataTalks zoomcamp course (2023 cohort)

## Project description and dataset

In this project I user data from [Culture.ru service](https://pro.culture.ru/new/api/documentation/export).  
It contains information about cultural events in Russia (the data is updated daily).

I ingested the following information:
- Events
- Places
- Organizations
- Categories
- Tags
- Locations

## Project plan

1. Step 1. Extract data from API
2. Step 2. Clean and store data in Google Cloud Storage
3. Step 3. Load data to BigQuery
4. Step 4. Make datamart (dbt)
5. Step 5. Make data visualization (Superset)


## Used technologies

1. Python as main programming language
2. Google Cloud Platform (GCP)
3. Prefect as ETL orchestrator
4. Poetry as dependency manager

linters
tests
add pre-commit hooks


