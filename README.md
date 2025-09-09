## 💻 This is the backend service for a web application that:
- fetches **trending Reddit topics**
- analyzes the **sentiment** of public discussions
- and enables **filtering topics by sentiment** (positive, negative, neutral)

> 🚧 This project is in early development.

## 🛠️ Tech Stack (Planned)

- **Language:** [Python](https://docs.python.org/3/)
- **Framework:** [Flask](https://flask.palletsprojects.com/en/stable/)
- **Reddit API:** [Async PRAW](https://asyncpraw.readthedocs.io/en/stable/)
- **Topic modeling:** [BERTopic](https://maartengr.github.io/BERTopic/index.html)
- **Sentiment analysis:** VADER or TextBlob or Hugging Face *(TBD)*
- **Database:** *(TBD)*

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
pip install flask-cors

### Connecting to Reddit API (Async PRAW)
Assuming you have already registered an app to Reddit's developer portal:
- Create **.env** file in the root of the project
- Add your Reddit app credentials to the file:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

### Try it out

View example Reddit posts and topic modeling results by running the script:
```bash
python demo.py
```

The results will be printed in your terminal.

💡 You can change the subreddit, type of posts and number of posts in `demo.py` to experiment with different data.

<hr>

View the REST API:

```bash
python run.py
```

When everything is working (you see the message on your console 'Running on http://127.0.0.1:5000') go to your browser and type: http://127.0.0.1:5000/posts/ where you can see 10 movie posts or type: http://127.0.0.1:5000/posts/subreddit/number_of_posts where you can select a subreddit of your choise and the number of posts you want to see (http://127.0.0.1:5000/posts/movies/5).

## 🔎 Solutions Overview
An overview of our solutions and approaches across the project's key areas.

<details>
<summary><strong>Topic Modeling</strong></summary>

**Topic modeling** is a natural language processing (NLP) technique for identifying themes and topics from text data.

There are multiple tools available for this task, and for this project, we chose **BERTopic**, a modern framework that leverages machine learning to extract easily interpretable topics.

<strong>Core concepts of BERTopic</strong>

BERTopic is a flexible framework that allows you to customize each component based on your needs. For example, embeddings can be generated with almost any sentence-transformers model, with BERT as the default option.

Here are the key steps in BERTopic and the models we used for them:

1. **Embedding**: Converts text into numerical vectors that capture meaning, so similar words are close in vector space. For example, words “*movie*” and “*film*” might end up near each other because they mean similar things.
    - Model: [all-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2)
2. **Dimensionality reduction**: Simplifies the high-dimensional vectors, making patterns and clusters easier to detect.
    - Model: [UMAP](https://umap-learn.readthedocs.io/en/latest/)
3. **Clustering**: Groups similar embeddings into coherent topic clusters.
    - Model: [HDBSCAN](https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html)
4. **Topic representation**: Labels each cluster with a few key words summarizing its main theme.
    - Model: BERTopic default, class-based TF-IDF (c-TF-IDF)


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
Coming soon
</details>

<details>
<summary><strong>REST API</strong></summary>
Coming soon
</details>
<br>
> Note: ChatGPT helped phrase parts of this README.
