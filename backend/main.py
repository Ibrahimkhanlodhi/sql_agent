from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from database import seed_database, DB_PATH
from agent import run_query

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Seed DB on startup if it doesn't exist
    if not os.path.exists(DB_PATH):
        print("Seeding database...")
        seed_database()
    yield


app = FastAPI(
    title="SQL Agent API",
    description="Natural language interface to a SQLite database using LangChain + Groq",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sql_queries: list[str]


EXAMPLE_QUESTIONS = [
    "Who are the top 5 customers by total spending?",
    "What is the best-selling product by quantity?",
    "How many orders were placed per country?",
    "What is the total revenue from completed orders?",
    "Which product category generates the most revenue?",
    "Show me customers who joined in 2023 and have spent more than $200.",
    "What is the average order value per customer?",
    "List the top 3 most expensive products still in stock.",
]


@app.get("/")
def root():
    return {
        "message": "SQL Agent API is running.",
        "docs": "/docs",
        "example_questions": EXAMPLE_QUESTIONS,
    }


@app.post("/query", response_model=QueryResponse)
async def query_database(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400, detail="Question cannot be empty.")

    result = run_query(request.question)
    return QueryResponse(
        answer=result["answer"],
        sql_queries=result["sql_queries"],
    )


@app.post("/reset-db")
def reset_database():
    """Re-seed the database with fresh data."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    seed_database()
    return {"message": "Database reset and re-seeded."}


@app.get("/schema")
def get_schema():
    """Return the database schema for transparency."""
    return {
        "tables": {
            "customers": ["id", "name", "email", "country", "joined_date"],
            "products": ["id", "name", "category", "price", "stock"],
            "orders": ["id", "customer_id", "order_date", "status", "total"],
            "order_items": ["id", "order_id", "product_id", "quantity", "unit_price"],
        }
    }
