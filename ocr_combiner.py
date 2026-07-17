import os
import re

def is_bad_text(text: str) -> bool:
    """
    Heuristic check for bad OCR text.
    Returns True if text looks corrupted.
    """
    if len(text.strip()) < 30:  # too short to be useful
        return True
    # Check proportion of non-alphanumeric chars
    clean_chars = re.sub(r"[^\w\s]", "", text)
    if len(clean_chars) / max(1, len(text)) < 0.5:
        return True
    # Specific gibberish markers
    if any(bad in text for bad in ["«", "©", "ae", "~~", "SE io"]):
        return True
    return False

def combine_txt_files(input_folder="ocr_output", output_file="input.txt"):
    all_text = []
    txt_files = sorted(
        [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    )

    for file in txt_files:
        file_path = os.path.join(input_folder, file)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not is_bad_text(text):
            all_text.append(text)
        else:
            print(f"Skipping {file} (bad OCR text)")

    combined_text = "\n\n".join(all_text)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(combined_text)

    print(f"\nCombined {len(all_text)} clean pages into {output_file}")

# ------------------ Run ------------------
if __name__ == "__main__":
    combine_txt_files("ocr_output", "input2.txt")
