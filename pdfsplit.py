# pdf_to_ocr.py
import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract

# if tesseract is not in PATH, set its path here (for Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def pdf_to_ocr(input_pdf, output_folder, lang="eng"):
    # make output folder if not exists
    os.makedirs(output_folder, exist_ok=True)

    # open pdf
    doc = fitz.open(input_pdf)

    for page_num in range(len(doc)):
        page = doc[page_num]

        # render page to image
        pix = page.get_pixmap(dpi=300)  # 300 dpi for better OCR
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # OCR text
        text = pytesseract.image_to_string(img, lang=lang)

        # save to text file (page_1.txt, page_2.txt, etc.)
        output_path = os.path.join(output_folder, f"page_{page_num+1}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"OCR done for page {page_num+1}/{len(doc)} -> {output_path}")

    doc.close()
    print(f"All pages saved in {output_folder}")


if __name__ == "__main__":
    input_pdf = "input2.pdf"                # replace with your file
    output_folder = "ocr_output"           # folder to save page texts
    pdf_to_ocr(input_pdf, output_folder, lang="eng")  # use "hin" for Hindi or "eng+hin" for both
