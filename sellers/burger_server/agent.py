from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
import uuid
import re

MENU = {
    "classic":  {"S": 6.0, "M": 7.5, "L": 9.0},
    "cheese":   {"S": 7.0, "M": 8.5, "L": 10.0},
    "double":   {"S": 8.5, "M": 10.0, "L": 12.0},
}

ALIASES = {
    "cheeseburger": "cheese",
    "cheese burger": "cheese",
    "cheese burgers": "cheese",
    "classic burger": "classic",
    "double burger": "double",
}

SIZE_MAP = {"s": "S", "small": "S", "m": "M", "med": "M", "medium": "M", "l": "L", "large": "L"}

def _canon_item(name: str) -> str | None:
    t = name.strip().lower()
    t = re.sub(r"\s+burger(s)?$", "", t)  # strip trailing “burger(s)”
    t = ALIASES.get(t, t)
    return t if t in MENU else None

def _canon_size(size: str) -> str | None:
    s = size.strip().lower()
    s = SIZE_MAP.get(s, s.upper())
    return s if s in ("S", "M", "L") else None

def list_menu() -> dict:
    return MENU

def quote(item: str, size: str = "M", qty: int = 1):
    i = _canon_item(item)
    s = _canon_size(size)
    if not i or not s:
        return {"error": "unknown item/size", "allowed_items": list(MENU.keys()), "sizes": ["S","M","L"]}
    total = round(MENU[i][s] * max(1, int(qty)), 2)
    return {"item": i, "size": s, "qty": int(qty), "total": total}

def place_order(item: str, size: str = "M", qty: int = 1, address: str = "pickup"):
    q = quote(item, size, qty)
    if isinstance(q, dict) and q.get("error"):
        return q
    order_id = f"burger-{uuid.uuid4().hex[:8]}"
    eta_min = 12 if str(address).strip().lower() == "pickup" else 22
    return {"order_id": order_id, "vendor": "BurgerCo", **q, "eta_min": eta_min, "address": address}

root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="burger_seller",
    description="Burger seller (A2A) with menu, quote, and order tools.",
    instruction=(
        "Use tools; never guess prices. Always call quote/place_order. "
        "If a tool returns {error: ...}, apologize and ask the user to pick from allowed_items/sizes. "
        "After using tools, ALWAYS produce a short, plain-text answer summarizing the result."
    ),
    tools=[list_menu, quote, place_order],
)

a2a_app = to_a2a(root_agent, port=11001)
