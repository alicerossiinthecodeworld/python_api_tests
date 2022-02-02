import pytest
import requests


def pytest_addoption(parser):
    parser.addoption("--baseurl", default="https://ya.ru",
                     help="Type the base URL. Default is https://ya.ru")

    parser.addoption("--status_code", default=200, help="Type the code if it is not 200")


@pytest.fixture()
def get_base_url(request):
    return request.config.getoption("--baseurl")


@pytest.fixture()
def get_status_code(request):
    return request.config.getoption("--status_code")


def test_check_status_code(get_base_url, get_status_code):
    assert requests.get(get_base_url).status_code == int(get_status_code)
