import fitz
import re

def clean_text(text):
    text = text.replace("-\n", "")  # handle word breaks
    text = text.replace("\n", " ")  # flatten newlines
    text = re.sub(r'\s+', ' ', text)  # normalize all whitespace
    return text.strip()

def extract_sections_from_pdf(pdf_path, start_page=21):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(start_page, len(doc)):
        full_text += doc[page_num].get_text() + "\n"

    full_text = clean_text(full_text)

    # Match sections like: "1. Title...", "302. Murder...", "410A. Section title..."
    # Must be followed by a capital letter or bracket to ensure it's not e.g. a year
    pattern = re.compile(r'\b(\d{1,3}(?:[A-Z]|-[A-Z])?)\. (?=[A-Z\[])')

    # Split at every matched section header, and keep the headers
    parts = pattern.split(full_text)

    sections = []
    for i in range(1, len(parts), 2):
        section_num = parts[i]
        section_text = parts[i + 1].strip()
        full_section = f"{section_num}. {section_text}"
        sections.append({
            "section": section_num,
            "text": full_section
        })

    return sections
