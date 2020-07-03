import pytest
import requests


@pytest.mark.postbuild
def test_image_runs(service_url):
    # this test is a bit redundant, but I wanted to demonstrate using the pytest-docker
    # fixture to run tests on the built image
    healthcheck_endpoint = f"{service_url}/health-check/"
    response = requests.get(healthcheck_endpoint)
    response.raise_for_status()
