from prefect.deployments import Deployment
from flow_locales import locales_flow
from flow_orgs import orgs_flow
from flow_events import events_flow


def create_deployments():
    Deployment.build_from_flow(
        flow=locales_flow,
        name="Load locales",
        entrypoint="data_ingestion/flow_locales.py:locales_flow",
        apply=True,
    )

    Deployment.build_from_flow(
        flow=orgs_flow,
        name="Load organizations",
        entrypoint="data_ingestion/flow_orgs.py:orgs_flow",
        apply=True,
    )

    Deployment.build_from_flow(
        flow=events_flow,
        name="Load events",
        entrypoint="data_ingestion/flow_events.py:events_flow",
        apply=True,
    )


if __name__ == "__main__":
    create_deployments()