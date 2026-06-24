from src.pipeline.rag_pipeline import (
    ask_question
)

question = input(
    "Ask Question: "
)

answer, sources, confidence = ask_question(
    question
)

print("\nANSWER:\n")

print(answer)

print(f"\nConfidence Score: {confidence}\n")

print("SOURCES:\n")

for source in sources:
    print(source)