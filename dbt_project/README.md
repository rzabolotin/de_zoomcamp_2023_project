# DBT project

## Description

Inside our BigQuery data warehouse we have tables.

In this project we will create models:
- fct_events (fact table)
- dim_organizations (dimension table)
- dim_locations (dimension table)
- lnk_event_locales (link table)

## How to run
First you need to specify dbt profile with name `cultura_ru` (or overwrite it in `dbt_project.yml`)

Then you can run:
- `poetry run dbt run` - to run all models
- `poetry run dbt test` - to run tests
- `poetry run dbt build` - to run all models and tests
- `poetry run dbt docs generate` - to generate documentation
- `poetry run dbt docs serve` - to run local server with documentation


