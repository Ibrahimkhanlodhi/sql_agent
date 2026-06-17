from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_groq import ChatGroq
from langchain.agents.agent_types import AgentType
from langchain_core.callbacks import BaseCallbackHandler
import re
import os

DB_PATH = "ecommerce.db"


class SQLCaptureHandler(BaseCallbackHandler):
    """Captures the SQL queries the agent generates."""

    def __init__(self):
        self.queries = []

    def on_tool_end(self, output: str, **kwargs):
        # LangChain SQL tools return raw query results; we capture the input
        pass

    def on_agent_action(self, action, **kwargs):
        if action.tool == "sql_db_query":
            sql = action.tool_input.strip()
            if sql and sql not in self.queries:
                self.queries.append(sql)


def build_agent():
    """Build and return the SQL agent."""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv(
            "GROK_API_KEY"),
    )

    db = SQLDatabase.from_uri(
        f"sqlite:///{DB_PATH}",
        include_tables=["customers", "products", "orders", "order_items"],
        sample_rows_in_table_info=3,
    )

    agent = create_sql_agent(
        llm=llm,
        db=db,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=20,
        max_execution_time=60,
    )

    return agent, db


def run_query(question: str) -> dict:
    """
    Run a natural language question against the database.
    Returns answer + the SQL queries that were generated.
    """
    handler = SQLCaptureHandler()
    agent, db = build_agent()

    try:
        result = agent.invoke(
            {"input": question},
            config={"callbacks": [handler]},
        )
        answer = result.get("output", "No answer generated.")
    except Exception as e:
        answer = f"Error: {str(e)}"

    # Fallback: extract SQL from verbose logs via the DB object
    queries = handler.queries if handler.queries else []

    return {
        "answer": answer,
        "sql_queries": queries,
    }
