# Reddit Trend Analyzer

This is the **backend service** for a web application that:
- fetches **popular Reddit posts**
- identifies **trending topics** using topic modeling
- analyzes **sentiment** of public discussions
- and enables **filtering** topics by sentiment (positive, negative, neutral) and category (e.g., technology, entertainment, sports)

<details open>
<summary><strong>Table of Contents</strong></summary>

- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Getting Started](#-getting-started)
  - [Development Setup](#development-setup)
  - [Connecting to Reddit API (Async PRAW)](#connecting-to-reddit-api-async-praw)
  - [Connecting to MongoDb Atlas](#connecting-to-mongodb-atlas)
  - [Run the demo](#run-the-demo)
- [🌐 REST API](#-rest-api)
  - [Get analyzed posts from Reddit (no database)](#get-analyzed-posts-from-reddit-no-database)
  - [Get latest analyzed posts from the database](#get-latest-analyzed-posts-from-the-database)
  - [Get post number statistics from the database](#get-post-number-statistics-for-a-subreddit-in-a-given-timeperiod)
  - [Get top topics statistics from the database](#get-top-topics-statistics-for-a-subreddit-in-a-given-timeperiod)
  - [Get analyzed example comments on hot topics](#get-analyzed-example-comments-on-hot-topics)
- [🔎 Solutions Overview](#-solutions-overview)
- [➡️ See Also](#see-also)

</details>
<br>

> This project was created as part of the Software Development Project II course at Haaga-Helia University of Applied Sciences, Finland. It is not affiliated with or endorsed by Reddit.

## 🛠️ Tech Stack
- **Language:** [Python](https://docs.python.org/3/)
- **Framework:** [Flask](https://flask.palletsprojects.com/en/stable/)
- **Reddit API:** [Async PRAW](https://asyncpraw.readthedocs.io/en/stable/)
- **Topic modeling:** [BERTopic](https://maartengr.github.io/BERTopic/index.html)
- **Sentiment analysis:** [VADER](https://vadersentiment.readthedocs.io/en/latest/index.html)
- **Database:** [MongoDB](https://www.mongodb.com/)

<p align="right"><a href="#reddit-trend-analyzer">Back to top 🔼</a></p>

## 🚀 Getting Started

### Development Setup
- Clone the repository:
```bash
git clone https://github.com/ohjelmistoprojekti-ii-reddit-app/reddit-app-backend.git
```
- Create Virtual Environment for the project in the project folder with command:
```bash
python -m venv venv
```
- Activate the Virtual Environment (this has to be done every time you open new terminal):
```bash
venv\Scripts\activate
```
- Install requirements to get started:
```bash
pip install -r requirements.txt
```
- Add MongoDb Atlas server:
```bash
python -m pip install "pymongo[srv]"
```

### Connecting to Reddit API (Async PRAW)
Assuming you have already registered an app to Reddit's developer portal:
- Create **.env** file in the root of the project
- Add your Reddit app credentials to the file:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

### Connecting to MongoDb Atlas
First log in to MongoDb Atlas and get your peronal connection string:
- Add your connection string to your **.env** file
```
ATLAS_CONNECTION_STR=your_connection_string
```

### Run the demo

View example Reddit analysis results by running the script:
```bash
python demo.py
```

The results will be printed in your terminal.

💡 You can change the subreddit, type of posts and number of posts in `demo.py` to experiment with different data.

<p align="right"><a href="#reddit-trend-analyzer">Back to top 🔼</a></p>

## 🌐 REST API

Start the Flask server by running:
```bash
python run.py
```

✅ When everything is working, you will see this message on your console: 'Running on http://127.0.0.1:5000'

### Get analyzed posts from Reddit (no database)

> GET /posts/{subreddit}/{type}/{amount}

**Description**: Fetches posts directly from Reddit, performs topic modeling and sentiment analysis, and returns analyzed data. Data is not stored in the database.

⌛ This operation may take a few minutes depending on the amount of posts.

| Parameter | Description | Examples |
| --------- | ----------- | ------- |
| subreddit | [name of any subreddit](https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits/) | `all`, `music`, `technology` |
| type | type of posts | `hot`, `rising`, `new` |
| amount | amount of posts | `500`, `1000` |

**Example request**:
```
http://127.0.0.1:5000/posts/technology/hot/500
```

➡️ **Returns** 10 most popular topics from the subreddit along with sample posts and sentiment analysis results.

<details>
<summary><strong>Example response format</strong> (click to open)</summary>

Note that the order of fields may vary.
```jsonc
{
  "topic_id": 3, // Indicates the rank of the topic, starting from 0 which is the most popular topic
  "topic": ["AI", "Innovation", "Gadgets"], // Keywords representing the topic
  "num_posts": 22, // Number of posts in this topic
  "posts": [ // Example posts with comments
    {
      "id": "abc123",
      "subreddit": "technology",
      "title": "AI model achieves new benchmark",
      "content": "A new AI model has set a record for image recognition accuracy.",
      "comments": [
        "This is amazing!",
        "Impressive results, can't wait to see it in action."
      ],
      "num_comments": 2,
      "score": 150,
      "upvote_ratio": 0.97
    },
    {
      "id": "def456",
      "subreddit": "technology",
      "title": "Tech company launches innovative gadget",
      "content": "The latest gadget has several cutting-edge features.",
      "comments": [
        "Looks promising!"
      ],
      "num_comments": 1,
      "score": 120,
      "upvote_ratio": 0.95
    }
  ],
  "sentiment_values": { // Sentiment analysis results
    "average_compound": 0.25,
    "average_neg": 10.0,
    "average_neu": 75.0,
    "average_pos": 15.0,
    "comment_count": 50
  },
}
```
</details>


### Get latest analyzed posts from the database

> GET /posts/latest/{subreddit}

**Description**: Retrieves the latest analyzed posts for a given subreddit from the database. Similar to the `/posts/{subreddit}/{type}/{amount}` method, but fetches data from the database instead of Reddit.

ℹ️ Our `GitHub Actions` pipeline automatically fetches, analyzes, and stores Reddit data once a day for a **predefined** set of subreddits (see table below).

⚙️ For testing purposes, you can also run the data pipeline manually to populate your database. To do this, ensure your `.env` file is set up with Reddit API and MongoDB Atlas credentials, then run the following command in your terminal:
```
python -m scripts.pipeline
```

| Parameter | Description | Options |
| --------- | ----------- | ------- |
| subreddit | name of subreddit from the predefined options | `worldnews`, `technology`, `entertainment`, `movies`, `gaming`, `sports`, `travel`, `jobs`, `futurology`, `programming`

**Example request**:
```
http://127.0.0.1:5000/posts/latest/technology
```

➡️ **Returns** 10 most popular topics, along with sample posts and sentiment analysis results, from the most recently saved batch in the database.

<details>
<summary><strong>Example response format</strong> (click to open)</summary>

Note that the order of fields may vary.

```jsonc
{
  "_id": "64a7f8e2b4c79e6f8c9d4e1a", // MongoDB document ID
  "topic_id": 3, // Indicates the rank of the topic, starting from 0 which is the most popular topic
  "topic": ["AI", "Innovation", "Gadgets"], // Keywords representing the topic
  "subreddit": "technology",
  "num_posts": 22, // Number of posts in this topic
  "posts": [ // Example posts with comments
    {
      "id": "abc123",
      "subreddit": "technology",
      "title": "AI model achieves new benchmark",
      "content": "A new AI model has set a record for image recognition accuracy.",
      "comments": [
        "This is amazing!",
        "Impressive results, can't wait to see it in action."
      ],
      "num_comments": 2,
      "score": 150,
      "upvote_ratio": 0.97
    },
    {
      "id": "def456",
      "subreddit": "technology",
      "title": "Tech company launches innovative gadget",
      "content": "The latest gadget has several cutting-edge features.",
      "comments": [
        "Looks promising!"
      ],
      "num_comments": 1,
      "score": 120,
      "upvote_ratio": 0.95
    }
  ],
  "sentiment_values": { // Sentiment analysis results
    "average_compound": 0.25,
    "average_neg": 10.0,
    "average_neu": 75.0,
    "average_pos": 15.0,
    "comment_count": 50
  },
  "timestamp": "2025-07-05T12:34:56.789Z", // Time when the data was saved to db
}
```
</details>

### Get post number statistics for a subreddit in a given timeperiod

> GET /posts/numbers/{subreddit}/{days}

**Description**: Retrieves daily and total post number statistics for one subreddit over a desired time period.

ℹ️ This endpoint supports a post number trend chart for a selected subreddit.

| Parameter | Description | Variable|
| --------- | ----------- | ------- |
| subreddit | name of subreddit from the predefined options | `worldnews`, `technology`, `entertainment`, `movies`, `gaming`, `sports`, `travel`, `jobs`, `futurology`, `programming` |
| days | Last amount of days | int |

**Example request**:
```
http://127.0.0.1:5000/posts/numbers/programming/7
```

➡️ **Returns** The subreddit and daily post numbers for the timestamps included in the provided time period.

<details>
<summary><strong>Example response format</strong> (click to open)</summary>

```json
{
    "_id:": "programming",
    "daily": [
      {"day": "2025-09-26", "posts":244},
      {"day":"2025-09-27", "posts":199},
      {"day":"2025-09-28", "posts":191},
      {"day":"2025-09-29", "posts":183},
      {"day":"2025-09-30", "posts":180},
      {"day":"2025-10-01", "posts":231},
      {"day":"2025-10-02", "posts":175}
    ],
    "total_posts": 1403
}
```
</details>

### Get top topics statistics for a subreddit in a given timeperiod

> GET /posts/numbers/topics/{subreddit}/{days}/{limit}

**Description**: Retrieves the most frequent topics and their count for one subreddit over a desired time period.

ℹ️ This endpoint supports a topic topics trend chart for a selected subreddit.

| Parameter | Description | Variable|
| --------- | ----------- | ------- |
| subreddit | name of subreddit from the predefined options | `worldnews`, `technology`, `entertainment`, `movies`, `gaming`, `sports`, `travel`, `jobs`, `futurology`, `programming` |
| days | Last amount of days | int |
| limit | The length of the top topics list to be displayed | int |

**Example request**:
```
http://127.0.0.1:5000/posts/numbers/topics/programming/7/8
```

➡️ **Returns** The subreddit and the most frequent topics and their count in the provided time period.

<details>
<summary><strong>Example response format</strong> (click to open)</summary>

```json
{
    "_id:": "programming",
    "topics": [
      {"count": 7, "topic": "python"},
      {"count": 7, "topic": "database"},
      {"count": 6, "topic": "postgresql"},
      {"count": 6, "topic": "postgres"},
      {"count": 6, "topic": "ai"},
      {"count": 6, "topic": "java"},
      {"count": 5, "topic": "threads"},
      {"count": 5, "topic": "rust"}
    ]
}
```
</details>

### Get analyzed example comments on hot topics

> GET /posts/hot/{subreddit}

**Description**: Fetches 10 hot posts directly from Reddit. For each post, selects one comment, translates it into English, performs sentiment analysis, and returns the analyzed data. The data is not stored in the database.

ℹ️ This endpoint supports the map feature on the front end. We use it primarily to fetch country-specific subreddits, but it can also be used to retrieve data about subreddits with supported languages.


| Parameter | Description | Examples |
| --------- | ----------- | ------- |
| subreddit | [name of any subreddit](https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits/) | `suomi`, `sweden`, `spain`, `mexico`, `italia`

**Example request**:
```
http://127.0.0.1:5000/posts/hot/italia
```
➡️ **Returns** For each current post that contains at least one comment, returns an example comment along with its sentiment analysis result. Posts without comments are excluded.

<details>
<summary><strong>Example response format</strong> (click to open)</summary>

```json
{
    "comment_eng": "thanks to all for support, I didn't feel like ahaha and I learned about the challenge",
    "comment_original": "grazie di cuore a tutti per il supporto, non me lo aspettavo ahaha e scusatemi per lo sfogo",
    "post_score": 480,
    "post_title": "Ho 23 anni e NON vivo",
    "sentiment_values": {
      "sentiment_compound": 0.585,
      "sentiment_neg": 0.111,
      "sentiment_neu": 0.526,
      "sentiment_pos": 0.363
    }
  },
  {
    "comment_eng": "With this opposition, I have spent ten years in government.",
    "comment_original": "Con questa opposizione fa tranquillissimamente dieci anni al governo",
    "post_score": 355,
    "post_title": "Zitta zitta la Meloni a fine mese arriva sul podio",
    "sentiment_values": {
      "sentiment_compound": 0,
      "sentiment_neg": 0,
      "sentiment_neu": 1,
      "sentiment_pos": 0
    }
  },
  {
    "comment_eng": "Is the minimum wage at 9 euros?",
    "comment_original": "Maa il salario minimo a 9 euro? Helloo? ",
    "post_score": 202,
    "post_title": "Se Flotilla sarà attaccata i sindacati sono pronti allo SCIOPERO GENERALE immediato",
    "sentiment_values": {
      "sentiment_compound": 0,
      "sentiment_neg": 0,
      "sentiment_neu": 1,
      "sentiment_pos": 0
    }
  }
```
</details>

<p align="right"><a href="#reddit-trend-analyzer">Back to top 🔼</a></p>

## 🔎 Solutions Overview
An overview of our solutions and approaches across the project's key areas.

<details>
<summary><strong>Topic Modeling</strong></summary>

**Topic modeling** is a natural language processing (NLP) technique for identifying themes and topics from text data.

There are multiple tools available for this task, and for this project, we chose **BERTopic**, a modern framework that leverages advanced sentence-transformer models and statistical techniques to uncover easily interpretable topics.

<strong>Core concepts of BERTopic</strong>

BERTopic is highly flexible, allowing you to customize or swap components based on your needs. For example, you can control how broad or detailed the topic groups are by changing the clustering model, or generate embeddings using almost any sentence-transformer model. Adjusting different components can have a significant impact on the results.

Here are the key steps in BERTopic and the models we used for each stage:

1. **Embedding**: Converts text into numerical vectors that capture meaning, so similar words are close in vector space. For example, words “*movie*” and “*film*” might end up near each other because they mean similar things.
    - Model: [all-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2)
2. **Dimensionality reduction**: Reduces the high-dimensional vectors, making patterns and clusters easier to detect.
    - Model: [UMAP](https://umap-learn.readthedocs.io/en/latest/)
3. **Clustering**: Groups similar embeddings into coherent topic clusters.
    - Model: [HDBSCAN](https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html)
4. **Topic representation**: Labels each cluster with a few key words summarizing its main theme.
    - Model: BERTopic default, [c-TF-IDF](https://maartengr.github.io/BERTopic/getting_started/ctfidf/ctfidf.html)


<strong>Why use BERTopic on Reddit data?</strong>

Reddit discussions are already organized into different topics as **subreddits**, so someone might wonder why we would use topic modeling on Reddit at all. We wanted to take our Reddit analysis a step further and see if recurring themes or topics could be found *within* large subreddits.

Reddit discussions are diverse, informal and full of slang and memes, making the data challenging to analyze. BERTopic uses contextual embeddings to capture the meaning behind words, allowing it to understand nuances that traditional models like LDA often miss. We believe this makes it well-suited for extracting meaningful topics from a large and messy dataset like Reddit.

**Learn more on this topic**:
- [What is Topic Modeling? An Introduction With Examples](https://www.datacamp.com/tutorial/what-is-topic-modeling) by Kurtis Pykes (Datacamp)
- [Advanced Topic Modeling with BERTopic](https://www.pinecone.io/learn/bertopic/) by James Briggs (Pinecone)
- [BERTopic official documentation](https://maartengr.github.io/BERTopic/algorithm/algorithm.html)
</details>

<details>
<summary><strong>Sentiment Analysis</strong></summary>

**Sentiment analysis** is a subfield of Natural Language Processing (NLP) that focuses on determining the **emotional tone or attitude** expressed in a piece of text.

In this project, we use sentiment analysis to determine the emotional tone of **Reddit posts and comments**. We chose to begin the analysis with **VADER** (Valence Aware Dictionary and sEntiment Reasoner), as it is specifically developed for analyzing **short, informal, and social media-style text**. The choice of VADER was also guided by its **high processing speed** and **low computational requirements**, which make it well-suited for efficiently analyzing large volumes of user-generated content.

---

## More about VADER's operating logic

Unlike machine learning–based models, VADER does **not learn from data**. Instead, it uses:

- A **predefined sentiment lexicon** (i.e., a list of words with known sentiment scores)  
- **Syntactic rules** to adjust sentiment based on context clues such as:
  - Capitalization (e.g., `"LOVE this"`)
  - Negations (e.g., `"not good"`)
  - Emojis and informal language

For each piece of text, VADER outputs four sentiment scores:

- **Positive** (`pos`)
- **Negative** (`neg`)
- **Neutral** (`neu`)
- **Compound** — a normalized score ranging from –1 (most negative) to +1 (most positive)

> ⚠️ Because VADER is a **lexicon-based tool**, it does **not understand deeper context** such as **sarcasm**, **irony**, or **ambiguous phrasing**.

---

## 🔧 Use of VADER in This Project

This project utilizes VADER to perform sentiment analysis on **user-generated content**, such as:

- Reddit comments under popular or trending posts

### Topic-Based Aggregated Sentiment

For a set of current or trending topics — each containing multiple posts and comments — the system:

- Analyzes the **sentiment of each comment** using VADER  
- Computes **average sentiment values** for each topic  
- Returns a **summary of sentiment scores** across all analyzed topics

We use typical threshold values to determine sentiments:

- **Positive sentiment**: `compound` ≥ **0.05**
- **Neutral sentiment**: `–0.05` < `compound` < **0.05**
- **Negative sentiment**: `compound` ≤ **–0.05**

</details>

<details>
<summary><strong>Automated Data Processing</strong></summary>

We use **GitHub Actions** to automatically fetch, analyze, and store Reddit data once per day. The pipeline currently only runs for a predefined set of subreddits (see table below).

**How it works**
- Runs daily at midnight (UTC) or on demand via manual trigger
- Fetches ~500 hot posts and up to 8 comments per subreddit
- Processes content with topic modeling and sentiment analysis
- Stores processed data in MongoDB Atlas

The processed data can be accessed via the `/posts/latest/{subreddit}` endpoint (see [REST documentation](#-rest-api)).

**Subreddits**

The pipeline processes a predefined set of active subreddits to ensure diverse and relevant content for our users:

| Subreddit    | Description                      |
|--------------|----------------------------------|
| worldnews    | International news               |
| technology   | Tech news and discussions        |
| entertainment| Entertainment & pop culture      |
| movies       | Movie news, reviews & discussions|
| gaming       | Game news, reviews & discussions |
| sports       | Sports news and updates          |
| travel       | Travel tips and stories          |
| jobs         | Careers and job postings         |
| futurology   | Future tech and trends           |
| programming  | Programming discussions          |

⚙️ The subreddit list can be modified in `scripts/pipeline.py`

💡 We use the data for category filtering in the frontend. We are planning to add historical analysis and trend tracking soon.

**Benefits**

- Ensures consistent and reliable daily updates
- Keeps the frontend up-to-date with fresh data
- Enables historical analysis and long-term trend tracking
- Delivers fast frontend performance without waiting for real-time processing

**Learn more**
- [GitHub Actions documentation](https://docs.github.com/en/actions)
</details>

<p align="right"><a href="#reddit-trend-analyzer">Back to top 🔼</a></p>

## See Also

🖼️ [Frontend repository](https://github.com/ohjelmistoprojekti-ii-reddit-app/reddit-app-frontend) | 👥 [Organization page](https://github.com/ohjelmistoprojekti-ii-reddit-app/)

> Note: ChatGPT helped phrase parts of this README.
