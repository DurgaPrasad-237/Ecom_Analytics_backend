from ai.core.agent import Agent
from fastapi import APIRouter,Request
import os
from dotenv import load_dotenv
load_dotenv()
router = APIRouter(
    prefix="/api/ai",
    tags=['AI Analytics']
)

agent = Agent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    domain="customer"
)


product_agent = Agent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    domain="product"
)

sales_agent = Agent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    domain="sales"
)

@router.post("/customer-chat")
async def customerChat(req: Request,question:str):
    # question = req.query_params.get("question")

    # data = await req.json()

    # question = data["question"]
    # chat_history = data.get("chat_history", [])

    result = agent.ask(
        question=question,
        # chat_history=chat_history,
        provider="openai",
    )

    return result


@router.post("/product-chat")
async def productChat(req: Request):

    data = await req.json()

    question = data["question"]
    chat_history = data.get("chat_history", [])

    print(question)
    print(chat_history)

    result = product_agent.ask(
        question=question,
        chat_history=chat_history,
        provider="openai",
    )

    return result


@router.post("/sales-chat")
async def SalesChat(req: Request):

    data = await req.json()

    question = data["question"]
    chat_history = data.get("chat_history", [])

    print(question)
    print(chat_history)

    result = sales_agent.ask(
        question=question,
        chat_history=chat_history,
        provider="openai",
    )

    return result