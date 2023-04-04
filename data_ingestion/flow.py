from prefect import task, flow


@task(log_prints=True)
def load_1():
    print("Loading 1")
    return "Loaded 1"

@flow(log_prints=True)
def test_flow():
    load_1()
    print("Done")


if __name__ == "__main__":
    test_flow()

