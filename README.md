# Reddit Trend Analyzer

## 💻 This is the backend service for a web application that:
- fetches **trending Reddit topics**
- analyzes the **sentiment** of public discussions
- and enables **filtering topics by sentiment** (positive, negative, neutral)

> 🚧 This project is in early development.


## 🛠️ Tech Stack (Planned)

- **Language:** Python
- **Framework:** Flask
- **Reddit API:** Async PRAW
- **Topic modeling:** BERTopic or LDA
- **Sentiment analysis:** VADER or TextBlob or Hugging Face *(TBD)*
- **Database:** *(TBD)*

## 🚀 For Getting Started

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

### Connecting to Async PRAW (Reddit API)
Assuming you have already registered an app to Reddit's developer portal:
- Create **.env** file in the root of the project
- Add your Reddit app credentials to the file:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

### Try it out
The app is still in early development, so there's not much you can do.

However, you can test the Reddit API connection by running the script:
```bash
python reddit_analyzer.py
```

If the connection is successful, example Reddit posts will be printed in your terminal.

💡 You can change the subreddit and number of posts directly in `reddit_analyzer.py` to experiment with different data.