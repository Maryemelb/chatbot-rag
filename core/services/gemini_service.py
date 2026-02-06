from google import genai
from google.genai import types
import os
import google.genai as genai
import re
from dotenv import load_dotenv
load_dotenv()
def unswer(question,response):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    You are an IT Analyst. Based ONLY on the provided text, answer this question: {question}

    Context:
    {response}

    Answer Requirements:
    1. Provide a brief 3-sentence summary.

    Constraints:
    - Use only the data provided.
    - Do not use outside knowledge or definitions.
    """
    response = client.models.generate_content(
      model="gemini-2.5-flash",
      config=types.GenerateContentConfig(
        system_instruction="be a good writer"),
      contents=prompt
    )
    return response.text if hasattr(response, "text") else None