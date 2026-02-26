"""
============================================
 LLM Handler — Groq API Integration
============================================
This module handles all AI/LLM logic for the
Travel Planner app. It keeps API configuration
and prompt engineering separate from the UI.

Model  : llama3-8b-8192
API    : Groq (OpenAI-compatible format)
============================================
"""

# ── Imports ──────────────────────────────────────────────
import os
from groq import Groq
from dotenv import load_dotenv

# ── Load environment variables from .env ─────────────────
# This reads GROQ_API_KEY from the .env file so we never
# hard-code secrets in our source code.
load_dotenv()

# ── Read the API key ─────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ── Model to use ─────────────────────────────────────────
MODEL_NAME = "llama-3.3-70b-versatile"


# ══════════════════════════════════════════════════════════
#  PROMPT BUILDER (private helper)
# ══════════════════════════════════════════════════════════

def _build_prompt(destination, days, budget, interests):
    """
    Build a detailed, structured prompt that tells the LLM
    exactly what kind of travel itinerary to generate.

    Args:
        destination (str) : City or country to visit.
        days        (int) : Number of travel days.
        budget      (str) : Budget level — "Low", "Medium", or "High".
        interests   (list): List of interest tags, e.g. ["Food", "Nature"].

    Returns:
        str : The fully formatted prompt string.
    """
    # Convert the interests list into a readable string
    interests_str = ", ".join(interests) if interests else "General sightseeing"

    prompt = f"""
You are an expert travel planner. Create a detailed {days}-day travel itinerary
for {destination} with the following preferences:

- Budget Level : {budget}
- Interests    : {interests_str}

IMPORTANT: Use **Markdown tables** wherever possible to make the plan look
professional and easy to scan. Follow this exact structure:

---

## 📋 Trip Overview

| Detail        | Info              |
|---------------|-------------------|
| Destination   | {destination}     |
| Duration      | {days} day(s)     |
| Budget        | {budget}          |
| Interests     | {interests_str}   |

---

## 📅 Day-wise Itinerary

For **each day**, create a section heading (e.g. "### Day 1 — Title") and
then a table like this:

| Time of Day | Activity | Place / Location | Duration |
|-------------|----------|------------------|----------|
| 🌅 Morning  | ...      | ...              | ...      |
| 🌞 Afternoon| ...      | ...              | ...      |
| 🌙 Evening  | ...      | ...              | ...      |

Include 2-3 activities per time slot. Be specific with real place names.

---

## 🏛️ Top Attractions

Present as a table:

| # | Attraction | Description | Estimated Entry Fee |
|---|-----------|-------------|---------------------|
| 1 | ...       | ...         | ...                 |

List at least 6-8 attractions.

---

## 🍽️ Food Recommendations

Present as a table:

| Dish / Cuisine | Restaurant / Area | Price Range | Must-Try? |
|---------------|-------------------|-------------|-----------|
| ...           | ...               | ...         | ⭐ Yes / No|

Include at least 5-6 recommendations with local specialties.

---

## 💰 Budget Breakdown

Present the estimated daily costs as a table:

| Category          | Estimated Daily Cost | {days}-Day Total |
|-------------------|---------------------|------------------|
| 🏨 Accommodation  | ...                 | ...              |
| 🍽️ Food & Drinks  | ...                 | ...              |
| 🚗 Transportation | ...                 | ...              |
| 🎟️ Activities     | ...                 | ...              |
| 🛍️ Shopping/Misc  | ...                 | ...              |
| **💵 TOTAL**      | **...**             | **...**          |

---

## 💡 Travel Tips

Present as a numbered table:

| # | Category    | Tip |
|---|------------|-----|
| 1 | 🛡️ Safety  | ... |
| 2 | 🧳 Packing | ... |
| 3 | 🚌 Transport| ... |
| 4 | 🌤️ Weather | ... |
| 5 | 🗣️ Customs | ... |

Include 5-7 practical, actionable tips.

---

Format everything in clean, well-structured Markdown with proper headings
and tables. Be specific, actionable, and use real place names.
"""
    return prompt


# ══════════════════════════════════════════════════════════
#  MAIN FUNCTION — called by app.py
# ══════════════════════════════════════════════════════════

def generate_itinerary(destination, days, budget, interests):
    """
    Generate a travel itinerary using Groq API (LLaMA 3).

    This is the ONLY function the UI layer (app.py) needs to call.
    It handles prompt creation, API communication, and returns
    the generated itinerary text.

    Args:
        destination (str) : City or country to visit.
        days        (int) : Number of travel days.
        budget      (str) : Budget level — "Low", "Medium", or "High".
        interests   (list): List of interest tags.

    Returns:
        str  : The generated itinerary in Markdown format.
        None : If the API key is missing.

    Raises:
        RuntimeError : If the Groq API call fails.
    """
    # ── Guard: make sure the API key is set ──────────────
    if not GROQ_API_KEY or GROQ_API_KEY == "your-groq-api-key-here":
        return None  # app.py will show an appropriate error message

    # ── Build the prompt ─────────────────────────────────
    prompt = _build_prompt(destination, days, budget, interests)

    # ── Call Groq API ────────────────────────────────────
    try:
        # Create the Groq client with the API key
        client = Groq(api_key=GROQ_API_KEY)

        # Use the chat completions endpoint (OpenAI-compatible)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful and knowledgeable travel planning "
                        "assistant. You provide detailed, practical, and well-"
                        "organized travel itineraries."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.7,   # slight creativity
            max_tokens=4096,   # enough for detailed tables
        )

        # Extract and return the assistant's reply text
        return response.choices[0].message.content

    except Exception as e:
        # Raise so app.py can catch and display the error
        raise RuntimeError(f"Groq API error: {e}")
