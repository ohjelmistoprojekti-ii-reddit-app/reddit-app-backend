# Test Cases

Test cases have been designed to cover the main functionalities of the Reddit Analyzer backend, focusing on database operations and REST API endpoints. Each test case includes a description, priority level, test steps, objectives, input parameters, and expected results.

Please refer to the [Test Plan](./test_plan.md) for an overview of the testing strategy and areas under test.

## Database Tests

Database tests will be unit tests. Our database contains diverse data, and no schemas or mandatory fields have been defined, so data integrity validation is not the focus. Instead, we will focus on verifying that database functions work as expected. We will use a test database created using *mongomock*.

### TC-01 - Save Data to Database
**Description**: Tests the `save_data_to_database(data_to_save, collection)` function to ensure data is **saved correctly** and errors are handled appropriately.  
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Save a single document | Ensure single document is saved correctly | Valid document | Document is added to the collection |
| 2 | Save a list of documents | Ensure multiple documents are saved correctly | List of valid documents | All documents are added to the collection |
| 3 | Save an empty document list | Ensure error handling works | Empty list | `ValueError` or equivalent |
| 4 | Save invalid data type | Ensure error handling works | Invalid type, e.g., string | `TypeError` or equivalent |


### TC-02 - Fetch Data from Database
**Description**: Tests the `fetch_data_from_collection(collection, filter=None)` function to ensure data **retrieval works correctly** and errors are handled appropriately.  
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch all documents | Ensure fetching all documents works normally | No `filter` | Returns all documents as a list |
| 2 | Fetch documents using filter | Ensure filtered fetch works correctly | Valid `filter` | Returns documents matching the filter |
| 3 | Fetch a non-existent document | Ensure fetch handles missing data correctly | Invalid `filter` | Returns empty list |


### TC-03 - Update Document in Database
**Description**: Tests the `update_one_item_in_collection(collection, filter, update)` function to ensure data **is updated correctly** and errors are handled appropriately.  
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Update existing document | Ensure update succeeds | Valid `filter` and `update` | Document is updated successfully |
| 2 | Update non-existent document | Ensure error handling works | Invalid `filter` | `ValueError` or equivalent |
| 3 | Update with invalid filter | Ensure error handling works | Invalid `filter`, e.g., string | `TypeError` or equivalent |


### TC-04 - Delete Document from Database
**Description**: Tests the `delete_one_item_from_collection(collection, filter)` function to ensure data **is deleted correctly** and errors are handled appropriately.  
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Delete existing document | Ensure deletion succeeds | Valid `filter` | Document is deleted successfully |
| 2 | Delete non-existent document | Ensure error handling works | Invalid `filter` | `ValueError` or equivalent |
| 3 | Delete with invalid filter | Ensure error handling works | Invalid `filter`, e.g., string | `TypeError` or equivalent |

---

> **NOTE:**
> For the next tests involving analysis results, a more comprehensive test dataset should be created covering different types of analysis results and multiple timestamps.
> For clarity, analysis-specific tests should be separated from basic CRUD tests.

### TC-05 - Fetch Latest Analysis Results by Subreddit
**Description**: Tests `get_latest_data_by_subreddit(collection, subreddit, type=None)` to ensure it **returns the latest data correctly** and handles errors appropriately.  
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch latest documents without `type` filter | Ensure latest documents are returned | Valid `subreddit` | Returns document with latest timestamp |
| 2 | Fetch latest documents with `type` filter | Ensure filtering by analysis type works | Valid `subreddit` and `type` | Returns document with latest timestamp and correct type |
| 3 | Fetch from non-existent subreddit | Ensure missing subreddit is handled correctly | Invalid `subreddit` | Returns empty list |
| 4 | Fetch with invalid `type` parameter | Ensure error handling works | Invalid `type` (not `posts` or `topics`) | `ValueError` or equivalent |



### TC-06 - Count Post Numbers by Time Period
**Description**: Tests `get_post_numbers_by_timeperiod(subreddit, number_of_days)` to ensure it **calculates post counts correctly** and handles errors appropriately.  
**Priority**: Medium  
**Note**: Test data must include posts across multiple days so that the counting logic can be properly verified.

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch posts for existing subreddit | Ensure counts are correct | Valid `subreddit` and `number_of_days` | Returns list of post counts, all counts correct |
| 2 | Fetch posts for non-existent subreddit | Ensure missing subreddit is handled correctly | Invalid `subreddit` | Returns empty list |
| 3 | Fetch with invalid `number_of_days` | Ensure error handling works | Invalid `number_of_days`, e.g., negative | `ValueError` or equivalent |



### TC-07 - Fetch Top Topics by Time Period
**Description**: Tests `get_top_topics_by_timeperiod(subreddit, number_of_days, limit)` to ensure it **returns topics in correct order and counts** and handles errors appropriately.  
**Priority**: Medium  
**Note**: Test data must include posts across multiple days with various topics so that the ranking logic can be properly verified.

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch top topics for existing subreddit | Ensure top topics are calculated correctly | Valid `subreddit`, `number_of_days`, `limit` | Returns list of top topics in order, count = `limit` |
| 2 | Fetch top topics for non-existent subreddit | Ensure missing subreddit is handled correctly | Invalid `subreddit` | Returns empty list |
| 3 | Fetch with large `limit` | Ensure function returns all available topics without error | Valid `subreddit`, large `limit` | Returns all top topics, count < `limit` |
| 4 | Fetch with invalid `number_of_days` | Ensure error handling works | Invalid `number_of_days`, e.g., negative | `ValueError` or equivalent |


---

## REST API and User Management Tests

REST API tests follow the priority order defined in the test plan. First, we will test public endpoints that are always accessible, then user management (login/register etc.), and lastly authenticated actions that require login.

*All endpoints and their details are listed in the test plan (see docs-folder)*

### Public endpoints (no authentication required)

#### TC-08 - Fetch List of Subreddits
**Description**: Tests `/api/subreddits` to ensure it **returns a list of available subreddits** and handles errors correctly.
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch list of subreddits | Ensure list is returned correctly | - | Status `200 OK`, subreddits in list |
| 2 | Verify list content | Ensure subreddits match config | - | Subreddits match `Config.SUBREDDITS` |
| 3 | Missing config | Ensure error handling works | Remove `Config.SUBREDDITS` | Status `500 Internal Service Error` or equivalent |

#### TC-09 - Fetch List of Country-Based Subreddits
**Description**: Tests `/api/subreddits/countries` to ensure it **returns a list of country-based subreddits** and handles errors correctly.  
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch list of country-based subreddits | Ensure list is returned correctly | - | Status `200 OK`, subreddits in list |
| 2 | Verify list content | Ensure subreddits match config | - | Subreddits match `Config.COUNTRY_SUBREDDITS` |
| 3 | Missing config | Ensure error handling works | Remove `Config.COUNTRY_SUBREDDITS` | Status `500 Internal Service Error` or equivalent |
| 4 | Check login requirement | Ensure some subreddits require login | - | Each item has `login_required` field, 0 or 1 |

#### TC-10 - Fetch Topic Analysis Results
**Description**: Tests `/api/topics/latest/<subreddit>` to ensure it **returns the latest analysis results** and handles errors correctly.  
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch results for existing subreddit | Ensure results are returned correctly | Valid `subreddit` | Returns list with latest `timestamp` |
| 2 | Fetch for non-existent subreddit | Ensure error handling works | Invalid `subreddit` | Status `404 Not Found` |
| 3 | Verify content | Ensure data matches database | Valid `subreddit` | JSON contains expected fields (label, posts, subreddit, timestamp, etc.) |

#### TC-11 - Fetch Country-Based Analysis Results
**Description**: Tests `/api/countries/latest/<subreddit>` to ensure it **returns the latest results** and handles errors correctly.  
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch results for existing subreddit | Ensure results are returned correctly | Valid `subreddit` | Returns list with latest `timestamp` |
| 2 | Fetch for non-existent subreddit | Ensure error handling works | Invalid `subreddit` | Status `404 Not Found` |
| 3 | Verify content | Ensure data matches database | Valid `subreddit` | JSON contains expected fields (country, posts, requiresLogin, etc.) |

#### TC-12 - Fetch Post Statistics for Topic Analysis
**Description**: Tests `/api/statistics/<subreddit>/<days>` to ensure it **returns post counts** and handles errors correctly.  
**Priority**: Medium

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch stats for existing subreddit | Ensure stats are returned correctly | Valid `subreddit` | Returns stats as list |
| 2 | Fetch for non-existent subreddit | Ensure error handling works | Invalid `subreddit` | Status `404 Not Found` |
| 3 | Verify content | Ensure data structure is correct | Valid `subreddit` | JSON contains expected fields (_id, daily, total_posts) |

#### TC-13 - Fetch Topic Statistics for Topic Analysis
**Description**: Tests `/api/statistics/topics/<subreddit>/<days>/<limit>` to ensure it **returns top topic statistics** and handles errors correctly.  
**Priority**: Medium

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch stats for existing subreddit | Ensure stats are returned correctly | Valid `subreddit` | Returns stats as list |
| 2 | Fetch for non-existent subreddit | Ensure error handling works | Invalid `subreddit` | Status `404 Not Found` |
| 3 | Verify content | Ensure data structure is correct | Valid `subreddit` | JSON contains expected fields (_id, topics) |


Tests that still need to be planned:
- **User management (authentication)**, including registration, login, token refresh etc.
- **User-specific features (that require login)**, including subscription management


> Note: This test case plan was translated from Finnish to English using ChatGPT, and although it has been reviewed by the team, it may still contain minor inaccuracies.