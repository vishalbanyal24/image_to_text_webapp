import google.generativeai as genai
from django.conf import settings

# Reuse the configured API key from settings
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_text(prompt: str):
    response = model.generate_content(prompt)
    return response.text
