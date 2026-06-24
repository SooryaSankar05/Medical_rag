# src/preprocessing/cleaner.py

def remove_references(text_or_pages):

    # Check if input is new page-based format or old text format
    if isinstance(text_or_pages, list) and len(text_or_pages) > 0 and isinstance(text_or_pages[0], dict):
        # New format: list of pages with page_number and text
        keywords = [
            "References",
            "REFERENCES",
            "Bibliography"
        ]

        for keyword in keywords:
            for page in text_or_pages:
                pos = page["text"].find(keyword)
                if pos != -1:
                    # Truncate this page and all subsequent pages
                    page_index = text_or_pages.index(page)
                    if pos > 0:
                        # Keep partial page up to references
                        text_or_pages[page_index]["text"] = page["text"][:pos]
                    # Remove all pages after this one
                    return text_or_pages[:page_index + 1]

        return text_or_pages
    else:
        # Old format: plain text (backward compatibility)
        keywords = [
            "References",
            "REFERENCES",
            "Bibliography"
        ]

        for keyword in keywords:
            pos = text_or_pages.find(keyword)

            if pos != -1:
                return text_or_pages[:pos]

        return text_or_pages