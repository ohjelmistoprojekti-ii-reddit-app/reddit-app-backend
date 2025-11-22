import allure
from app.config import Config
from datetime import datetime, timezone

from tests.helpers import get_country_subreddit

"""
These tests cover public API endpoints that do not require authentication.

TC-08 tests API endpoints that fetches static data.
TC-09 and forward test API endpoints that interact with the database (mocked).
"""


# TC-08: Fetch subreddits used in analyses

@allure.parent_suite("REST API tests")
@allure.suite("TC-08: Fetch subreddits used in analyses")
@allure.severity(allure.severity_level.CRITICAL)
class TestFetchSubredditsUsedInAnalyses:
    
    @allure.sub_suite("Fetch subreddits used in trending topics analysis")
    @allure.description("Test fetching subreddit options for trending topics analysis, and verify that they are returned correctly.")
    def test_fetch_subreddits_for_trending_topics(self, client):
        response = client.get('/api/subreddits/')
        assert response.status_code == 200
        
        data = response.get_json()
        assert isinstance(data, list)
        assert set(data) == set(Config.SUBREDDITS)


    @allure.sub_suite("Fetch subreddits used in country subreddit analysis")
    @allure.description("Test fetching subreddit options for country analysis, and verify that they are returned correctly.")
    def test_fetch_subreddits_for_country_analysis(self, client):
        response = client.get('/api/subreddits/countries')
        assert response.status_code == 200
        
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == len(Config.COUNTRY_SUBREDDITS)
        
        for expected in Config.COUNTRY_SUBREDDITS:
            assert expected in data


    @allure.sub_suite("Check that country subreddits include login requirement field")
    @allure.description("Test that country subreddit entries include the 'login_required' field, and verify its correctness.")
    def test_country_subreddits_include_login_requirement_field(self, client):
        response = client.get('/api/subreddits/countries')
        assert response.status_code == 200
        
        data = response.get_json()
        for entry in data:
            assert 'login_required' in entry
            assert entry['login_required'] in [0, 1]


# TC-09: Fetch topic analysis results

@allure.parent_suite("REST API tests")
@allure.suite("TC-09: Fetch topic analysis results")
@allure.severity(allure.severity_level.CRITICAL)
class TestFetchTopicAnalysisResults:
    
    @allure.sub_suite("Fetch topic analysis results with valid subreddit")
    @allure.description("Test fetching latest topic analysis results with valid parameters, and verify the response includes correct data with latest timestamp.")
    def test_fetch_topic_analysis_results_valid_params(self, client, mock_db):
        db = mock_db

        subreddit = "test"
        # Tested function uses 'posts' collection
        db["posts"].insert_many([
            {"subreddit": subreddit, "topic": "A", "timestamp": datetime(2025, 9, 1, 12, 0, tzinfo=timezone.utc)},
            {"subreddit": subreddit, "topic": "B", "timestamp": datetime(2025, 9, 1, 9, 0, tzinfo=timezone.utc)}
        ])

        response = client.get(f'/api/topics/latest/{subreddit}')
        assert response.status_code == 200

        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]['topic'] == 'A' # Latest topic


    @allure.sub_suite("Fetch topic analysis results with invalid subreddit")
    @allure.description("Test fetching latest topic analysis results with invalid parameters, and verify that status 404 is returned.")
    def test_fetch_topic_analysis_results_invalid_params(self, client, mock_db):
        db = mock_db

        # Tested function uses 'posts' collection
        db["posts"].insert_many([
            {"subreddit": "test", "topic": "A", "timestamp": datetime(2025, 9, 1, 12, 0, tzinfo=timezone.utc)},
            {"subreddit": "test", "topic": "B", "timestamp": datetime(2025, 9, 1, 9, 0, tzinfo=timezone.utc)}
        ])

        subreddit = "nonexistent"
        response = client.get(f'/api/topics/latest/{subreddit}')
        assert response.status_code == 404

        data = response.get_json()
        assert 'error' in data


    @allure.sub_suite("Fetch topic analysis results and verify response content")
    @allure.description("Test fetching latest topic analysis results and verify that response contains expected fields.")
    def test_verify_topic_analysis_response_content(self, client, mock_db):
        db = mock_db

        subreddit = "test"
        # Tested function uses 'posts' collection
        db["posts"].insert_many([
            {"subreddit": subreddit, "topic": "A", "timestamp": datetime(2025, 9, 1, 15, 0, tzinfo=timezone.utc)},
            {"subreddit": subreddit, "topic": "B", "timestamp": datetime(2025, 9, 1, 10, 0, tzinfo=timezone.utc)}
        ])

        response = client.get(f'/api/topics/latest/{subreddit}')
        assert response.status_code == 200

        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        
        expected_fields = ["subreddit", "topic", "timestamp"]
        for field in expected_fields:
            assert field in data[0].keys()


# TC-10: Fetch country analysis results
# Note that some country subreddits require authentication. These tests only cover subreddits that do not require login.

@allure.parent_suite("REST API tests")
@allure.suite("TC-10: Fetch country analysis results")
@allure.severity(allure.severity_level.CRITICAL)
class TestFetchCountryAnalysisResults:
    
    @allure.sub_suite("Fetch country analysis results with valid subreddit no login")
    @allure.description("Test fetching latest country analysis results with valid parameters, and verify the response includes correct data with latest timestamp. Fetching from a subreddit that does not require login.")
    def test_fetch_country_analysis_results_no_login(self, client, mock_db):
        db = mock_db

        # Get a country subreddit that does not require login
        subreddit = get_country_subreddit(login_required=0)

        # Tested function uses 'countries' collection
        db["countries"].insert_many([
            {"subreddit": subreddit, "post": "X", "timestamp": datetime(2025, 9, 1, 15, 0, tzinfo=timezone.utc)},
            {"subreddit": subreddit, "post": "Y", "timestamp": datetime(2025, 9, 1, 10, 0, tzinfo=timezone.utc)}
        ])

        response = client.get(f'/api/countries/latest/{subreddit}')
        assert response.status_code == 200

        data = response.get_json()
        assert isinstance(data, dict)

        # Saved test data is expected to be under 'posts' key
        assert 'posts' in data
        country_data = data['posts'][0]
        assert country_data['post'] == 'X' # Latest post


    @allure.sub_suite("Fetch country analysis results with invalid subreddit")
    @allure.description("Test fetching latest country analysis results with invalid parameters, and verify that status 404 is returned.")
    def test_fetch_country_analysis_results_invalid_params(self, client, mock_db):
        db = mock_db

        # Tested function uses 'countries' collection
        db["countries"].insert_many([
            {"subreddit": "country_test", "timestamp": datetime(2025, 9, 2, 15, 0, tzinfo=timezone.utc)},
            {"subreddit": "country_test", "timestamp": datetime(2025, 9, 1, 10, 0, tzinfo=timezone.utc)}
        ])

        subreddit = "nonexistent"
        response = client.get(f'/api/countries/latest/{subreddit}')
        assert response.status_code == 404

        data = response.get_json()
        assert 'error' in data


    @allure.sub_suite("Fetch country analysis results and verify response content")
    @allure.description("Test fetching latest country analysis results and verify that response contains expected fields.")
    def test_verify_country_analysis_response_content(self, client, mock_db):
        db = mock_db

        # Get a country subreddit that does not require login
        subreddit = get_country_subreddit(login_required=0)

        # Tested function uses 'countries' collection
        db["countries"].insert_many([
            {"subreddit": subreddit, "post": "X", "timestamp": datetime(2025, 9, 1, 15, 0, tzinfo=timezone.utc)},
            {"subreddit": subreddit, "post": "Y", "timestamp": datetime(2025, 9, 1, 10, 0, tzinfo=timezone.utc)}
        ])

        response = client.get(f'/api/countries/latest/{subreddit}')
        assert response.status_code == 200

        data = response.get_json()
        assert isinstance(data, dict)

        # Saved test data is expected to be under 'posts' key
        assert 'posts' in data
        country_data = data['posts'][0]
        
        expected_fields = ["subreddit", "post", "timestamp"]
        for field in expected_fields:
            assert field in country_data.keys()