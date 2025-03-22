from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig
from pydantic import SecretStr
import os
from dotenv import load_dotenv

load_dotenv()

gemini_model = 'gemini-2.0-flash-exp'
gemini_api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model=gemini_model, api_key=gemini_api_key)
# browser = Browser(
#     config=BrowserConfig(
#         chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
#     )
# )

async def main(msg):
    agent = Agent(
        task=f"Based on this data: {msg}, go to the URL of the cheapest flight and return the proper price",
        llm=llm
    )

    result = await agent.run()
    return result.final_result()