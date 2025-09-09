giy# Reddit Trend Analyzer

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

### Try It Out
The app is still in early development, so there's not much you can do.

However, you can test the Reddit-App-Backend REST API connection by running the script:
```bash
python run.py
```
When everything is working (you see the message on your console 'Running on http://127.0.0.1:5000') go to your browser and type: http://127.0.0.1:5000/posts/ where you can see 10 movie posts or type: http://127.0.0.1:5000/posts/subreddit/number_of_posts where you can select a subreddit of your choise and the number of posts you want to see (http://127.0.0.1:5000/posts/movies/5).
However, you can view example Reddit posts and topic modeling results by running the script:
```bash
python demo.py
```

The results will be printed in your terminal.

💡 You can change the subreddit, type of posts and number of posts in `demo.py` to experiment with different data.

## 🔎 Solutions Overview
An overview of our solutions and approaches across the project's key areas.

<details><summary>Topic Modeling</summary>
Coming soon
</details>

<details><summary>Sentiment Analysis</summary>
Coming soon
</details>

<details><summary>REST API</summary>
Coming soon
</details>
