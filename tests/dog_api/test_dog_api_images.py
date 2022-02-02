import requests
import pytest
import random
from test_dog_api_breeds import get_list_of_breeds, get_breeds, get_random_subbreeds

random_image_url = "https://dog.ceo/api/breeds/image/random"
image_formats = ("image/png", "image/jpeg", "image/jpg")


@pytest.fixture()
def get_random_number_of_pics():
    return requests.get(f"{random_image_url}/{random.randint(0, 50)}")


@pytest.fixture()
def get_random_breed_image(get_list_of_breeds):
    breed = get_list_of_breeds[random.randint(0, len(get_list_of_breeds)-1)]
    return requests.get(f"https://dog.ceo/api/breed/{breed}/images")


@pytest.fixture()
def get_json():
    return requests.get(random_image_url).json()


def test_success_status():
    response = requests.get(random_image_url)
    assert response.status_code == 200


def test_json_returns(get_json):
    assert get_json is not None


def test_json_has_message(get_json):
    assert get_json['message'] is not None


def test_message_a_valid_link(get_json):
    response = requests.get(get_json['message'])
    assert response.status_code == 200


def test_link_leads_to_image(get_json):
    resp = requests.get(get_json['message'])
    assert resp.headers["content-type"] in image_formats


def test_getting_multiple_pictures_success(get_random_number_of_pics):
    assert get_random_number_of_pics.status_code == 200


@pytest.mark.parametrize("number", [3, 5, 10, 15, 49, 50])
def test_number_of_pics_equals_argument(number):
    resp = requests.get(f'{random_image_url}/{number}')
    assert len(resp.json()["message"]) == number


@pytest.mark.parametrize("number", [50, 51, 100, 100, 150])
def test_more_than_fifty_pics(number):
    resp = requests.get(f'{random_image_url}/{number}')
    assert (len(resp.json()["message"])) == 50


def test_image_by_breed_success(get_random_breed_image):
    assert get_random_breed_image.status_code == 200


def test_link_returns_by_breed(get_random_breed_image):
    assert get_random_breed_image.json()["message"] is not None

def test_non_existing_breed():
    error_message = requests.get("https://dog.ceo/api/breed/1/images").json()["message"]
    assert error_message == "Breed not found (master breed does not exist)"

def test_link_returns_image(get_random_breed_image):
    links = list(get_random_breed_image.json()["message"])
    resp = requests.get(links[random.randint(0, len(links)-1)])
    assert resp.headers["content-type"] in image_formats


def test_image_by_subbreed_success():
    assert requests.get("https://dog.ceo/api/breed/hound/afghan/images").status_code == 200


def test_non_existing_breed_returns_error():
    error_message = requests.get("https://dog.ceo/api/breed/husky/123/images").json()["message"]
    assert error_message == "Breed not found (sub breed does not exist)"

