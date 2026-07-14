# -----------------------------------------
# Step 1: Load all the required libraries
# -----------------------------------------

from dotenv import load_dotenv
load_dotenv()

import os
import requests

from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage
from langchain_mistralai import ChatMistralAI
from tavily import TavilyClient
from rich import print

# -----------------------------------------
# Step 2: Initialize API Keys
# -----------------------------------------

weather_api_key = os.getenv("OPENWEATHER_API_KEY")
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# -----------------------------------------
# Step 3: Create Weather Tool
# -----------------------------------------

@tool
def get_weather(city: str) -> str:
    """
    Fetch the current weather details of a city.
    """

    url = "https://api.openweathermap.org/data/2.5/weather"

    response = requests.get(
        url,
        params={
            "q": city,
            "appid": weather_api_key,
            "units": "metric"
        }
    )

    if response.status_code != 200:
        return "Unable to fetch weather."

    data = response.json()

    return (
        f"Weather in {city}\n"
        f"Temperature : {data['main']['temp']}°C\n"
        f"Humidity : {data['main']['humidity']}%\n"
        f"Condition : {data['weather'][0]['description']}\n"
        f"Wind Speed : {data['wind']['speed']} m/s"
    )


# -----------------------------------------
# Step 4: Create News Tool
# -----------------------------------------

@tool
def get_news(city: str) -> str:
    """
    Fetch the latest news of a city using Tavily.
    """

    response = tavily_client.search(
        query=f"Latest news about {city}",
        topic="news",
        max_results=5
    )

    if not response.get("results"):
        return f"No news found for {city}."

    news = []

    for i, article in enumerate(response["results"], start=1):
        title = article.get("title")
        url = article.get("url")

        news.append(
            f"{i}. {title}\n{url}"
        )

    return "\n\n".join(news)


# -----------------------------------------
# Step 5: Human Approval Middleware
# -----------------------------------------

@wrap_tool_call
def human_approval(request, handler):
    """
    Ask for human approval before every tool call.
    """

    tool_name = request.tool_call["name"]

@wrap_tool_call
def human_approval(request, handler):
    """
    Human approval middleware.
    Streamlit UI ke liye automatic approval.
    """

    return handler(request)


# -----------------------------------------
# Step 6: Initialize the Mistral LLM
# -----------------------------------------

llm = ChatMistralAI(
    model="mistral-small-latest",
    api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0
)

# -----------------------------------------
# Step 7: Create AI Agent
# -----------------------------------------

agent = create_agent(
    model=llm,
    tools=[get_weather, get_news],
    middleware=[human_approval]
)

# -----------------------------------------
# Step 8: Start Chatbot
# -----------------------------------------

# -----------------------------------------
# Step 8: Start Chatbot
# -----------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("      CITY INTELLIGENCE SYSTEM")
    print("Type 'exit' to quit")
    print("=" * 60)

    while True:

        user_input = input("\nYou : ")

        if user_input.lower() == "exit":
            print("\nThank you for using the City Intelligence System!")
            break

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            }
        )

        print("\nAI :")

        for message in response["messages"]:
            if message.type == "ai" and message.content:
                print(message.content)