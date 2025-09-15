from transformers import T5Tokenizer, T5ForConditionalGeneration

# IN PROGRESS

# generate short, more understandable topic labels from the topic modeling results
def summarize_topic_labels(raw_topics, posts):
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

    # best_post = max(posts, key=lambda p: p['score'])
    # processed_post = []
    # post_parts = [best_post['title'], best_post['content']]
    # for comment in best_post['comments'][:3]:
    #     if comment:
    #         post_parts.append(comment)
    # joined_post = " ".join(post_parts)
    # processed_post.append(joined_post)

    input_text = (
        f"Summarize these words into a coherent title, in short sentence-form: {raw_topics}."
        # f"Example document under this topic: {" // ".join(processed_post)}."
    )

    # tokenize the text into input ids so the model can process it
    input_ids = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True).input_ids

    # generate the results using token ids
    outputs = model.generate(input_ids, min_length=5, max_length=25, num_beams=4, repetition_penalty=2.0, length_penalty=1.0, early_stopping=True)

    # convert results back to text
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return result