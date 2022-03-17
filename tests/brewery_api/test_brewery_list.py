import requests
import pytest

brewery_list_url = "https://api.openbrewerydb.org/breweries"


def test_brewery_list_success():
    assert requests.get(brewery_list_url).status_code == 200


def test_brewery_list_returned():
    assert requests.get(brewery_list_url).json()[0]["id"]


@pytest.mark.parametrize("payload", [{"by_city": "san_diego"},
                                     {"by_name": "cooper"},
                                     {"by_dist": "38.8977,77.0365"},
                                     {"by_state": "ohio"},
                                     {"by_postal": "44107"},
                                     {"by_type": "micro"},
                                     {"page": "15"},
                                     {"per_page": "25"},
                                     {"sort": "type", "id": "asc"}])
def test_queries(payload):
    json_resp = requests.get(brewery_list_url, params=payload).json()
    assert json_resp[0]["id"]


@pytest.mark.parametrize("by_type", ["micro",
                                     "nano",
                                     "regional",
                                     "brewpub",
                                     "large",
                                     "planning",
                                     "bar",
                                     "contract",
                                     "closed"])
def test_by_type(by_type):
    json_resp = requests.get(brewery_list_url, params={"by_type": by_type}).json()
    assert json_resp[0]["id"]


def test_per_page():
    json_resp = requests.get(brewery_list_url, params={"per_page": 25}).json()
    assert len(json_resp) == 25


@pytest.mark.parametrize("numbers", [51, 60, 108, 1999])
def test_per_page_max_50(numbers):
    json_resp = requests.get(brewery_list_url, params={"per_page": numbers}).json()
    assert len(json_resp) == 50

def test_getting_brewery_by_id():
    json_resp = requests.get("https://api.openbrewerydb.org/breweries/madtree-brewing-cincinnati").json()
    assert json_resp["id"] == "madtree-brewing-cincinnati"
