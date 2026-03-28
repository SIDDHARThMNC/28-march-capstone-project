# ============================================================
#
# Scenario 1: AI Customer Support Multi-Agent System
#
# Objective:
#   Build a multi-agent customer support system that can
#   classify, delegate, and resolve user queries.
#
# Problem Statement:
#   A company wants to automate its support system using AI
#   agents. The system should:
#     - Understand customer queries
#     - Route them to the correct department
#     - Provide responses
#
# Agents to Build:
#   1. Classifier Agent
#      - Identifies query type (Billing / Technical / General)
#   2. Billing Agent
#      - Handles payment/refund queries
#   3. Technical Support Agent
#      - Handles app/software issues
#   4. Response Agent
#      - Combines outputs into a final response
#
# Tasks to Implement:
#   - Multi-agent architecture (at least 3 agents mandatory)
#   - Task delegation logic
#   - Basic agent communication (message passing / function calls)
#
# Sample Inputs:
#   - "I was charged twice for my subscription"
#   - "The app crashes when I open it"
#   - "What are your pricing plans?"
#
# Expected Output:
#   - Correct classification of query
#   - Delegation to appropriate agent
#   - Final structured response
#
# Tools Used: Python (basic functions)

import random
import string
from typing import Literal, TypedDict

# ── Shared Message State ──────────────────────────────────────

class SupportTicket(TypedDict):
    query: str
    category: str
    department: str
    priority: str
    ticket_id: str
    response: str
    follow_up: str

def generate_ticket_id() -> str:
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"TKT-{suffix}"


# ====================================
    query_lower = query.lower()
    if "crash" in query_lower or "crashes" in query_lower:
        return {"department": "Technical Support", "response": responses["crash"]}
    elif "login" in query_lower:
        return {"department": "Technical Support", "response": responses["login"]}
    elif "slow" in query_lower:
        return {"department": "Technical Support", "response": responses["slow"]}
    else:
        return {"department": "Technical Support", "response": responses["default"]}


def general_agent(query: str) -> dict:
    """Handles general queries."""
    responses = {
        "pricing": "Our plans start at $9/month. Visit our website at www.company.com/pricing for full details.",
        "hours": "Our support team is available Monday–Friday, 9 AM to 6 PM EST.",
        "contact": "You can reach us at support@company.com or call 1-800-COMPANY.",
        "default": "Thank you for reaching out! Our team will get back to you within 24 hours with a detailed response."
    }

    query_lower = query.lower()
    if "pricing" in query_lower or "plan" in query_lower or "cost" in query_lower:
        return {"department": "General", "response": responses["pricing"]}
    elif "hour" in query_lower or "available" in query_lower or "timing" in query_lower:
        return {"department": "General", "response": responses["hours"]}
    elif "contact" in query_lower or "email" in query_lower or "phone" in query_lower:
        return {"department": "General", "response": responses["contact"]}
    else:
        return {"department": "General", "response": responses["default"]}


def response_agent(query: str, classification: str, agent_output: dict) -> str:
    """Combines all outputs into a final structured response."""
    return (
        f"\n{'='*55}\n"
        f"  CUSTOMER SUPPORT RESPONSE\n"
        f"{'='*55}\n"
        f"  Query     : {query}\n"
        f"  Department: {agent_output['department']}\n"
        f"  Category  : {classification.upper()}\n"
        f"{'─'*55}\n"
        f"  Response  :\n  {agent_output['response']}\n"
        f"{'='*55}\n"
    )


# ── Orchestrator ─────────────────────────────────────────────

def support_system(query: str) -> str:
    """Main orchestrator that delegates to the right agent."""
    # Step 1: Classify
    classification = classifier_agent(query)

    # Step 2: Delegate
    if classification == "billing":
        agent_output = billing_agent(query)
    elif classification == "technical":
        agent_output = technical_support_agent(query)
    else:
        agent_output = general_agent(query)

    # Step 3: Format final response
    return response_agent(query, classification, agent_output)


# ── Test Cases ───────────────────────────────────────────────

if __name__ == "__main__":
    test_queries = [
        "I was charged twice for my subscription",
        "The app crashes when I open it",
        "What are your pricing plans?"
    ]

    for query in test_queries:
        print(support_system(query))
