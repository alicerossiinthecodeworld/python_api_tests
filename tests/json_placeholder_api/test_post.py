import requests
import pytest

post_url = "https://jsonplaceholder.typicode.com/posts"


@pytest.fixture()
def send_post():
    return requests.post(post_url, data={"title": "foo", "body": "bar", "userId": "1"})


@pytest.fixture()
def send_get():
    return requests.get(post_url)


def test_post_success(send_post):
    assert send_post.status_code == 201


def test_post_returns_id(send_post):
    assert send_post.json()["id"] is not None


@pytest.mark.parametrize("data", [{"title": "foo", "body": "bar", "userId": "1"},
                                  {"title": "fo", "body": "ba", "userId": "3"},
                                  {"title": "faa", "body": "bee", "userId": "5"}
                                  ])
def test_post_not_remembered(data):
    resp = requests.post(post_url, data=data)
    assert resp.json()["id"] == 101


@pytest.mark.parametrize("ids", (1, 2, 3, 4, 5))
def test_delete_post(ids):
    assert requests.delete(f"{post_url}/{ids}").status_code == 200


def test_delete_non_existing_post(send_get):
    resp = requests.delete(f"{post_url}/{len(send_get.json()) + 1}")
    assert resp.status_code == 200


def test_getting_posts_by_user():
    resp = requests.get(post_url, params={"userId": "1"})
    for posts in resp.json():
        assert posts["userId"] == 1


@pytest.mark.parametrize("services", ["comments", "photos", "albums", "todos"])
def test_listing_nested_resources(services):
    resp = requests.get(f"{post_url}/1/{services}")
    assert resp.status_code == 200
