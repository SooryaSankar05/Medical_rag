# src/preprocessing/cleaner.py

def remove_references(text):

    keywords = [
        "References",
        "REFERENCES",
        "Bibliography"
    ]

    for keyword in keywords:
        pos = text.find(keyword)

        if pos != -1:
            return text[:pos]

    return text