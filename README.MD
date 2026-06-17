# SQL Agent — Chat With Your Database

A natural language interface for SQL databases. Ask questions in plain English, get answers backed by real SQL queries — no SQL knowledge required.

Built with **FastAPI**, **LangChain**, **Groq (LLaMA 3.1)**, and **Next.js 14**.

---

## Demo

> **"Who are the top 5 customers by total spending?"**

```
Answer: The top 5 customers by total spending are:
1. Emma Müller — $1,847.23
2. Priya Sharma — $1,654.10
3. Alice Rossi — $1,521.80
...

Generated SQL:
SELECT c.name, SUM(o.total) AS total_spent
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.status = 'completed'
GROUP BY c.id, c.name
ORDER BY total_spent DESC
LIMIT 5;
```

---

## Features

- **Plain English queries** — no SQL needed from the user
- **SQL transparency** — see every query the agent generated
- **Auto-seeded DB** — spins up a realistic e-commerce dataset on first run
- **Schema endpoint** — expose DB structure for debugging or client apps
- **Reset endpoint** — re-seed the database anytime

---

## Stack

| Layer    | Technology                       |
| -------- | -------------------------------- |
| LLM      | Groq — LLaMA 3.1 8B Instant      |
| Agent    | LangChain SQL Agent              |
| Backend  | FastAPI + SQLAlchemy             |
| Database | SQLite (swap-ready for Postgres) |
| Frontend | Next.js 14 + Tailwind CSS        |

---

## Database Schema

```
customers     → id, name, email, country, joined_date
products      → id, name, category, price, stock
orders        → id, customer_id, order_date, status, total
order_items   → id, order_id, product_id, quantity, unit_price
```

---

## Getting Started

### 1. Clone

```bash
git clone https://github.com/your-username/sql-agent.git
cd sql-agent
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Seed the database and start the API:

```bash
python database.py        # optional — auto-runs on first API start
uvicorn main:app --reload
```

API runs at `http://localhost:8000` — docs at `/docs`.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:3000`.

---

## Example Questions

```
Who are the top 5 customers by total spending?
What is the best-selling product by quantity?
How many orders were placed per country?
What is the total revenue from completed orders?
Which product category generates the most revenue?
Show me customers who joined in 2023 and spent more than $200.
What is the average order value per customer?
List the top 3 most expensive products still in stock.
```

---

## API Reference

| Method | Endpoint    | Description                      |
| ------ | ----------- | -------------------------------- |
| POST   | `/query`    | Run a natural language question  |
| GET    | `/schema`   | Return the database schema       |
| POST   | `/reset-db` | Re-seed the database             |
| GET    | `/`         | Health check + example questions |

### POST `/query`

```json
// Request
{ "question": "What is the total revenue this year?" }

// Response
{
  "answer": "The total revenue from completed orders is $48,392.15.",
  "sql_queries": [
    "SELECT SUM(total) FROM orders WHERE status = 'completed';"
  ]
}
```

---

## Architecture

```
User types question
       │
       ▼
  Next.js Frontend
       │  POST /query
       ▼
  FastAPI Backend
       │
       ▼
  LangChain SQL Agent
  ┌────────────────┐
  │  1. Inspect schema          │
  │  2. Write SQL query         │
  │  3. Execute against DB      │
  │  4. Interpret results       │
  │  5. Return natural language │
  └────────────────┘
       │
       ▼
    SQLite DB
```

---

## Extending This Project

- **Swap the DB** — change the SQLAlchemy URI to Postgres or MySQL with no other changes
- **Add auth** — protect the `/query` endpoint with JWT or API keys
- **Stream responses** — replace `agent.invoke()` with `.astream()` for token-by-token output
- **Multi-tenant** — pass a different DB path per user for isolated databases

---

## License

MIT
