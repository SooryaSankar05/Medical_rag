from src.pipeline.rag_pipeline import (
    ask_question
)

question = input(
    "Ask Question: "
)

answer, sources, confidence, timing = ask_question(
    question
)

print("\nANSWER:\n")

print(answer)

print(f"\nConfidence Score: {confidence}")
print(f"Retrieval Time: {timing['retrieval_time']}s")
print(f"Generation Time: {timing['generation_time']}s")
print(f"Total Time: {timing['total_time']}s\n")

print("SOURCES:\n")

for source in sources:
    print(source)