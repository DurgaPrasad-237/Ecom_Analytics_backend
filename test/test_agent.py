import os
from dotenv import load_dotenv

from ai.core.agent import Agent


load_dotenv()

agent = Agent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    domain="customer"
)

result = agent.ask(
    question="How many customers we have?",
    provider="openai"
)

print(result["answer"])