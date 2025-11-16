from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
import uuid

MENU = {
    "margherita": {"S": 8.0, "M": 10.0, "L": 12.0},
    "pepperoni":  {"S": 9.0, "M": 11.0, "L": 13.0},
    "veggie":     {"S": 9.0, "M": 11.0, "L": 13.0},
}

def list_menu() -> dict:
    return MENU

def quote(item: str, size: str = "M", qty: int = 1) -> float:
    i, s = item.lower(), size.upper()
    if i not in MENU or s not in MENU[i]:
        raise ValueError("unknown item/size")
    return round(MENU[i][s] * max(1, int(qty)), 2)

def place_order(item: str, size: str = "M", qty: int = 1, address: str = "pickup") -> dict:
    total = quote(item, size, qty)
    order_id = f"pizza-{uuid.uuid4().hex[:8]}"
    eta_min = 20 if address.lower() == "pickup" else 30
    return {
        "order_id": order_id, "vendor": "PizzaCo",
        "item": item, "size": size.upper(), "qty": qty,
        "total": total, "eta_min": eta_min
    }

root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="pizza_seller",
    description="Pizza seller (A2A) with menu, quote, and order tools.",
    instruction="Use tools; never guess prices. Always call quote/place_order. After using tools, ALWAYS produce a short, plain-text answer summarizing the result.",
    tools=[list_menu, quote, place_order],
)

a2a_app = to_a2a(root_agent, port=11000)
