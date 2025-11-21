import allure
import pytest
from app.config import Config

""" Tests for public API endpoints that do not require authentication. """


""" TC-08: Fetch list of subreddits """

@allure.parent_suite("REST API tests")
@allure.suite("TC-08 - Fetch subreddits used in analyses")
@allure.sub_suite("Fetch subreddits used in trending topics analysis")
@allure.description("Test fetching subreddit options for trending topics analysis, and verify that they are returned correctly.")
@allure.severity(allure.severity_level.CRITICAL)
def test_fetch_subreddits_for_trending_topics(client):
    response = client.get('/api/subreddits/')
    assert response.status_code == 200
    
    data = response.get_json()
    assert isinstance(data, list)
    assert set(data) == set(Config.SUBREDDITS)


@allure.parent_suite("REST API tests")
@allure.suite("TC-08 - Fetch subreddits used in analyses")
@allure.sub_suite("Fetch subreddits used in country subreddit analysis")
@allure.description("Test fetching subreddit options for country analysis, and verify that they are returned correctly.")
@allure.severity(allure.severity_level.CRITICAL)
def test_fetch_subreddits_for_country_analysis(client):
    response = client.get('/api/subreddits/countries')
    assert response.status_code == 200
    
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == len(Config.COUNTRY_SUBREDDITS)
    
    for expected in Config.COUNTRY_SUBREDDITS:
        assert expected in data


@allure.parent_suite("REST API tests")
@allure.suite("TC-08 - Fetch subreddits used in analyses")
@allure.sub_suite(" country subreddits include login requirement field")
@allure.description("Test that country subreddit entries include the 'login_required' field, and verify its correctness.")
@allure.severity(allure.severity_level.CRITICAL)
def test_country_subreddits_include_login_requirement_field(client):
    response = client.get('/api/subreddits/countries')
    assert response.status_code == 200
    
    data = response.get_json()
    for entry in data:
        assert 'login_required' in entry
        assert entry['login_required'] in [0, 1]


