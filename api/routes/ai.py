from ai.core.agent import Agent
from fastapi import APIRouter
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Dict, Any


load_dotenv()


router = APIRouter(
    prefix="/api/ai",
    tags=["AI Analytics"]
)


# ============================================================
# AGENTS
# ============================================================

customer_agent = Agent(
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


demandforecast_agent = Agent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    domain="demandforecast"
)


inventory_planning_agent = Agent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    domain="inventory_planning"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):
    question: str
    chat_history: List[Dict[str, Any]] = Field(
        default_factory=list
    )


# ============================================================
# CUSTOMER CHAT
# ============================================================

@router.post("/customer-chat")
async def customerChat(data: ChatRequest):

    result = customer_agent.ask(
        question=data.question,
        chat_history=data.chat_history,
        provider="openai",
    )

    return result


# ============================================================
# PRODUCT CHAT
# ============================================================

@router.post("/product-chat")
async def productChat(data: ChatRequest):

    result = product_agent.ask(
        question=data.question,
        chat_history=data.chat_history,
        provider="openai",
    )

    return result


# ============================================================
# SALES CHAT
# ============================================================

@router.post("/sales-chat")
async def salesChat(data: ChatRequest):

    result = sales_agent.ask(
        question=data.question,
        chat_history=data.chat_history,
        provider="openai",
    )

    return result


# ============================================================
# DEMAND FORECASTING CHAT
# ============================================================

@router.post("/demandforecast-chat")
async def demandForecastChat(data: ChatRequest):

    result = demandforecast_agent.ask(
        question=data.question,
        chat_history=data.chat_history,
        provider="openai",
    )

    return result


# ============================================================
# INVENTORY PLANNING CHAT
# ============================================================

@router.post("/inventory-planning-chat")
async def inventoryPlanningChat(data: ChatRequest):

    result = inventory_planning_agent.ask(
        question=data.question,
        chat_history=data.chat_history,
        provider="openai",
    )

    return result