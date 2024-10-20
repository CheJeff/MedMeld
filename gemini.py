import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])

#generate response from file
def generate_info(json_input, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"{prompt}\n\n{json_input}")
    return response.text