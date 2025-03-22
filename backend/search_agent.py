from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")

class Suggestion(BaseModel):
    url: str
    departureDate: str
    returnDate: str
    departureAirport: str
    arrivalAirport: str
    flightDuration: str
    companyName: str

class AnswerFormat(BaseModel):
    answer: str
    suggestions: list[Suggestion]

def run(msg):
    response = client.chat.completions.create(
        model="sonar",
        messages=[{
            "role": "system",
            "content": (
                "You are a professional travel agent."

                "Rules:"
                "1. Provide the final answer in a structured JSON format."
                "2. Do not include any explanations or intermediate steps."
                "3. The answer should be a list of suggestions."
                "4. The list of suggestions should be an array of objects."
                "5. Each suggestion should have an URL pointing to the company website."
                "6. Each suggestion should have a departure date and a return date."
                "7. Each suggestion should have a departure and arrival airport."
                "8. Each suggestion should have a flight duration."
                "9. Each suggestion should have a company name."
                "10. Dates should be in the format YYYY-MM-DD like: 2023-05-02."
                "11. Airports should be in the format IATA code like: MAD"

                "Steps:"
                "1. Determine if the response should be a single JSON object or an array of suggestions."
                "2. If it is an array of suggestions, include a brief introduction in the JSON object that summarizes the query."
                "3. Each suggestion should be a separate JSON object within the array, containing relevant details such as destination, price, and travel dates."
            ),
        }, 
        {   
            "role": "user",
            "content": (
                msg
            ),
        }],
        response_format={
		    "type": "json_schema",
            "json_schema": {"schema": AnswerFormat.model_json_schema()},
        },
    )
    return response.choices[0].message.content
