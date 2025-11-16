import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH

load_dotenv()
MODEL = os.getenv("GENAI_MODEL", "gemini-2.0-flash")

pizza = RemoteA2aAgent(
    name="pizza_seller",
    description="Remote pizza seller via A2A.",
    agent_card=f"http://127.0.0.1:11000{AGENT_CARD_WELL_KNOWN_PATH}",
)

burger = RemoteA2aAgent(
    name="burger_seller",
    description="Remote burger seller via A2A.",
    agent_card=f"http://127.0.0.1:11001{AGENT_CARD_WELL_KNOWN_PATH}",
)

SYSTEM_PROMPT = (
    "You are a Purchasing Concierge that helps users order food.\n"
    "- If the user mentions pizza terms, use pizza_seller.\n"
    "- If burger terms, use burger_seller.\n"
    "- When unclear, ask one clarifying question OR propose both menus with cheapest picks.\n"
    "- Always call seller tools (list_menu, quote, place_order) rather than guessing prices.\n"
    "- For an order: confirm item, size, qty, address, price, ETA. Provide a brief receipt.\n"
    "After calling tools or sub-agents, ALWAYS produce a short final answer."
)

root_agent = LlmAgent(
    model=MODEL,
    name="purchasing_concierge",
    description="Concierge that orchestrates orders between pizza & burger sellers via A2A.",
    instruction=SYSTEM_PROMPT,
    sub_agents=[pizza, burger],
)
