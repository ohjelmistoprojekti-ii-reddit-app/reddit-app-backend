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
  - [Trending topics analysis endpoints](#trending-topics-analysis-endpoints)
  - [Statistics endpoints](#statistics-endpoints)
  - [Country subreddit analysis endpoints](#country-subreddit-analysis-endpoints)
  - [Subscriptions endpoints](#subscriptions-endpoints)
  - [No database endpoints](#no-database-endpoints)
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

**Available endpoints:**
- [No database endpoints](#no-database-endpoints)
  - [Get analyzed posts from Reddit (no database)](#get-analyzed-posts-from-reddit-no-database)
  - [Get translated and analyzed posts from Reddit (no database)](#get-translated-and-analyzed-posts-from-reddit-no-database)
- [Trending topics analysis endpoints](#trending-topics-analysis-endpoints)
  - [Get subreddits that have data available in the database](#get-subreddits-that-have-data-available-in-the-database)
  - [Get latest analyzed posts from the database](#get-latest-analyzed-posts-from-the-database)
- [Statistics endpoints](#statistics-endpoints)
  - [Get post number statistics for a subreddit in a given timeperiod](#get-post-number-statistics-for-a-subreddit-in-a-given-timeperiod)
  - [Get top topics statistics for a subreddit in a given timeperiod](#get-top-topics-statistics-for-a-subreddit-in-a-given-timeperiod)
- [Country subreddit analysis endpoints](#country-subreddit-analysis-endpoints)
  - [Get country subreddits that have data available in the database](#get-country-subreddits-that-have-data-available-in-the-database)
  - [Get latest analyzed country subreddit data from the database](#get-latest-analyzed-country-data-from-the-database)
- [Subscriptions endpoints](#subscriptions-endpoints)
  - [Get list of active subscriptions by analysis type](#get-list-of-active-subscriptions-by-analysis-type)
  - [Get subscriptions for current user](#get-subscription-for-current-user)
  - [Add new subscription for current user](#add-new-subscriptions-for-current-user)
  - [Deactivate subscription for current user](#deactivate-subscription-for-current-user)
  - [Get latest analyzed data for current user's active subscription](#get-latest-analyzed-data-for-current-users-active-subscription)


## No database endpoints

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
  "topic": ["AI", "Innovation", "Gadgets", "..."], // Keywords representing the topic
  "label": "AI Innovation Gadgets", // Official topic label
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

### Get translated and analyzed posts from Reddit (no database)

> GET /posts/hot/{subreddit}

**Description**: Fetches 10 hot posts directly from Reddit, translates their title, content and comments into English, performs sentiment analysis on the comments, and returns the analyzed data. The data is not stored in the database.

ℹ️ This endpoint supports the map feature on the front end. We use it primarily to fetch country-specific subreddits, but it can also be used to retrieve data about any subreddit with supported language.


| Parameter | Description | Examples |
| --------- | ----------- | ------- |
| subreddit | [name of any subreddit](https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits/) | `suomi`, `sweden`, `spain`, `mexico`, `italia`

**Example request**:
```
http://127.0.0.1:5000/posts/hot/italia
```
➡️ **Returns** Posts with original and translated content, including sentiment analysis on comments.

<details>
<summary><strong>Example response format</strong> (click to open)</summary>

```json
[
  {
    "comments": [
      "Immagino sia successo a [Firenze](https://www.ilgiornale.it/news/cronaca-locale/vandalismo-pro-pal-firenze-blocchi-cemento-sui-binari-2546511.html), cerchiamo di mettere le fonti, thanks.",
      "Attaccato da chi? Questo è un gesto molto pericoloso e non ha nessun senso e non c’entra niente con le manifestazioni pacifiche che ci sono state in questi giorni. Se davvero l’hanno fatto dei manifestanti vanno fermati.\nFortunatamente con tutte le telecamere di sicurezza di una stazione ferroviaria sarà facilissimo risalire ai responsabili, per caso il tuo amico ti ha detto dove è successo? Vedo che è notte quindi immagino tra ieri e oggi",
      "“manifestanti”.."
    ],
    "comments_eng": [
      "The image has been successfully re-created in [French] ( we are asking for the fonts, thanks.",
      "Accused of who? This is a very dangerous move and there is no sense and there is no sense in the peaceful demonstrations that we are experiencing in these days. If they really did make the manifestos. Unfortunately, with all the security cameras at a railway station, it will be easy to get to the responsible, if your friend has told you where it happened? I see that I am now comparing yesterday and today.",
      "This language is so far unsupported"
    ],
    "content": "So che verrò attaccato da molti, ma dopo questa ennesima bravata inizio a convincermi sempre di più che qui la situazione sta sfuggendo di mano a tutti. Volete manifestare? Bene, avete tutto il diritto di farlo, ma fatelo usando la testa e pensando alle conseguenze di ciò che fate. Proprio ieri avevo letto un post di un utente che raccontava che sua nonna è rimasta bloccata nel traffico per ore quando doveva andare a fare il suo ciclo di chemio… Una cosa a mio parere molto grave. Ieri sera ricevo questo video da un mio amico che lavora come macchinista. Questo gesto non è un gesto di protesta ma un vero e proprio attentato. Se un treno in corsa passava su quei blocchi c’era un alta possibilità che deragliasse… Risultato? Feriti e possibili morti di innocenti che stavano viaggiando su un semplice treno.",
    "content_eng": "So he would be beaten by many, but after this latest bravery he started to convince me constantly that the situation is worse than here. Volete manifestare? Well, you have all the directions to do it, but you kill it using the test and thinking about the consequences of what you kill. Yesterday I had a post on a poet who told me that his wife was stranded in traffic for hours when she needed to take her chemotherapy... A thing that makes me feel very bad. I'll be taking this video from a friend who works as a mechanic. This gesture is not a protest gesture but a real and committed one. If a train was in the path on those blocks there was a high possibility of crashing... result? Feriti and possible deaths of innocents traveling on a simple train.",
    "score": 579,
    "sentiment_values": {
      "average_compound": 0.242,
      "average_neg": 17.133,
      "average_neu": 66.767,
      "average_pos": 16.1
    },
    "title": "Manifestanti cercano di bloccare il traffico ferroviario mettendo blocchi di cemento sui binari",
    "title_eng": "Manifestos are trying to block traffic by putting cement blocks on the bridges."
  }
]
  
```
</details>


## Trending topics analysis endpoints

### Get subreddits that have data available in the database
> GET /subreddits

**Description**: Retrieves list of subreddits that our `GitHub Actions` pipeline currently analyzes regularly. The analyzed data is stored in the database and can be accessed via `/posts/latest/{subreddit}` endpoint.

**Example request**:
```
http://127.0.0.1:5000/subreddits
```

➡️ **Returns** list of subreddits that have data available in the database.

<details>
<summary><strong>Example response format</strong> (click to open)</summary>

```json
[
  "worldnews",
  "technology",
  "entertainment",
  "sports",
  "science",
  "programming"
]
```
</details>

### Get latest analyzed posts from the database

> GET /posts/latest/{subreddit}

**Description**: Retrieves the latest analyzed data for a given subreddit from the database. The analysis process for these subreddits includes topic modeling and sentiment analysis on comments.

ℹ️ Our `GitHub Actions` pipeline automatically fetches, analyzes, and stores Reddit data once a day for a **predefined** set of subreddits. To learn more about the automated pipeline, see the [Solutions Overview](#-solutions-overview) section.

| Parameter | Description | Examples | All options |
| --------- | ----------- | -------- | ----------- |
| subreddit | name of subreddit from the predefined options | `worldnews`, `technology`, `entertainment` | [Get all available subreddits](#get-subreddits-that-have-data-available-in-the-database) |

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
  "topic": ["AI", "Innovation", "Gadgets", "..."], // Keywords representing the topic
  "label": "AI Innovation Gadgets", // Official topic label
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

## Statistics endpoints

### Get post number statistics for a subreddit in a given timeperiod

> GET /posts/numbers/{subreddit}/{days}

**Description**: Retrieves daily and total post number statistics for one subreddit over a desired time period.

ℹ️ This endpoint supports a post number trend chart for a selected subreddit.

| Parameter | Description | Variable|
| --------- | ----------- | ------- |
| subreddit | name of subreddit from the predefined options | `worldnews`, `technology`, `entertainment`, `science`, `programming` |
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
| subreddit | name of subreddit from the predefined options | `worldnews`, `technology`, `entertainment`, `science`, `programming` |
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


## Country subreddit analysis endpoints

### Get country subreddits that have data available in the database
> GET /subreddits/countries

**Description**: Retrieves list of country subreddits that our `GitHub Actions` pipeline currently analyzes daily. The analyzed data is stored in the database and can be accessed via `/countries/latest/{subreddit}` endpoint.

**Example request**:
```
http://127.0.0.1:5000/subreddits/countries
```

➡️ **Returns** list of country subreddits that have data available in the database.

<details>
<summary><strong>Example response format</strong> (click to open)</summary>

```json
[
  {
    "id": "FI",
    "name": "Finland",
    "subreddit": "suomi"
  },
  {
    "id": "SE",
    "name": "Sweden",
    "subreddit": "sweden"
  },
  {
    "id": "IT",
    "name": "Italy",
    "subreddit": "italia"
  },
  {
    "id": "MX",
    "name": "Mexico",
    "subreddit": "mexico"
  },
  {
    "id": "ES",
    "name": "Spain",
    "subreddit": "spain"
  },
]
```
</details>

### Get latest analyzed country data from the database
> GET /countries/latest/{subreddit}

**Description**: Retrieves the latest analyzed posts for a given country subreddit from the database. The analysis process for country subreddits includes translation to English (if needed), and sentiment analysis on comments.

ℹ️ Our `GitHub Actions` pipeline automatically fetches, translates, analyzes, and stores country subreddit data every day for a **predefined** set of country subreddits. To read more about the automated pipeline, see the [Solutions Overview](#-solutions-overview) section.

| Parameter | Description | Examples | All options |
| --------- | ----------- | -------- | ----------- |
| subreddit | name of country subreddit from the predefined options | `suomi`, `sweden`, `italia`, `mexico`, `spain` | [Get all available country subreddits](#get-country-subreddits-that-have-data-available-in-the-database) |

**Example request**:
```
http://127.0.0.1:5000/countries/latest/italia
```

➡️ **Returns** latest analyzed posts for the country subreddit from the most recently saved batch in the database. The response includes original and translated content, along with sentiment analysis on comments.

<details>
<summary><strong>Example response format</strong> (click to open)</summary>

Note that some fields may be empty depending on the post content. For example, there is often no `content` field if the post only contains an image or a link. In such cases, the `content_link` field will contain the link to the media content. Also, if the post is already in English, the `content_eng`, `title_eng` and `comments_eng` fields will be empty, as no translation is needed.

Also note that the response does not contain all comments: currently, we only store a few example comments per post for brevity. `Num_comments` field indicates the total amount of comments on the post.

```jsonc
[
  {
    "_id": "68fb7be963ba754836af3d90", // MongoDB document ID
    "country_id": "IT",
    "country_name": "Italy",
    "posts": [
      {
        "comments": [
          "Non c’è nulla di più pericoloso del revisionismo storico. O dei “se solo…”. Che lo si faccia con buone, o cattive intenzioni, poco cambia. Un mondo violento crea leader violenti. Al giorno d’oggi, questi personaggi sarebbero CEO di aziende altisonanti. E finirebbero per influenzare molte più vite. Non si muore solo di spada.",
          "Khan, Cesare, Alessandro Magno, tutti genocidi assassini... infatti se non ci fossero stati il mondo antico avrebbe vissuto nel pacifismo più totale",
          "Non c’è rosa senza spine. Chi ha cambiato il mondo o voleva cambiarlo ha spento vite. \nEgel diceva “laddove non ci sono guerre la storia presenta pagine bianche”.\nLa penso uguale."
        ],
        "comments_eng": [
          "There is nothing more dangerous than historical revisionism. Or they say \"it's just...\". If you do it with good, or strong, intentions, it changes. A violent world creates violent leaders. Today, these people would be CEOs of high-growth companies. And they would end up influencing many more lives. Not only do you die.",
          "Khan, Cesare, Alessandro Magno, all the genocidal assassins ... in fact if we had not existed the ancient world would have lived in the most total peace",
          "There is no rose without a spine. Whoever changed the world or wanted to change it spent his life. Egel said “there are no wars, the story of the white pages.” I think it's a universal idea."
        ],
        "content": "",
        "content_eng": "",
        "content_link": "https://i.redd.it/elut1z7650xf1.jpeg", // Link to the post's media content (e.g., image or link to a news article). If the post has no additional media content, this matches 'link'
        "link": "https://reddit.com/r/Italia/comments/1oeq9gq/il_dualismo_di_reddit/", // Direct link to the original Reddit post
        "num_comments": 25, // Total amount of comments on the post
        "score": 219,
        "sentiment_values": {
          "average_compound": 0.001,
          "average_neg": 9.45,
          "average_neu": 78.15,
          "average_pos": 12.4
        },
        "title": "Il dualismo di reddit",
        "title_eng": "Reddit's Duality"
      },
    ],
    "subreddit": "italia",
    "timestamp": "Fri, 24 Oct 2025 13:15:21 GMT" // Time when the data was saved to db
  }
]
```
</details>

## Subscriptions endpoints

ℹ️ The subscription feature allows users to **subscribe to subreddits** with preferred analysis type (topics or posts). This way, the user can receive **personalized insights** based on their interests. Currently, the user can subscribe to one subreddit at a time. The subscribed subreddits will be analyzed regularly by our `GitHub Actions` pipeline.

### Get list of active subscriptions by analysis type
> GET /subscriptions/type/{type}

**Description**: Retrieves list of active subscriptions by analysis type.

| Parameter | Description | Options |
| --------- | ----------- | ------- |
| type | analysis type | `topics`, `posts` |

**Example request**:
```
http://127.0.0.1:5000/subscriptions/type/topics
```

<details>
<summary><strong>Example response format</strong> (click to open)</summary>

```json
[
  {
    "subreddit": "python",
    "analysis_type": "topics",
    "active": true,
    "subscribers": ["user1", "user2", "..."],
    "created_at": "2025-10-01T10:00:00.000Z"
  },
  {
    "subreddit": "stocks",
    "analysis_type": "topics",
    "active": true,
    "subscribers": ["user3", "user4", "..."],
    "created_at": "2025-10-02T11:30:00.000Z"
  }
]
```
</details>

### Get subscriptions for current user
> GET /subscriptions/current-user

**Description**: Retrieves active subscriptions for the current user.

**Example request**:
```
http://127.0.0.1:5000/subscriptions/current-user
```

<details>
<summary><strong>Example response format</strong> (click to open)</summary>
The subscribers list includes the current user. Users are represented by user ids (string).

```json
[
  {
    "subreddit": "python",
    "analysis_type": "topics",
    "active": true,
    "subscribers": ["current-user", "user2", "..."],
    "created_at": "2025-10-01T10:00:00.000Z"
  }
]
```
</details>

### Create a new subscription for current user
> POST /subscriptions/current-user/add/{subreddit}/{type}

**Description**: Creates a subscription for the current user with the preferred analysis type. If the same subreddit already has active subscriptions with the same analysis type, user is added to the subscribers list; if not, a new subscription is created. Currently, user can only subscribe to **1 subreddit at a time**.

| Parameter | Description | Examples |
| --------- | ----------- | -------- |
| subreddit | **any subreddit** with preferably 1000+ weekly contributions<br>- the existence of the subreddit is checked in the save process | `baseball`, `python`, `stocks`, `lifeprotips`, `gaming` |
| type | **analysis type**<br>- topic analysis identifies recurring themes within the subreddit, and analyses overall sentiment of the topic<br>- posts analysis focuses on individual posts and their sentiment | `topics`, `posts` |

**Example request**:
```
http://127.0.0.1:5000/subscriptions/current-user/add/python/topics
```

### Deactivate subscription for current user
> PATCH /subscriptions/current-user/deactivate

**Description**: Deactivates the current user's active subscription. The active subscription is checked in the process and not required as a parameter. If no active subscription exists, an error message is returned.

**Example request**:
```
http://127.0.0.1:5000/subscriptions/current-user/deactivate
```

### Get latest analyzed data for current user's subscription
> GET /subscriptions/current-user/latest-analyzed

**Description**: Retrieves the latest analyzed data for the current user's active subscription. The active subscription is checked in the process and not required as a parameter. If no active subscription exists, an error message is returned.

**Example request**:
```
http://127.0.0.1:5000/subscriptions/current-user/latest-analyzed
```

The response format depends on the analysis type of the subscription:

<details>
<summary><strong>Example response format for 'topics' analysis type</strong></summary>

```jsonc
{
  "type": "topics", // Subscription analysis type
  "data": [
    {
      "topic_id": 1,
      "topic": ["python", "code", "programming", "..."], // Keywords representing the topic
      "label": "Python Code Programming", // Official topic label
      "subreddit": "python",
      "summary": "Discussion about Python programming, coding tips, and best practices.", // LLM generated summary of the topic
      "num_posts": 30,
      "posts": [
        {
          "id": "lmnop456",
          "subreddit": "python",
          "title": "Best practices for writing clean Python code",
          "content": "Looking for tips on how to write clean and maintainable Python code",
          "comments": [
            "Use meaningful variable names"
          ],
          "num_comments": 15,
          "score": 95,
          "upvote_ratio": 0.92
        }
      ],
      "sentiment_values": {
        "average_compound": 0.12,
        "average_neg": 8.0,
        "average_neu": 78.0,
        "average_pos": 14.0,
        "comment_count": 30
      },
      "timestamp": "2025-10-05T14:23:45.678Z", // Time when the data was saved to db
      "type": "topics" // Subscription analysis type
    }
  ]
}
```
</details>

<details>
<summary><strong>Example response format for 'posts' analysis type</strong></summary>

```jsonc
{
  "type": "posts", // Subscription analysis type
  "data": [
    {
      "subreddit": "python",
      "posts": [
        {
          "id": "ghijk789",
          "title": "How to optimize Python code for performance?",
          "content": "Looking for tips on optimizing Python code for better performance.",
          "content_link": "https://reddit.com/r/python/...", // Link to the post's media content. If the post has no additional media content, this matches 'link'
          "link": "https://reddit.com/r/python/...", // Direct link to the original Reddit post
          "comments": [
            "Consider using built-in libraries for efficiency."
          ],
          "num_comments": 20,
          "score": 85,
          "upvote_ratio": 0.95,
          "sentiment_values": {
            "average_compound": 0.15,
            "average_neg": 5.0,
            "average_neu": 80.0,
            "average_pos": 15.0
          }
        }
      ],
      "timestamp": "2025-10-05T14:23:45.678Z", // Time when the data was saved to db
      "type": "posts" // Subscription analysis type
    }
  ]
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
<summary><strong>GitHub Actions</strong></summary>

We use **GitHub Actions** to automate data processing and keep our database up-to-date with fresh Reddit data. Currently, we have two main pipelines that run daily:

### 1. Trending topics analysis

This pipeline:
- Fetches 500 posts with a few example comments from a predefined set of subreddits
- Processes the data with topic modeling, summarization and sentiment analysis
- Stores the processed data in MongoDB Atlas

💡 We use the data for displaying trending topics and sentiment analysis results in the frontend. The data can also be used for tracking long-term trends.

**🔗 API Access**
- The subreddit options for this pipeline can be accessed via [`/subreddits`](#get-subreddits-that-have-data-available-in-the-database) endpoint
- The processed data can be accessed via [`/posts/latest/{subreddit}`](#get-latest-analyzed-posts-from-the-database) endpoint


### 2. Country subreddit analysis

This pipeline:
- Fetches 10 hot posts with comments from a predefined set of country subreddits
- Processes the data with language translation (if needed) and sentiment analysis
- Stores the processed data in MongoDB Atlas
  
💡 We use the data in a SVG map in frontend to visualize popular discussions and their sentiment across different countries and regions.

**🔗 API Access**
- The subreddit options for this pipeline can be accessed via [`/subreddits/countries`](#get-country-subreddits-that-have-data-available-in-the-database) endpoint
- The processed data can be accessed via [`/countries/latest/{subreddit}`](#get-latest-analyzed-country-data-from-the-database) endpoint

### Configuring subreddit options

The subreddit options for both pipelines can be modified in `app/config.py`. Note that the GitHub Actions pipelines currently run once a day, so new data may not be immediately available for all subreddits. To get immediate analysis results, you can run the data pipeline manually via command line (see instructions below) or via GitHub Actions.

### Run the pipelines locally

For testing purposes, you can also run the data pipelines locally to populate your database. To do this, ensure your `.env` file is set up with Reddit API and MongoDB Atlas credentials, then run the following commands in your terminal:
1. Trending topics analysis pipeline:
```
python -m scripts.topics_pipeline
```
2. Country subreddit analysis pipeline:
```
python -m scripts.countries_pipeline
```

⚠️ Note that processing all current subreddit options will take several minutes. Depending on your needs, you can modify the subreddit options in `app/config.py` to limit the amount of data processed.

### Why automate data processing?

Automating data processing with GitHub Actions offers several benefits:
- Ensures consistent and reliable daily updates
- Keeps the frontend up-to-date with fresh data
- Enables historical analysis and long-term trend tracking
- Delivers fast frontend performance without waiting for real-time processing

**Learn more:**
- [GitHub Actions documentation](https://docs.github.com/en/actions)
</details>

<details>
<summary><strong>Language Translation</strong></summary>
Coming soon
</details>

<p align="right"><a href="#reddit-trend-analyzer">Back to top 🔼</a></p>

## See Also

🖼️ [Frontend repository](https://github.com/ohjelmistoprojekti-ii-reddit-app/reddit-app-frontend) | 👥 [Organization page](https://github.com/ohjelmistoprojekti-ii-reddit-app/)

> Note: ChatGPT helped phrase parts of this README.
