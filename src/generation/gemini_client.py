import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(prompt):

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        error_str = str(e)
        print(f"Gemini Error: {e}")

        # Handle 503 UNAVAILABLE error specifically
        if "503" in error_str or "UNAVAILABLE" in error_str:
            return "The language model is temporarily unavailable. Please try again."

        return "Gemini request failed."