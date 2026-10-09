import os
from dotenv import load_dotenv

from ai.core.agent import Agent


load_dotenv()

agent = Agent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    domain="demandforecast"
)

result = agent.ask(
    question="What is the forecasted demand for 2026?",
    provider="openai"
)

print(result["answer"])