# Data loader
This project is about to collect data from [culture.ru](https://pro.culture.ru) API and load it to GCS bucket.

## Data ingestion
To collect data I use request library and save json data from API and save it as parquet files locally.  

Main script is [data_loader.py](data_ingestion/data_loader.py). It can be run manually.

Example of usage:
```bash
poetry run python data_ingestion/data_loader.py orgs
```

You can load following information from API:
- Events (`events`)
- Organizations (`orgs`)
- Locations (`locales`)

## Orchestration
I use [Prefect](https://www.prefect.io/) to orchestrate data ingestion.  
I've created deployment script that encapsulates all the logic of data ingestion, and sends files it to GCS Bucket.

## Used prefect blocks
- You need to add block 


