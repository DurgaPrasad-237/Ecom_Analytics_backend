from ai.core.agent import Agent
from fastapi import APIRouter,Request
import os
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import List, Dict, Any
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

class ChatRequest(BaseModel):
    question: str
    chat_history: List[Dict[str, Any]] = Field(default_factory=list)



@router.post("/customer-chat")
async def customerChat(data: ChatRequest):

    result = agent.ask(
        question=data.question,
        chat_history=data.chat_history,
        provider="openai",
    )

    return result


@router.post("/product-chat")
async def productChat(data: ChatRequest):

    result = product_agent.ask(
        question=data.question,
        chat_history=data.chat_history,
        provider="openai",
    )

    return result


@router.post("/sales-chat")
async def SalesChat(data: ChatRequest):

    result = sales_agent.ask(
        question=data.question,
        chat_history=data.chat_history,
        provider="openai",
    )

    return result