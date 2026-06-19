from src.pipeline.rag_pipeline import (
    ask_question
)

question = input(
    "Ask Question: "
)

answer, sources = ask_question(
    question
)

print("\nANSWER:\n")

print(answer)

print("\nSOURCES:\n")

for source in sources:
    print(source)