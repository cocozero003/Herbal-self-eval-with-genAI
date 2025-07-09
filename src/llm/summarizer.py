import os
import openai
from .prompts import TEMPLATES

class Summarizer:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def summarize(self, content, module):
        prompt = TEMPLATES[module].replace("{{text}}", content[:1000])
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
