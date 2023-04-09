from flow_events import events_flow
from flow_locales import locales_flow
from flow_optimization import partitioning_flow
from flow_orgs import orgs_flow
from prefect.deployments import Deployment
from prefect.filesystems import GitHub


def create_deployments():
    github_block = GitHub.load("de-proj-repo")

    Deployment.build_from_flow(
        flow=locales_flow,
        name="Load locales",
        storage=github_block,
        entrypoint="data_ingestion/flow_locales.py:locales_flow",
        apply=True,
    )

    Deployment.build_from_flow(
        flow=orgs_flow,
        name="Load organizations",
        storage=github_block,
        entrypoint="data_ingestion/flow_orgs.py:orgs_flow",
        apply=True,
    )

    Deployment.build_from_flow(
        flow=events_flow,
        name="Load events",
        storage=github_block,
        entrypoint="data_ingestion/flow_events.py:events_flow",
        apply=True,
    )

    Deployment.build_from_flow(
        flow=partitioning_flow,
        name="Make partition for events",
        storage=github_block,
        entrypoint="data_ingestion/flow_optimization.py:partitioning_flow",
        apply=True,
    )


if __name__ == "__main__":
    create_deployments()
