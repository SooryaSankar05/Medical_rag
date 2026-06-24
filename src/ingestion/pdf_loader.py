import fitz


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)

    pages_text = []

    for page_num, page in enumerate(doc):
        pages_text.append({
            "page_number": page_num + 1,
            "text": page.get_text()
        })

    doc.close()

    return pages_text