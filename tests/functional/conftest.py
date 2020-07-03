import os

import psycopg2
import requests
import requests.exceptions

import pytest


def is_postgresql_responsive(url):
    """Check if a PostgreSQL database is responsive."""
    try:
        psycopg2.connect(url)
    except psycopg2.OperationalError:
        return False
    return True


def is_http_responsive(url, require_200=True):
    """Check if an HTTP endpoint is responsive."""
    try:
        response = requests.get(url)
        if response.status_code == 200 or not require_200:
            return True
    except requests.exceptions.ConnectionError:
        return False


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    # Turn on verbose logging during tests.
    os.environ["MINTEL_LOGGING_LEVEL"] = "DEBUG"

    return pytestconfig.rootdir / "docker" / "docker-compose.yaml"


@pytest.fixture(scope="session")
def service_url(docker_ip, docker_services):
    port = docker_services.port_for("proxy", 80)
    url = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=30.0,
        pause=0.1,
        check=lambda: is_http_responsive(f"{url}/health-check/"),
    )
    return url


@pytest.fixture(scope="session")
def db_url(docker_ip, docker_services):
    """Create a PostgreSQL container to use for the DB and return a URL."""
    port = docker_services.port_for("db", 5432)
    url = f"postgresql://mad_libz:mad_libz@{docker_ip}:{port}/mad_libz"

    docker_services.wait_until_responsive(
        timeout=90, pause=0.1, check=lambda: is_postgresql_responsive(url)
    )
    return url
