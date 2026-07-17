import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
from nltk.tokenize import sent_tokenize

# ---------------------------
# Download NLTK punkt tokenizer if not already
# ---------------------------
nltk.download("punkt")

# ---------------------------
# Load Legal Summarization Model
# ---------------------------
model_name = "mithra99/bart-indian-law"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cpu")
if model.config.decoder_start_token_id is None:
    model.config.decoder_start_token_id = tokenizer.bos_token_id

# ---------------------------
# Sentence-based chunking function
# ---------------------------


def chunk_text_by_sentences(text, max_sentences=15):
    """
    Splits text into chunks of sentences for summarization.
    """
    sentences = sent_tokenize(text)
    chunks = [sentences[i:i + max_sentences] for i in range(0, len(sentences), max_sentences)]
    return chunks

# ---------------------------
# Generative factual summarization function
# ---------------------------


def summarize_text(text, section_name="Section"):
    """
    Generates a factual summary of legal text using the model.
    Adds grounding instructions and post-filters sensitive hallucinated terms.
    """
    chunks = chunk_text_by_sentences(text, max_sentences=15)
    summaries = []

    # List of sensitive terms to check
    hallucination_keywords = ["rape", "murder", "sexual", "assault", "kidnap"]

    for idx, chunk in enumerate(chunks):
        chunk_text = " ".join(chunk)
        # Prepend grounding instruction
        prompt_text = (
            "Summarize the following legal text accurately and factually. "
            "Use only information present in the text. "
            "Do not add, assume, or invent details.\n\n"
            + chunk_text
        )

        inputs = tokenizer(
            prompt_text,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        )

        # Generate summary with controlled decoding
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=250,   # shorter to avoid hallucination
            min_length=100,
            num_beams=2,      # lower beams to reduce pattern completion hallucinations
            early_stopping=True,
            no_repeat_ngram_size=3,
            length_penalty=2.2
        )

        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        # Post-generation hallucination filter
        for word in hallucination_keywords:
            if re.search(rf"\b{word}\b", summary, re.IGNORECASE) and word not in chunk_text:
                summary = summary.replace(word, "[REDACTED]")

        summaries.append(f"\n### {section_name} {idx+1}\n{summary}\n")

    # Combine into structured summary
    structured_summary = "# Legal Case Summary\n" + "\n".join(summaries)
    return structured_summary

# ---------------------------
# Main Execution
# ---------------------------


if __name__ == "__main__":
    with open("input2.txt", "r", encoding="utf-8") as f:
        case_text = f.read()

    structured_summary = summarize_text(case_text, section_name="Part")

    # Save to file
    with open("structured_summary.txt", "w", encoding="utf-8") as f:
        f.write(structured_summary)

    print("Structured summary saved to structured_summary.txt")
