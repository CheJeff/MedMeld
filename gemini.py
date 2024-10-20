import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])

#generate response from file
def generate_info(json_input, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"My question is: {prompt}\n\n and the following is my record: {json_input} \n\n summarize my record before answering my question")
    return response.text