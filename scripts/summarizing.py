import re
from scripts.text_processing import filter_factual_sentences, smart_split, clean_text

def summarize_texts(texts, summarizer):
    tokenizer = summarizer.tokenizer
    max_tokens = min(480, tokenizer.model_max_length - 32)

    all_chunks = []
    for text in texts:
        cleaned_texts = clean_text(text)
        filtered_texts = filter_factual_sentences(cleaned_texts)
        chunks = smart_split(filtered_texts, tokenizer, max_tokens=max_tokens)
        all_chunks.extend(chunks)

    partial_summaries = []

    for chunk in all_chunks:
        if not chunk.strip():
            continue
        prompt = (
            "Summarize the following into a factual and neutral news report. "
            "Exclude personal opinions, jokes, or speculation. Focus only on verifiable facts and official reports:\n\n"
            + chunk
        )
        try:
            summary = summarizer(prompt, max_new_tokens=100, min_length=10, do_sample=False)
            partial_summaries.append(summary[0]['summary_text'])
        except Exception as e:
            print(f"Error summarizing chunk: {e}")
            continue

    # Combine all chunk summaries
    combined_summary_text = " ".join(partial_summaries)

    # Final high-level summary of the full document
    final_prompt = (
        "Summarize the following discussion thread into a concise and factual news update. Focus on key facts only, and exclude opinions or speculation:\n"
        + combined_summary_text
    )

    try:
        final_summary = summarizer(final_prompt, max_new_tokens=300, min_length=80, do_sample=False)
        final_text = re.sub(r'\s+', ' ', final_summary[0]['summary_text']).strip()
        return final_text
    except Exception as e:
        print(f"Error during final summarization: {e}")
        return combined_summary_text.strip()  # Fallback