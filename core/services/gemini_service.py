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
        ROLE: You are a Senior Data Analyst and Subject Matter Expert in IT Service Management.

        CONTEXT:
        {response}

        TASK:
        1. Conduct a multi-layered analysis of the provided text to answer: {question}
        2. Extract specific technical methodologies (What, When, How) and personal anecdotes.
        3. If the data only shows titles/index entries, specifically state which pages seem missing.

        STRICT CONSTRAINTS:
        - Use ONLY the provided data.
        - Do not hallucinate external ITIL or ITSM definitions.

        OUTPUT STRUCTURE:
        # 📊 EXECUTIVE SUMMARY
        (A 3-sentence high-level overview of the answer.)

        # 🛠️ CORE DIAGNOSTIC METHODOLOGY
        - **The "What" Principle:** (Explain the importance of "What's changed?")
        - **The "When" Timeline:** (Explain the role of Event Viewer/Reliability Monitor.)
        - **The "How" Complexity:** (Explain user perceptions vs. technical reality.)

        # 📖 AUTHOR'S ORIGIN & ANALOGIES
        - **Personal Background:** (List the devices tinkered with: ZX81, Psion, etc.)
        - **Case Studies:** (Briefly summarize Scenario A or B if relevant.)

        # ⚠️ DATA GAPS & LIMITATIONS
        - (List any parts of the question that cannot be answered due to missing context.)
        """
    response = client.models.generate_content(
      model="gemini-2.5-flash",
      config=types.GenerateContentConfig(
        system_instruction="be a good writer"),
      contents=prompt
    )
    return response.text if hasattr(response, "text") else None