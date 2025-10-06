from transformers import pipeline

import json
from importlib import resources

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",
    device_map="auto"
)

#test_data = 'technology_test_data.json'
test_data = 'movies_test_data.json'
with resources.open_text('app.helpers', test_data) as f:
    data = json.load(f)

"""
Simpler method for processing topic labels: choose top 3 words that don't contain numbers and are not too similar to each other,
then use LLM to reorder them into a proper phrase.

Doesn't work properly, Flan-T5 is not too good at this task. Might try with another model later.
"""

def process_topic_label(raw_topics):
    # Remove words that contain numbers or are very similar to each other
    top_words = []
    for raw_word in raw_topics:
        if any(char.isdigit() for char in raw_word):
            continue

        is_similar = False
        for top_word in top_words:
            if raw_word.lower() in top_word.lower() or top_word.lower() in raw_word.lower():
                is_similar = True
                break

        if not is_similar:
            top_words.append(raw_word)

    top_three = top_words[:3]
    topic_text = " ".join(top_three)

    # Use Flan-T5 to convert words into a proper phrase
    prompt = f"Reorder the following words to a proper phrase:\n{topic_text}\nAnswer:"
    output = generator(prompt, max_new_tokens=20, do_sample=False)
    ordered_topic = output[0]['generated_text'].strip()

    return ordered_topic.title()

if __name__ == "__main__":
    for topic in data:
        label = process_topic_label(topic['raw_topic'])
        print(f"{topic['raw_topic']} --> {label}\n")
