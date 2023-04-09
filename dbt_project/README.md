# DBT project

## Description

Inside our BigQuery data warehouse we have tables.

In this project we will create 3 models:
- events (fact table)
- organizations (dimension table)
- locations (dimension table)

## How to run
First you need to specify dbt profile with name `cultura_ru` (or overwrite it in `dbt_project.yml`)

Then you can run:
- `poetry run dbt run` - to run all models
- `poetry run dbt test` - to run tests


