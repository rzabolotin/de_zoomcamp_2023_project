# de_zoomcamp_2023_project

My project at [DataTalks Data Engineering zoomcamp course](https://github.com/DataTalksClub/data-engineering-zoomcamp)   
Cohort: **January 2023 - March 2023**  
Student: **Roman Zabolotin**

## Project description and dataset
There is platform [culture.ru](https://pro.culture.ru/new/api/documentation/export) with API. It contains information about events in the field of culture for the period from Jan 2021 to March 2023.  
In this project I used this data and made an ETL pipeline for it.
In this project I've made data warehouse with data from this API, and made data visualization with it.

The main goal of this project is to get experience in data engineering and data visualization.  
The secondary goal is to find main trends in the field of culture in Russia.

## Clouds
In this project I used [Google Cloud Platform](https://cloud.google.com/)  

Services:
  - [Google Cloud Storage](https://cloud.google.com/storage)
  - [BigQuery](https://cloud.google.com/bigquery)
  - [Dataproc](https://cloud.google.com/dataproc)
  - [Looker](https://looker.com/)

### Terraform
I've used terraform to create infrastructure in GCP.  
My terraform code is [here](terraform)

To deploy terraform project you need to run following steps:
1. Authenticate to GCP
```bash
gcloud auth application-default login
```

2. Fill `terraform.tfvars` file (you can use terraform.tfvars.example as example)


3. Run terraform
```bash
terraform init
terraform apply
```

It will create:
- GCS bucket
- BigQuery dataset


## Data ingestion
- Description
- Orchestration
- Docker (remove poetry)

I've ingested the following information from API:
- Events
- Places
- Organizations
- Categories
- Tags
- Locations

To ingest data I write [the script](src/data_ingestion/data_loader.py)  
Run it in orchestration tool (Prefect) with [the flow](src/data_ingestion/flow.py)

## Loading to DWH
- Spark
- Orchestration

## Transformation
- Dbt
- Orchestration Dbt run

## Data visualization
- Superset
- Looker

## Additional
- Tests
- CI/CD
- Scheme of pipeline


> To load environment from your .env file run:
```bash
export $(cat .env | xargs)
```