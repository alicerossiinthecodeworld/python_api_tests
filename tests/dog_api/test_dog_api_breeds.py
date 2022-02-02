import requests
import pytest
import random

breeds_url = "https://dog.ceo/api/breeds/list/all"


@pytest.fixture()
def get_breeds():
    return requests.get(breeds_url)


@pytest.fixture()
def get_random_subbreeds(get_list_of_breeds):
    breeds = get_list_of_breeds[random.randint(0, len(get_list_of_breeds))]
    return requests.get(f"https://dog.ceo/api/breed/{breeds}/list")


@pytest.fixture()
def get_list_of_breeds(get_breeds):
    return list(get_breeds.json()["message"].keys())


def test_list_of_breeds_success(get_breeds):
    assert get_breeds.status_code == 200


def test_breeds_returned(get_breeds):
    assert get_breeds.json()["message"] is not None


def test_subbreeds_success(get_random_subbreeds):
    assert get_random_subbreeds.status_code == 200


def test_subbreed_returns_link(get_random_subbreeds):
    assert get_random_subbreeds.json()["message"] is not None

