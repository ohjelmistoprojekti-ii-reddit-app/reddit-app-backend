from transformers import pipeline
import json
from importlib import resources

"""
This method is for summarizing topic labels into a more understandable form using LLM.

Test the results by running this file directly:
python -m app.helpers.topic_label_summary

Change the test data and model below as needed.

Note: this is still a work in progress, results are not very good yet.
"""

# --- Choose testdata ---
test_data = 'technology_test_data.json'
#test_data = 'movies_test_data.json'
#test_data = 'jobs_test_data.json'

# --- Choose model ---
model = "google/flan-t5-large"
#model = "Qwen/Qwen3-0.6B"

# Pipeline and output type according to model
if "Qwen" in model:
    pipeline_type = "text-generation"
    output_type = "generated_text"
elif "flan-t5" in model:
    pipeline_type = "summarization"
    output_type = "summary_text"

generator = pipeline(
    pipeline_type,
    model=model,
    device_map="auto"
)

# Load test data
with resources.open_text('app.helpers', test_data) as f:
    data = json.load(f)

# Generate short, more understandable topic labels
def summarize_topic_label(raw_topics, posts):
    docs_list = []
    for post in posts:
        title_words = post['title'].lower().split()
        # Only keep posts that contain at least one of the topic words in the title
        if any(topic in title_words for topic in raw_topics):
            docs_list.append(post['title'])

    if not docs_list:
        return "No matching documents"

    keywords = " | ".join(raw_topics)
    docs = " | ".join(docs_list)
    print("Docs:", docs)

    prompt = f"""
    I have a topic that is described with the following keywords: {keywords}
    The topic includes these documents: {docs}
    What is the main theme of this topic? Summarize it with 1-5 words.
    """

    output = generator(prompt, max_new_tokens=30, do_sample=False)
    result = output[0][output_type].strip()

    return result

if __name__ == "__main__":
    for topic in data:
        label = summarize_topic_label(topic['raw_topic'], topic['posts'])
        print(f"{topic['raw_topic']} --> {label}\n")