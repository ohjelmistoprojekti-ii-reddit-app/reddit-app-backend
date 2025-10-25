import langid
from transformers import T5Tokenizer, T5ForConditionalGeneration
from app.helpers.supported_languages import get_supported_languages
from app.helpers.text_processing import remove_links
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize
import torch

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large", legacy=False)
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")

async def batch_translate(sentences, original_language, tokenizer, model):
    prompts = [f"Translate from {original_language} to English: {s}" for s in sentences]
    inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True)
    with torch.inference_mode():  # Disable gradient tracking for faster inference
        outputs = model.generate(**inputs, max_length=512)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)


async def translate_into_english(text, tokenizer, model):
    supported_languages = get_supported_languages()

    try:
        # Identifies the original language of the title
        language, confidence = langid.classify(text)
        
        if language == 'en':
            return text
        if language not in supported_languages:
            return "This language is so far unsupported"
        
        # Identifies the name of language based on supported_languages dictionary
        original_language = supported_languages[language]
        text_without_links = remove_links(text)
        sentences = sent_tokenize(text_without_links, language=supported_languages[language])

        translations = await batch_translate(sentences, original_language, tokenizer, model)
    
        return " ".join(translations)
    except Exception as e:
        print(f"Translation error: {e}\nText snippet: {text[:200]}...")
        return text
    
