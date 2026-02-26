"""
============================================
LLM Handler — Groq API Integration
============================================
This module handles all AI/LLM logic for the
Travel Planner app. It keeps API configuration
and prompt engineering separate from the UI.

Model  : llama-3.3-70b-versatile
API    : Groq (OpenAI-compatible format)
============================================
"""

# ── Imports ──────────────────────────────────────────────
import os
import re
from groq import Groq
from dotenv import load_dotenv

# ── Load environment variables from .env ─────────────────
load_dotenv()

# ── Read the API key ─────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ── Model to use ─────────────────────────────────────────
MODEL_NAME = "llama-3.3-70b-versatile"

# ── Strong system prompt for professional output ─────────
SYSTEM_PROMPT = (
    "You are a professional travel planning AI assistant. "
    "You create detailed, practical, and well-organized travel itineraries. "
    "Always structure your responses clearly using Markdown headings, "
    "bullet points, and tables. Be specific with real place names, "
    "prices, and actionable advice. "
    "Never use placeholder text — always provide real recommendations."
)


# ══════════════════════════════════════════════════════════
#  PROMPT BUILDER (private helper)
# ══════════════════════════════════════════════════════════

def _build_prompt(destination, days, budget, style, interests):
    """
    Build a detailed, structured prompt that instructs the LLM
    to generate a professional travel itinerary with tables,
    budget breakdown, and packing suggestions.

    Args:
        destination (str) : City or country to visit.
        days        (int) : Number of travel days.
        budget      (str) : Budget level — "Low", "Medium", or "High".
        style       (str) : Travel style — "Solo", "Couple", "Family", or "Friends".
        interests   (list): List of interest tags, e.g. ["Food", "Nature"].

    Returns:
        str : The fully formatted prompt string.
    """
    interests_str = ", ".join(interests) if interests else "General sightseeing"

    prompt = f"""
Create a detailed {days}-day travel itinerary for **{destination}** with these preferences:

- **Budget Level**: {budget}
- **Travel Style**: {style}
- **Interests**: {interests_str}

IMPORTANT: Use **Markdown tables** wherever possible. Follow this EXACT structure:

---

## 📋 Trip Overview

| Detail        | Info              |
|---------------|-------------------|
| Destination   | {destination}     |
| Duration      | {days} day(s)     |
| Budget        | {budget}          |
| Travel Style  | {style}           |
| Interests     | {interests_str}   |

---

## 📅 Day-wise Itinerary

For **each day**, create a heading (### Day 1 — Title) and a table:

| Time of Day  | Activity | Place / Location | Duration |
|-------------|----------|------------------|----------|
| 🌅 Morning  | ...      | ...              | ...      |
| 🌞 Afternoon | ...     | ...              | ...      |
| 🌙 Evening  | ...      | ...              | ...      |

Include 2-3 activities per time slot with real place names.

---

## 🏛️ Top Attractions

| # | Attraction | Description | Entry Fee |
|---|-----------|-------------|-----------|
| 1 | ...       | ...         | ...       |

List at least 6-8 real attractions.

---

## 🍽️ Food Recommendations

| Dish / Cuisine | Restaurant / Area | Price Range | Must-Try? |
|---------------|-------------------|-------------|-----------|
| ...           | ...               | ...         | ⭐ Yes / No |

Include 5-6 local specialties.

---

## 💰 Budget Breakdown

IMPORTANT: Show costs in **BOTH the local currency of {destination} AND Indian Rupees (₹)**.
Format: `Local Amount (₹ INR Amount)` — e.g. `¥5,000 (₹3,400)` or `€50 (₹4,600)`
If the destination is in India, just use ₹.

| Category          | Estimated Daily Cost | {days}-Day Total |
|-------------------|---------------------|------------------|
| 🏨 Accommodation  | ...                 | ...              |
| 🍽️ Food & Drinks  | ...                 | ...              |
| 🚗 Transportation | ...                 | ...              |
| 🎟️ Activities     | ...                 | ...              |
| 🛍️ Miscellaneous  | ...                 | ...              |
| **💵 TOTAL**      | **...**             | **...**          |

Use realistic amounts. DO NOT use placeholders — give real estimates.

---

## 💡 Travel Tips

| # | Category     | Tip |
|---|-------------|-----|
| 1 | 🛡️ Safety   | ... |
| 2 | 🧳 Packing  | ... |
| 3 | 🚌 Transport | ... |
| 4 | 🌤️ Weather  | ... |
| 5 | 🗣️ Language  | ... |
| 6 | 💳 Money     | ... |
| 7 | 📱 Apps      | ... |

---

## 🎒 Packing Suggestions

Based on {destination} for {days} days with a {budget} budget, suggest what to pack.
Organize into categories:

| Category       | Items |
|---------------|-------|
| 👕 Clothing    | ... (list 4-5 items, weather-appropriate) |
| 👟 Footwear    | ... (list 2-3 items based on activities) |
| 🧴 Toiletries  | ... (list 3-4 essentials) |
| 📱 Electronics | ... (list 3-4 items) |
| 📄 Documents   | ... (list 3-4 items) |
| 🎒 Extras      | ... (list 3-4 useful items) |

Be specific to {destination}'s climate, culture, and the planned activities.

---

Format everything in clean Markdown with proper headings and tables.
Be specific, actionable, and use real place names and prices.
"""
    return prompt


# ══════════════════════════════════════════════════════════
#  BUDGET PARSER — extract budget table for st.table()
# ══════════════════════════════════════════════════════════

def parse_budget_table(itinerary_text):
    """
    Extract budget data from the generated itinerary text
    and return it as a list of dictionaries for st.table().

    Looks for the Budget Breakdown section and parses the
    markdown table rows into structured data.

    Args:
        itinerary_text (str): The full itinerary markdown text.

    Returns:
        list[dict]: Budget items with Category, Daily Cost, and Total.
                    Returns empty list if parsing fails.
    """
    budget_data = []

    try:
        # Find the Budget Breakdown section
        budget_match = re.search(
            r"##\s*💰\s*Budget Breakdown(.*?)(?=\n##\s|\Z)",
            itinerary_text,
            re.DOTALL | re.IGNORECASE,
        )

        if not budget_match:
            return budget_data

        budget_section = budget_match.group(1)

        # Parse each table row (skip header and separator rows)
        # Match rows like: | 🏨 Accommodation | $50 | $150 |
        row_pattern = re.compile(
            r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|"
        )

        for match in row_pattern.finditer(budget_section):
            category = match.group(1).strip()
            daily_cost = match.group(2).strip()
            total_cost = match.group(3).strip()

            # Skip header row, separator rows, and empty rows
            if (
                "---" in category
                or "Category" in category
                or "Estimated" in daily_cost
                or not category
            ):
                continue

            budget_data.append({
                "Category": category,
                "Daily Cost": daily_cost,
                "Total": total_cost,
            })

    except Exception:
        # If parsing fails, return empty — app.py will skip the table
        pass

    return budget_data


# ══════════════════════════════════════════════════════════
#  MAIN FUNCTION — called by app.py
# ══════════════════════════════════════════════════════════

def generate_itinerary(destination, days, budget, style, interests):
    """
    Generate a travel itinerary using Groq API (LLaMA 3).

    This is the ONLY function the UI layer (app.py) needs to call.
    It handles prompt creation, API communication, and returns
    the generated itinerary text.

    Args:
        destination (str) : City or country to visit.
        days        (int) : Number of travel days.
        budget      (str) : Budget level — "Low", "Medium", or "High".
        style       (str) : Travel style — "Solo", "Couple", "Family", or "Friends".
        interests   (list): List of interest tags.

    Returns:
        str  : The generated itinerary in Markdown format.
        None : If the API key is missing.

    Raises:
        RuntimeError : If the Groq API call fails.
    """
    # ── Guard: make sure the API key is set ──────────────
    if not GROQ_API_KEY or GROQ_API_KEY == "your-groq-api-key-here":
        return None

    # ── Build the prompt ─────────────────────────────────
    prompt = _build_prompt(destination, days, budget, style, interests)

    # ── Call Groq API ────────────────────────────────────
    try:
        client = Groq(api_key=GROQ_API_KEY)

        # System + User message format for best results
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.7,
            max_tokens=4096,
        )

        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"Groq API error: {e}")
