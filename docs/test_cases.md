# Test Cases

Test cases have been designed to cover the main functionalities of the Reddit Analyzer backend, focusing on database operations and REST API endpoints. Each test case includes a description, priority level, test steps, objectives, input parameters, and expected results.

Please refer to the [Test Plan](./test_plan.md) for an overview of the testing strategy and areas under test.

## Database Tests

Database tests will be unit tests. Our database contains diverse data, and no schemas or mandatory fields have been defined, so data integrity validation is not the focus. Instead, we will focus on verifying that database functions work as expected. We will create a test database using *mongomock*.

### TC-01 - Save Data to Database
**Description**: Tests the `save_data_to_database(data_to_save, collection)` function to ensure data is **saved correctly** and errors are handled appropriately.<br> 
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Save a single document | Ensure single document is saved correctly | Valid document | Document is added to the collection |
| 2 | Save a list of documents | Ensure multiple documents are saved correctly | List of valid documents | All documents are added to the collection |
| 3 | Save an empty document list | Ensure error handling works | Empty list | `ValueError` or equivalent |
| 4 | Save invalid data type | Ensure error handling works | Invalid type, e.g., string | `TypeError` or equivalent |


### TC-02 - Fetch Data from Database
**Description**: Tests the `fetch_data_from_collection(collection, filter=None)` function to ensure data **retrieval works correctly** and errors are handled appropriately.<br>
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch all documents | Ensure fetching all documents works normally | No `filter` | Returns all documents as a list |
| 2 | Fetch documents using filter | Ensure filtered fetch works correctly | Valid `filter` | Returns documents matching the filter |
| 3 | Fetch a non-existent document | Ensure fetch handles missing data correctly | Invalid `filter` | Returns empty list |
| 4 | Fetch documents with invalid filter type | Ensure error handling works | Invalid `filter` | `TypeError` |


### TC-03 - Update Document in Database
**Description**: Tests the `update_one_item_in_collection(collection, filter, update)` function to ensure data **is updated correctly** and errors are handled appropriately.<br>
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Update existing document | Ensure update succeeds | Valid `filter` and `update` | Document is updated successfully |
| 2 | Update non-existent document | Ensure error handling works | Invalid `filter` | `ValueError` or equivalent |
| 3 | Update with invalid filter | Ensure error handling works | Invalid `filter`, e.g., string | `TypeError` or equivalent |


### TC-04 - Delete Document from Database
**Description**: Tests the `delete_one_item_from_collection(collection, filter)` function to ensure data **is deleted correctly** and errors are handled appropriately.<br>
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Delete existing document | Ensure deletion succeeds | Valid `filter` | Document is deleted successfully (function returns 1) |
| 2 | Delete non-existent document | Ensure deleting non-existent document is handled gracefully | Invalid `filter` | Function returns 0 |
| 3 | Delete with invalid filter | Ensure error handling works | Invalid `filter`, e.g., string | `TypeError` or equivalent |

---

> **NOTE:**
> For the next tests involving analysis results, make sure to create a dataset that covers different types of analysis results and multiple timestamps. For clarity, analysis-related tests should be separated from basic CRUD tests.

### TC-05 - Fetch Latest Analysis Results From Database
**Description**: Tests `get_latest_data_by_subreddit(collection, subreddit, type=None)` to ensure it **returns the latest data correctly** and handles errors appropriately.<br>
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch latest data without `type` filter | Ensure latest documents are returned | Valid `subreddit` | Returns correct documents with latest timestamp |
| 2 | Fetch latest data with `type` filter | Ensure filtering by analysis type works | Valid `subreddit` and `type` | Returns correct documents with latest timestamp and correct type |
| 3 | Fetch latest data from non-existent subreddit | Ensure missing subreddit is handled correctly | Invalid `subreddit` | Returns empty list |
| 4 | Fetch latest data with invalid `type` parameter | Ensure error handling works | Invalid `type` (not `posts` or `topics`) | `ValueError` or equivalent |


### TC-06 - Calculate Post Number Statistics From Analysis Results
**Description**: Tests `get_post_numbers_by_timeperiod(subreddit, number_of_days)` to ensure it **calculates post counts correctly** and handles errors appropriately.<br>
**Priority**: Medium <br>
**Note**: Test data must include posts across multiple days so that the counting logic can be properly verified.

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Count post numbers for existing subreddit | Ensure counts are correct | Valid `subreddit` and `number_of_days` | Returns list of post counts with correct totals |
| 2 | Count post numbers for non-existent subreddit | Ensure missing subreddit is handled correctly | Invalid `subreddit` | Returns empty list |
| 3 | Count post numbers with invalid `number_of_days` | Ensure error handling works | Invalid `number_of_days`, e.g., negative | `ValueError` or equivalent |


### TC-07 - Calculate Top Topics Statistics From Analysis Results
**Description**: Tests `get_top_topics_by_timeperiod(subreddit, number_of_days, limit)` to ensure it **returns topics in correct order and counts** and handles errors appropriately.<br>
**Priority**: Medium  
**Note**: Test data must include posts across multiple days with various topics so that the ranking logic can be properly verified.

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Count top topics for existing subreddit | Ensure top topics are calculated correctly | Valid `subreddit`, `number_of_days`, `limit` | Returns list of top topics in order, topic amount = `limit` |
| 2 | Count top topics for non-existent subreddit | Ensure missing subreddit is handled correctly | Invalid `subreddit` | Returns empty list |
| 3 | Count top topics with large `limit` | Ensure function returns all available topics without error | Valid `subreddit`, large `limit` | Returns all top topics, count < `limit` |
| 4 | Count top topics with invalid `number_of_days` | Ensure error handling works | Invalid `number_of_days`, e.g. negative | `ValueError` or equivalent |
| 5 | Count top topics with invalid `limit` | Ensure error handling works | Invalid `limit`, e.g. negative | `ValueError` or equivalent |



## REST API and User Management Tests

REST API tests follow the priority order defined in the test plan. First, we will test public endpoints that are always accessible, then user management (login/register etc.), and lastly authenticated actions that require login.

*All endpoints and their details are listed in the test plan (see docs-folder)*

### Public endpoints (no authentication required)

### TC-08 - Fetch Subreddits Used in Analyses
**Description**: Tests `/api/subreddits` and `/api/subreddits/countries` to ensure they **return subreddits correctly**. As the lists are static, no error handling tests are needed.<br>
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch list of subreddits | Ensure list is returned correctly | - | Status `200 OK`, correct subreddits in list |
| 2 | Fetch list of country-based subreddits | Ensure list is returned correctly | - | Status `200 OK`, correct country-based subreddits in list |
| 3 | Check country subreddit login requirement | Ensure some subreddits require login | - | Each item has `login_required` field, 0 or 1 |

### TC-09 - Fetch Topic Analysis Results
**Description**: Tests `/api/topics/latest/<subreddit>` to ensure it **returns the latest analysis results** and handles errors correctly.<br>
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch results for existing subreddit | Ensure results are returned correctly | Valid `subreddit` | Returns list with latest `timestamp` |
| 2 | Fetch for non-existent subreddit | Ensure error handling works | Invalid `subreddit` | Status `404 Not Found` |
| 3 | Verify response content | Ensure data matches database | Valid `subreddit` | JSON contains expected fields |

### TC-10 - Fetch Country-Based Analysis Results
**Description**: Tests `/api/countries/latest/<subreddit>` to ensure it **returns the latest results** and handles errors correctly.<br>
**Priority**: High<br>
**Note**: Some country subreddits require user authentication. These tests cover unauthenticated access. The rest are in the **user-specific** endpoints section.

**No authentication tests:**
| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch results for existing subreddit that does not require login | Ensure results are returned correctly | Valid `subreddit` | Returns list with latest `timestamp` |
| 2 | Fetch for non-existent subreddit | Ensure error handling works | Invalid `subreddit` | Status `404 Not Found` |
| 3 | Verify response content | Ensure data matches database | Valid `subreddit` | JSON contains expected fields |

### TC-11 - Fetch Post Statistics for Topic Analysis
**Description**: Tests `/api/statistics/<subreddit>/<days>` to ensure it **returns post counts** and handles errors correctly.<br>
**Priority**: Medium

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch stats for existing subreddit | Ensure stats are returned correctly | Valid `subreddit` | Returns stats as list |
| 2 | Fetch stats for non-existent subreddit | Ensure error handling works | Invalid `subreddit` | Status `404 Not Found` |
| 3 | Verify response content | Ensure data structure is correct | Valid `subreddit` | JSON contains expected fields |

### TC-12 - Fetch Topic Statistics for Topic Analysis
**Description**: Tests `/api/statistics/topics/<subreddit>/<days>/<limit>` to ensure it **returns top topic statistics** and handles errors correctly.<br>
**Priority**: Medium

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch stats for existing subreddit | Ensure stats are returned correctly | Valid `subreddit` | Returns stats as list |
| 2 | Fetch stats for non-existent subreddit | Ensure error handling works | Invalid `subreddit` | Status `404 Not Found` |
| 3 | Verify response content | Ensure data structure is correct | Valid `subreddit` | JSON contains expected field |


### User authentication endpoints

### TC-13 - Register New User
**Description**: Tests `/api/authentication/register` to ensure **user registration works correctly** and errors are handled appropriately.<br>
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|-----------|-----------------|----------------|
| 1 | Register with valid data | Ensure registration succeeds | Valid username, email, password | Status `201 Created`, token returned |
| 2 | Register with existing username | Ensure duplicate username is handled | Existing username, valid email, password | Status `400 Bad Request`, error message |
| 3 | Register with existing email | Ensure duplicate email is handled | Valid username, existing email, password | Status `400 Bad Request`, error message |
| 4 | Register with invalid data | Ensure validation works | Invalid email format, short password | Status `400 Bad Request`, error message |
| 5 | Register with missing user information | Ensure validation works | Missing required information, e.g., email | Status `400 Bad Request`|

### TC-14 - Login as User
**Description**: Tests `/api/authentication/login` to ensure **user login works correctly** and errors are handled appropriately.<br>
**Priority**: High

| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|-----------|-----------------|----------------|
| 1 | Login with valid credentials | Ensure login succeeds | Valid username/email and password | Status `200 OK`, token returned |
| 2 | Login with invalid password | Ensure error handling works | Valid username/email and invalid password | Status `401 Unauthorized`, error message |
| 3 | Login with non-existent user | Ensure error handling works | Invalid username/email and password | Status `401 Unauthorized`, error message |


### Planned tests (not yet implemented)

#### User-specific endpoints (require authentication)

#### TC-10 - Fetch Country-Based Analysis Results
**Description**: Tests `/api/countries/latest/<subreddit>` to ensure it **returns the latest results** and handles errors correctly.<br>
**Priority**: High<br>
**Note**: Some country subreddits require user authentication. These tests cover authenticated access. The other tests are in the **public endpoints** section.

**Authenticated tests:**
| # | Test Step | Objective | Input/Parameter | Expected Result |
|---|-----------|----------|-----------------|----------------|
| 1 | Fetch results for existing subreddit that requires login | Ensure results are returned correctly | Valid `subreddit`, authenticated user | Returns list with latest `timestamp` |
| 2 | Fetch results for existing subreddit that requires login, but without authentication | Ensure access is denied or error is returned | Valid `subreddit`, unauthenticated user | Status `401 Unauthorized` or appropriate error |

Still to be planned:
- **User management (authentication)**, including token refresh, user logout
- **User-specific features (that require login)**, including subscription management


> Note: This test case plan was translated from Finnish to English using ChatGPT, and although it has been reviewed by the team, it may still contain minor inaccuracies.