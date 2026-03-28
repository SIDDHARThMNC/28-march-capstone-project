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
#
# ============================================================
# Architecture:
#   User Query
#       └─> Classifier Agent
#               ├─> Billing Agent
#               ├─> Technical Support Agent
#               └─> General Agent
#                       └─> Response Agent (final output)
# ============================================================

from typing import Literal


# ── Agent 1: Classifier ───────────────────────────────────────

def classifier_agent(query: str) -> Literal["billing", "technical", "general"]:
    """Classifies the query into a department."""
    query_lower = query.lower()

    billing_keywords = ["charge", "payment", "refund", "invoice", "subscription", "bill", "price", "pricing", "plan"]
    technical_keywords = ["crash", "error", "bug", "not working", "issue", "app", "software", "install", "login", "slow"]

    if any(kw in query_lower for kw in billing_keywords):
        return "billing"
    elif any(kw in query_lower for kw in technical_keywords):
        return "technical"
    else:
        return "general"


# ── Agent 2: Billing ──────────────────────────────────────────

def billing_agent(query: str) -> dict:
    """Handles billing and payment related queries."""
    responses = {
        "double charge": "We're sorry for the inconvenience. A duplicate charge has been detected. Our team will process a full refund within 3-5 business days.",
        "refund": "Refund requests are processed within 5-7 business days. Please share your transaction ID for faster resolution.",
        "pricing": "We offer three plans: Basic ($9/mo), Pro ($29/mo), and Enterprise ($99/mo). All plans include a 14-day free trial.",
        "default": "Our billing team will review your account and respond within 24 hours. Please check your registered email for updates."
    }

    query_lower = query.lower()
    if "twice" in query_lower or "double" in query_lower or "charged twice" in query_lower:
        return {"department": "Billing", "response": responses["double charge"]}
    elif "refund" in query_lower:
        return {"department": "Billing", "response": responses["refund"]}
    elif "pricing" in query_lower or "plan" in query_lower:
        return {"department": "Billing", "response": responses["pricing"]}
    else:
        return {"department": "Billing", "response": responses["default"]}


# ── Agent 3: Technical Support ────────────────────────────────

def technical_support_agent(query: str) -> dict:
    """Handles technical and software related queries."""
    responses = {
        "crash": "We're aware of a crash issue on some devices. Please try: 1) Clear app cache, 2) Update to latest version (v3.2.1), 3) Restart your device. If the issue persists, contact support@app.com.",
        "login": "For login issues: 1) Reset your password via 'Forgot Password', 2) Clear browser cookies, 3) Try incognito mode. Still stuck? We'll escalate to our tech team.",
        "slow": "Performance issues can be resolved by: 1) Closing background apps, 2) Checking your internet speed, 3) Reinstalling the app.",
        "default": "Our technical team has logged your issue. You'll receive a resolution within 24-48 hours."
    }

    query_lower = query.lower()
    if "crash" in query_lower or "crashes" in query_lower:
        return {"department": "Technical Support", "response": responses["crash"]}
    elif "login" in query_lower:
        return {"department": "Technical Support", "response": responses["login"]}
    elif "slow" in query_lower:
        return {"department": "Technical Support", "response": responses["slow"]}
    else:
        return {"department": "Technical Support", "response": responses["default"]}


# ── Agent 4: General ──────────────────────────────────────────

def general_agent(query: str) -> dict:
    """Handles general queries."""
    responses = {
        "pricing": "Our plans start at $9/month. Visit our website at www.company.com/pricing for full details.",
        "hours": "Our support team is available Monday-Friday, 9 AM to 6 PM EST.",
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


# ── Agent 5: Response ─────────────────────────────────────────

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


# ── Orchestrator ──────────────────────────────────────────────

def support_system(query: str) -> str:
    """Main orchestrator that delegates to the right agent."""
    classification = classifier_agent(query)

    if classification == "billing":
        agent_output = billing_agent(query)
    elif classification == "technical":
        agent_output = technical_support_agent(query)
    else:
        agent_output = general_agent(query)

    return response_agent(query, classification, agent_output)


# ── Test Cases ────────────────────────────────────────────────

if __name__ == "__main__":
    test_queries = [
        "I was charged twice for my subscription",
        "The app crashes when I open it",
        "What are your pricing plans?"
    ]

    for query in test_queries:
        print(support_system(query))
