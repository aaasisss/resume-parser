import os
from openai import OpenAI
import google.generativeai as genai

# OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Google Gemini setup
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_models = {
    "pro": genai.GenerativeModel("gemini-1.5-pro"),
    "flash": genai.GenerativeModel("gemini-1.5-flash"),
}
