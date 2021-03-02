import requests_mock

from pytest import fixture

from scraper_alloforfait import Package


@fixture
def response_free():
    """Mock requests response of alloforfait free package"""

    with open("free_response.html", "r") as reader:
        response = reader.read()

    return response


@fixture
def response_sfr():
    """Mock requests response of alloforfait sfr package"""

    with open("sfr_response.html", "r") as reader:
        response = reader.read()

    return response


@fixture
def response_bouygues():
    """Mock requests response of alloforfait bouygues package"""

    with open("bouygues_response.html", "r") as reader:
        response = reader.read()

    return response


def test_scrapper_alloforfait_free(response_free):
    with requests_mock.Mocker() as mock_request:
        mock_request.get("https://alloforfait.fr/tv/free/", text=response_free)
        free = Package("free").channels()

    assert free[0] == (1, "TF1")
    assert free[-1] == (944, "AS TV")
    assert len(free) == 224


def test_scrapper_alloforfait_sfr(response_sfr):
    with requests_mock.Mocker() as mock_request:
        mock_request.get("https://alloforfait.fr/tv/sfr/", text=response_sfr)
        sfr = Package("sfr").channels()

    assert sfr[0] == (1, "TF1")
    assert sfr[-1] == (945, "NET VIET")
    assert len(sfr) == 172


def test_scrapper_alloforfait_bouygues(response_bouygues):
    with requests_mock.Mocker() as mock_request:
        mock_request.get(
            "https://alloforfait.fr/tv/bbox-bouygues-telecom/", text=response_bouygues
        )
        bouygues = Package("bbox-bouygues-telecom").channels()

    assert bouygues[0] == (1, "TF1")
    assert bouygues[-1] == (802, "NTD")
    assert len(bouygues) == 191
