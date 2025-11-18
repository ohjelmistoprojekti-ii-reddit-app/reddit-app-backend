# Test Plan

Contents:
- [Objective and Testing Scope](#objective-and-testing-scope)
- [Testing Approach](#testing-approach)
- [Testing Areas](#testing-areas)
- [Test Prioritization](#test-prioritization)
- [Test Environment](#test-environment)
- [Testing Criteria](#testing-criteria)
- [Testing Deliverables](#testing-deliverables)

## Objective and Testing Scope

The goal of the testing process is to ensure the **functionality and stability of key backend features** of Reddit Analyzer as the project is coming to an end. The testing also supports **quality assessment**, such as evaluating reliability, identifying potential issues, and highlighting the strengths and weaknesses of the implemented solutions.

The testing scope includes:
- **Database connections (MongoDB)** – CRUD operations  
- **REST API** – responses, error handling, and boundary conditions  
- **Token-based user management and authentication** – registration, login, and token validation  

Testing **does not cover** the analysis pipelines, as they run in a separate automated environment (*GitHub Actions*) and do not belong to the runtime environment of the backend. For the same reason, external services such as the Reddit API and analysis-related libraries (e.g., BERTopic) are excluded. However, GitHub Actions provides feedback through workflow logs, which can be used to identify issues in the analysis pipelines if needed.

Frontend testing is outside the scope of this plan, as it is handled by a different team member.

## Testing Approach

The testing follows the **"test first, refactor later"** principle: tests are first written for all major functionalities, even if they initially fail. The goal is to gain a clear understanding of the problematic areas. After that, the test results will guide the refactoring process. If this approach becomes too difficult or time-consuming, a more traditional approach —testing and refactoring simultaneously— may be used.

Since the project's requirement specification is incomplete and lacks explicit acceptance criteria, test design is primarily based on how the application’s functionalities are **expected** to behave. This aligns with the main goal of testing: ensuring the functionality and stability of the critical components. We will use a **white-box testing** strategy, meaning tests are designed by examining the structure and logic of the functions directly.

The testing tools include:
- **pytest** – for implementing unit and integration tests  
- **Allure Report** – for visualizing test results  
- **mongomock** – for simulating database operations without affecting the production database 

Unit tests verify individual functions and methods, while integration tests verify cooperation between components (e.g., REST API ↔ database).

## Testing Areas

### REST API and User Management

The REST API controls all key features of Reddit Analyzer, including trending topics analysis, country-specific subreddit analysis, subscription-based analysis, and user management. **Analyses are executed automatically via GitHub Actions**, and the API provides access to these results. The API also handles user and subscription management.

Below is an overview of the main functionalities and how they interact with the API:

- **Topic Analysis**:  
  A large set of Reddit posts is used to identify trending topics via topic modeling, followed by topic-level summarization (LLM) and sentiment analysis.  
  The API provides access to the subreddits that are analyzed and the results/statistics of those analyses.

- **Country-based Subreddit Analysis**:  
  A smaller set of posts per country-based subreddit is processed using translation (if needed) and sentiment analysis.  
  The API provides access to country-based subreddits and their analysis results.

- **User Management**:  
  Registration, login, and logout are handled through the API. Authentication uses access and refresh tokens. The access token authorizes API requests, and the refresh token can generate a new access token. Logout invalidates both tokens.

- **Subscription-based Analysis**:  
  A user can subscribe to analyses with a chosen subreddit and analysis type (*posts* or *topics*). Analyses for subscribed subreddits are then executed regularly via Actions.
  The API handles subscription creation, deactivation, and retrieval of the analysis results.

#### API Endpoints

| Feature | Endpoint | Method | Description |
|--------|----------|--------|-------------|
| Topic Analysis | `/api/subreddits` | GET | Returns subreddits that are analyzed regularly |
| Topic Analysis | `/api/topics/latest/<subreddit>` | GET | Returns the latest topic analysis results for a subreddit |
| Topic Analysis | `/api/statistics/<subreddit>/<days>` | GET | Returns statistics on post volumes for a selected timeframe |
| Topic Analysis | `/api/statistics/topics/<subreddit>/<days>/<limit>` | GET | Returns statistics on most frequent topics within a timeframe |
| Country Analysis | `/api/subreddits/countries` | GET | Returns country-based subreddits that are analyzed regularly |
| Country Analysis | `/api/countries/latest/<subreddit>` | GET | Returns the latest analysis results for a country-based subreddit |
| User Management | `/api/authentication/register` | POST | Creates a new user account |
| User Management | `/api/authentication/login` | POST | Authenticates user and returns access/refresh tokens |
| User Management | `/api/authentication/refresh` | POST | Exchanges a refresh token for a new access token |
| User Management | `/api/authentication/logout` | DELETE | Invalidates access and refresh tokens (logs out user) |
| User Management | `/api/authentication/delete` | DELETE | Deletes user account and its active subscriptions |
| Subscriptions | `/api/subscriptions/type/<type>` | GET | Retrieves active subscriptions by analysis type |
| Subscriptions | `/api/subscriptions/current-user` | GET | Retrieves subscriptions for the current user |
| Subscriptions | `/api/subscriptions/current-user/add/<subreddit>/<type>` | POST | Adds a new subscription for the current user |
| Subscriptions | `/api/subscriptions/current-user/deactivate` | PATCH | Deactivates the current user’s subscription |
| Subscriptions | `/api/subscriptions/current-user/latest-analyzed` | GET | Returns the latest analysis results for the user's subscription |

Two real-time data fetching endpoints are intentionally excluded from testing, as they are for demo purposes only.

A detailed description of all endpoints (with examples) is available in the backend documentation of Reddit Analyzer.

### Database

The Reddit Analyzer database is implemented using [MongoDB Atlas](https://www.mongodb.com/docs/atlas/). MongoDB is a NoSQL document database where data is stored in JSON-like documents and organized into *collections*. Schemas are flexible, allowing for easy adaptation to changing data requirements.

Reddit Analyzer database contains the following collections:

| Collection | Content |
|-----------|---------|
| `posts` | Contains topic and sentiment analysis results for selected subreddits. (The name is a bit misleading, **topics** would be more descriptive.) |
| `countries` | Contains analysis results for country-based subreddits, including translated posts (if needed) and sentiment scores. |
| `users` | Contains registered user accounts. |
| `subscriptions` | Contains user-created subreddit subscriptions including selected analysis type. |
| `subscription_data` | Contains analysis results produced from user subscriptions (topic-level or post-level depending on subscription type). |

Database access is managed through a dedicated database layer that handles saving, updating, and retrieving data.

The goal of this database description is to provide context for the database-related test cases. Please not that tests **do not use** the production database. Instead, a separate test database simulated with *mongomock* is used.

## Test Prioritization

Test cases and functionalities are prioritized **based on risk**, ensuring that the most critical parts are tested first.

Priority order for the functional areas:
1. **Database connections**
2. **REST API**
3. **User management and authentication**

Each **test case** also receives a criticality label (e.g., *high*, *medium*, *low*) depending on its importance to application stability.

Prioritization occurs on two levels:
1. **Area criticality** (database → REST API → user management)
2. **Test case criticality** (high → medium → low)

## Test Environment

Tests will be executed primarily in a **local** Python virtual environment. If time allows, test execution may be migrated to GitHub Actions for automated testing.

## Testing Criteria

- **Entry Criteria:** (conditions for starting testing)
  Required libraries and dependencies are installed, backend runs locally, and the test environment is set up.

- **Exit Criteria:** (conditions for completing testing)
  All unit and integration tests have been executed, and all critical tests pass. Any failed tests are documented and resolved.

- **Suspension Criteria:** (conditions for pausing testing)
  Testing may be paused if unexpected issues occur in the environment or if time or resource constraints prevent continuation.

## Testing Deliverables

Test results are compiled into **Allure Report** -report, which provides a visual summary of test execution, successes, and detected issues. This report supports test analysis and documentation.

Test cases are documented separately in the [Test Cases](./test_cases.md) file.

> Note: The test plan was translated from Finnish to English using ChatGPT, and although it has been reviewed by the team, it may still contain minor inaccuracies.