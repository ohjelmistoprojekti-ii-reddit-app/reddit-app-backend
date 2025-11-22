import allure
import pytest
from datetime import datetime, timedelta, timezone
from app.services.db import get_latest_data_by_subreddit, get_post_numbers_by_timeperiod, get_top_topics_by_timeperiod

"""
These tests cover database operations for analysis results retrieval and statistics calculation.
The used datasets include only the necessary fields for the tested functions.
"""


# TC-05: Fetch latest analysis results from database

@allure.parent_suite("Database tests")
@allure.suite("TC-05: Fetch latest analysis results from database")
@allure.severity(allure.severity_level.CRITICAL)
class TestFetchLatestAnalysisResultsFromDatabase:
    @allure.sub_suite("Fetch latest data without type filter")
    @allure.description("Test fetching latest data without type filter from the database, and verify that correct documents (with most recent timestamp) are returned.")
    def test_fetch_latest_results_without_type_filter(self, mock_db):
        db = mock_db
        test_data = [
            { "label": "Topic A", "subreddit": "example", "timestamp": datetime(2025, 9, 1, 10, 0, tzinfo=timezone.utc) },
            { "label": "Topic B", "subreddit": "example", "timestamp": datetime(2025, 10, 1, 10, 0, tzinfo=timezone.utc) },
            { "label": "Topic C", "subreddit": "example", "timestamp": datetime(2025, 11, 1, 10, 0, tzinfo=timezone.utc) },
        ]

        collection = "test_collection"
        db[collection].insert_many(test_data)

        fetched_data = get_latest_data_by_subreddit(collection, subreddit=test_data[0]["subreddit"])
        assert isinstance(fetched_data, list)
        assert len(fetched_data) == 1

        most_recent_data = list(db[collection].find({}, sort=[("timestamp", -1)]))
        
        fetched = fetched_data[0]
        most_recent = most_recent_data[0]
        assert fetched["timestamp"] == most_recent["timestamp"]
        assert fetched["label"] == most_recent["label"]


    @allure.sub_suite("Fetch latest data with type filter")
    @allure.description("Test fetching latest data with type filter from the database, and verify that correct documents (with most recent timestamp and correct type) are returned.")
    def test_fetch_latest_results_with_type_filter(self, mock_db):
        db = mock_db

        test_data = [
            { "type": "topics", "label": "Topic A", "subreddit": "example", "timestamp": datetime(2025, 9, 1, 10, 0, tzinfo=timezone.utc) },
            { "type": "topics", "label": "Topic B", "subreddit": "example", "timestamp": datetime(2025, 10, 1, 10, 0, tzinfo=timezone.utc) },
            { "type": "posts", "posts": [{"title": "Example post"}], "subreddit": "example", "timestamp": datetime(2025, 11, 1, 10, 0, tzinfo=timezone.utc) },
        ]

        collection = "test_collection"
        db[collection].insert_many(test_data)

        fetched_data = get_latest_data_by_subreddit(collection, subreddit=test_data[0]["subreddit"], type="topics")
        assert isinstance(fetched_data, list)
        assert len(fetched_data) == 1 # Check that only one document of type "topics" is returned

        # Verify that the returned document is the most recent one of type "topics"
        most_recent_topics = list(db[collection].find({"type": "topics"}, sort=[("timestamp", -1)]))

        fetched = fetched_data[0]
        most_recent = most_recent_topics[0]
        assert fetched["timestamp"] == most_recent["timestamp"]
        assert fetched["label"] == most_recent["label"]


    @allure.sub_suite("Fetch latest data from nonexistent subreddit")
    @allure.description("Test fetching latest data from a nonexistent subreddit, and verify that an empty list is returned.")
    def test_fetch_latest_results_from_nonexistent_subreddit(self, mock_db):
        db = mock_db

        test_data = [
            { "label": "Topic A", "subreddit": "example", "timestamp": datetime(2025, 9, 1, 10, 0, tzinfo=timezone.utc) },
            { "label": "Topic B", "subreddit": "example", "timestamp": datetime(2025, 10, 1, 10, 0, tzinfo=timezone.utc) },
        ]

        collection = "test_collection"
        db[collection].insert_many(test_data)

        fetched_data = get_latest_data_by_subreddit(collection, subreddit="nonexistent")
        assert isinstance(fetched_data, list)
        assert len(fetched_data) == 0


    @allure.sub_suite("Fetch latest data using invalid filter")
    @allure.description("Test fetching latest data using invalid filter, and verify that a ValueError or TypeError is raised.")
    def test_fetch_latest_results_using_invalid_filter_type(self, mock_db):
        db = mock_db

        test_data = [
            { "label": "Topic A", "subreddit": "example", "timestamp": datetime(2025, 9, 1, 10, 0, tzinfo=timezone.utc) },
            { "label": "Topic B", "subreddit": "example", "timestamp": datetime(2025, 10, 1, 10, 0, tzinfo=timezone.utc) },
        ]

        collection = "test_collection"
        db[collection].insert_many(test_data)

        with pytest.raises((ValueError, TypeError)):
            get_latest_data_by_subreddit(collection, subreddit=test_data[0]["subreddit"], type="invalid")


# TC-06: Calculate post number statistics from analysis results

@allure.parent_suite("Database tests")
@allure.suite("TC-06: Calculate post number statistics from analysis results")
@allure.severity(allure.severity_level.NORMAL)
class TestCalculatePostNumberStatistics:
    
    @allure.sub_suite("Calculate post numbers for existing subreddit")
    @allure.description("Test calculating post numbers for existing subreddit, and verify that the correct post count statistics are returned. Expects today's statistics to be included.")
    def test_calculate_post_numbers_for_existing_subreddit(self, mock_db):
        db = mock_db

        # Ensure test data includes today's date
        current_date = datetime.now(timezone.utc)
        test_data =[
            { "subreddit": "example", "num_posts": 5, "timestamp": current_date },
            { "subreddit": "example", "num_posts": 10, "timestamp": (current_date - timedelta(days=1)) },
            { "subreddit": "example", "num_posts": 15, "timestamp": (current_date - timedelta(days=2)) },
        ]

        # Tested function uses hardcoded collection name "posts"
        db["posts"].insert_many(test_data)

        # High number_of_days to include all test data
        number_of_days = 10
        post_stats = get_post_numbers_by_timeperiod(subreddit="example", number_of_days=number_of_days)
        assert isinstance(post_stats, list)
        results = post_stats[0]

        current_date_str = current_date.strftime("%Y-%m-%d")

        current_date_found = False
        for stat in results["daily"]:
            if stat["day"] == current_date_str:
                current_date_found = True
                break

        assert current_date_found # Verify that today's statistics are included
        assert results["total_posts"] == 30 # 5 + 10 + 15


    @allure.sub_suite("Calculate post numbers for nonexistent subreddit")
    @allure.description("Test calculating post numbers for nonexistent subreddit, and verify that an empty list is returned.")
    def test_calculate_post_numbers_for_nonexistent_subreddit(self, mock_db):
        db = mock_db

        current_date = datetime.now(timezone.utc)
        test_data = [
            { "subreddit": "example", "num_posts": 5, "timestamp": current_date },
            { "subreddit": "example", "num_posts": 10, "timestamp": (current_date - timedelta(days=1)) },
        ]

        # Tested function uses hardcoded collection name "posts"
        db["posts"].insert_many(test_data)

        post_stats = get_post_numbers_by_timeperiod(subreddit="nonexistent", number_of_days=2)
        assert isinstance(post_stats, list)
        assert len(post_stats) == 0


    @allure.sub_suite("Calculate post numbers with invalid number of days")
    @allure.description("Test calculating post numbers with invalid number of days, and verify that a ValueError is raised.")
    def test_calculate_post_numbers_with_invalid_number_of_days(self, mock_db):
        with pytest.raises(ValueError):
            get_post_numbers_by_timeperiod(subreddit="example", number_of_days=-2)



# TC-07: Calculate top topics statistics from analysis results

@allure.parent_suite("Database tests")
@allure.suite("TC-07: Calculate top topics statistics from analysis results")
@allure.severity(allure.severity_level.NORMAL)
class TestCalculateTopTopicsStatistics:
    
    @allure.sub_suite("Calculate top topics for existing subreddit")
    @allure.description("Test calculating top topics for existing subreddit, and verify that the correct topics statistics are returned. Expects today's statistics to be included.")
    def test_calculate_top_topics_for_existing_subreddit(self, mock_db):
        db = mock_db

        # Ensure test data includes today's date
        current_date = datetime.now(timezone.utc)
        test_data =[
            { "subreddit": "example", "topic": ["A", "B", "C"], "timestamp": current_date },
            { "subreddit": "example", "topic": ["A", "B", "Z"], "timestamp": (current_date - timedelta(days=1)) },
            { "subreddit": "example", "topic": ["A", "Y", "X"], "timestamp": (current_date - timedelta(days=2)) },
        ]

        # Tested function uses hardcoded collection name "posts"
        db["posts"].insert_many(test_data)

        # High number_of_days to include all test data
        number_of_days = 10
        limit = 3
        topic_stats = get_top_topics_by_timeperiod(subreddit="example", number_of_days=number_of_days, limit=limit)
        
        assert isinstance(topic_stats, list)
        results = topic_stats[0]
        
        assert results["topics"][0]["topic"] == "A" # Topic A should be the most frequent
        assert results["topics"][0]["count"] == 3   # Topic A should appear 3 times if today's data is included
        assert len(results["topics"]) == limit      # Amount of topics should match the limit


    @allure.sub_suite("Calculate top topics for nonexistent subreddit")
    @allure.description("Test calculating top topics for nonexistent subreddit, and verify that an empty list is returned.")
    def test_calculate_top_topics_for_nonexistent_subreddit(self, mock_db):
        db = mock_db

        current_date = datetime.now(timezone.utc)
        test_data = [
            { "subreddit": "example", "topic": ["A", "B", "C"], "timestamp": current_date },
            { "subreddit": "example", "topic": ["A", "B", "Z"], "timestamp": (current_date - timedelta(days=1)) },
        ]

        # Tested function uses hardcoded collection name "posts"
        db["posts"].insert_many(test_data)

        topic_stats = get_top_topics_by_timeperiod(subreddit="nonexistent", number_of_days=2, limit=3)
        assert isinstance(topic_stats, list)
        assert len(topic_stats) == 0


    @allure.sub_suite("Calculate top topics with large limit")
    @allure.description("Test calculating top topics with a large limit, and verify that all available topics are returned without error.")
    def test_calculate_top_topics_with_large_limit(self, mock_db):
        db = mock_db

        current_date = datetime.now(timezone.utc)
        test_data = [
            { "subreddit": "example", "topic": ["A", "B", "C"], "timestamp": current_date },
            { "subreddit": "example", "topic": ["A", "B", "D"], "timestamp": (current_date - timedelta(days=1)) },
        ]

        # Tested function uses hardcoded collection name "posts"
        db["posts"].insert_many(test_data)

        large_limit = 50
        topic_stats = get_top_topics_by_timeperiod(subreddit="example", number_of_days=2, limit=large_limit)
        
        assert isinstance(topic_stats, list)
        results = topic_stats[0]
        
        # Expecting all unique topics (A, B, C, D) to be returned (today's data included)
        assert len(results["topics"]) == 4


    @allure.sub_suite("Calculate top topics with invalid number of days")
    @allure.description("Test calculating top topics with invalid number of days, and verify that a ValueError is raised.")
    def test_calculate_top_topics_with_invalid_number_of_days(self, mock_db):
        with pytest.raises(ValueError):
            get_top_topics_by_timeperiod(subreddit="example", number_of_days=-3, limit=3)


    @allure.sub_suite("Calculate top topics with invalid limit")
    @allure.description("Test calculating top topics with invalid limit, and verify that a ValueError is raised.")
    def test_calculate_top_topics_with_invalid_limit(self, mock_db):
        with pytest.raises(ValueError):
            get_top_topics_by_timeperiod(subreddit="example", number_of_days=3, limit=-3)
