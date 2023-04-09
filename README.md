# de_zoomcamp_2023_project

My project at [DataTalks Data Engineering zoomcamp course](https://github.com/DataTalksClub/data-engineering-zoomcamp)   
Cohort: **January 2023 - March 2023**  
Student: **Roman Zabolotin**

## Project description and dataset
![img.png](media/cultura_logo.png)

I found data for project at platform **[culture.ru](https://pro.culture.ru)** with an API access.  
It contains information about events in the field of culture for the period from *Jan 2021* to *March 2023*.
In this project I use this data for making ETL pipelines, moving data to data warehouse and visualization.

The main goal of this project is to get hands-on experience in data engineering.   
The secondary goal is to find main trends in the field of culture in Russia.

## Cloud platform

![img.png](media/gcloud_logo.png)

In this project I use [Google Cloud Platform](https://cloud.google.com/)  

Services:
  - [Google Cloud Storage](https://cloud.google.com/storage)
  - [BigQuery](https://cloud.google.com/bigquery)
  - [Looker](https://looker.com/)

### Terraform
I used terraform to create infrastructure in GCP.  
My terraform code is presented [here](terraform/main.tf)

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


## Data ingestion and loading to DWH
To collect data I use [API](https://pro.culture.ru/api/v1/docs/) of platform **[culture.ru](https://pro.culture.ru)**  
I've written a special script to collect data from that API.  
Then I've used [Prefect](https://www.prefect.io/) to orchestrate the process of data ingestion.

It gathers data from 3 API methods:
- events
- locations
- organizations

For each method I've created a separate flow in Prefect.

Example of flow diagram for events endpoint:
![img.png](media/prefect_flow.png)


Each flow has 4 main tasks:
- **load_data** - get data from API
- **save_to_parquet** - save data in parquet format
- **upload_to_gcs** - upload data to GCS
- **load_to_bq** - load data to BigQuery

Some flows make more than one table in BigQuery.  
The resulted list of tables in BigQuery is:
- events
- event_tags
- event_places
- event_locales
- event_seances
- locales
- organizations
- organization_locales

**More information about data ingestion you can find [here](data_ingestion/README.MD)**

## Optimizing data warehouse
The biggest table in the project is **events** table.  So let's make partitioning for it.  
After all data was loaded to BigQuery I've made one more flow in Prefect to optimize data warehouse.

In [this flow](data_ingestion/flow_optimization.py) I run bigquery queries to make partitioning for **events** table.

![img.png](media/big_query_partitioning.png)





## Transformation
- Dbt
- Orchestration Dbt run

## Data visualization
- Superset
- Looker
