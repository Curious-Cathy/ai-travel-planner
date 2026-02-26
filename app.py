"""
============================================
🌍 AI-Powered Travel Planner — UI Layer
============================================
A Streamlit web app that generates personalized
day-wise travel itineraries using Groq API.

This file handles ONLY the user interface.
All AI/LLM logic lives in llm_handler.py.
PDF generation lives in utils/pdf_generator.py.

Author    : Your Name
Hackathon : Your Hackathon Name
Built with: Python, Streamlit, Groq API (LLaMA 3)
============================================
"""

# ── Imports ──────────────────────────────────────────────
import streamlit as st
import pandas as pd

# Import AI function and budget parser from our handler module
from llm_handler import generate_itinerary, parse_budget_table

# Import PDF generator
from utils.pdf_generator import generate_pdf

# ── Page configuration (must be the first Streamlit call) ─
st.set_page_config(
    page_title="AI Travel Planner ✈️",
    page_icon="🌍",
    layout="centered",
)


# ══════════════════════════════════════════════════════════
#  CUSTOM CSS — polished look & feel
# ══════════════════════════════════════════════════════════

st.markdown(
    """
    <style>
    /* ── Global font ─────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ── Hero header gradient ────────────────────────── */
    .hero-header {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    }
    .hero-header h1 {
        color: #ffffff;
        font-size: 2.4rem;
        margin: 0 0 0.3rem 0;
    }
    .hero-header p {
        color: #b0c4d8;
        font-size: 1.05rem;
        margin: 0;
    }

    /* ── Section divider ─────────────────────────────── */
    .section-divider {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #2C5364, transparent);
        margin: 1.8rem 0;
    }

    /* ── Itinerary card ──────────────────────────────── */
    .itinerary-card {
        background: #f9fbfd;
        border-left: 4px solid #2C5364;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    /* ── Budget highlight box ────────────────────────── */
    .budget-box {
        background: linear-gradient(135deg, #f0f4f8, #e8eef3);
        border: 1px solid #2C5364;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
    }

    /* ── Footer ──────────────────────────────────────── */
    .footer {
        text-align: center;
        color: #7a8b9a;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════
#  UI — HEADER
# ══════════════════════════════════════════════════════════

st.markdown(
    """
    <div class="hero-header">
        <h1>🌍 AI Travel Planner</h1>
        <p>Your personal AI-powered travel assistant — plan smarter, travel better.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════
#  UI — SIDEBAR (user inputs)
# ══════════════════════════════════════════════════════════

with st.sidebar:
    st.header("🗺️ Plan Your Trip")
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # --- Destination ---
    destination = st.text_input(
        "📍 Destination",
        placeholder="e.g. Tokyo, Japan",
        help="Enter the city or country you want to visit.",
    )

    # --- Number of days ---
    days = st.number_input(
        "📆 Number of Days",
        min_value=1,
        max_value=30,
        value=3,
        step=1,
        help="How many days will you be traveling?",
    )

    # --- Budget type ---
    budget = st.selectbox(
        "💰 Budget Type",
        options=["Low", "Medium", "High"],
        index=1,
        help="Select your overall budget level.",
    )

    # --- Travel style ---
    style = st.selectbox(
        "🧳 Travel Style",
        options=["Solo", "Couple", "Family", "Friends"],
        help="Who are you traveling with?",
    )

    # --- Interests (multiselect) ---
    interests = st.multiselect(
        "❤️ Interests",
        options=["Food", "Adventure", "Nature", "Shopping", "History", "Nightlife"],
        default=["Food", "Nature"],
        help="Pick the things you love — we'll tailor your plan.",
    )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # --- Generate button ---
    generate_btn = st.button("🚀 Generate My Travel Plan", use_container_width=True)


# ══════════════════════════════════════════════════════════
#  MAIN AREA — generate & display itinerary
# ══════════════════════════════════════════════════════════

if generate_btn:
    # ── Validate required input ──────────────────────────
    if not destination.strip():
        st.warning("⚠️ Please enter a destination to get started!")
    else:
        # ── Call the LLM handler with a loading spinner ──
        error_occurred = False
        with st.spinner("✨ Crafting your perfect itinerary — hang tight..."):
            try:
                itinerary = generate_itinerary(
                    destination=destination,
                    days=days,
                    budget=budget,
                    style=style,
                    interests=interests,
                )
            except RuntimeError as e:
                itinerary = None
                error_occurred = True
                st.error(f"❌ {e}")

        # ── Display results ──────────────────────────────
        if itinerary:
            st.success("🎉 Your travel plan is ready!")
            st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

            # ── Full itinerary in Markdown ───────────────
            st.markdown(itinerary)

            st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

            # ── Budget Summary Table (extracted) ─────────
            budget_data = parse_budget_table(itinerary)

            if budget_data:
                st.markdown("### 💰 Budget Summary")
                st.markdown(
                    "<div class='budget-box'>",
                    unsafe_allow_html=True,
                )

                # Convert to DataFrame for st.table()
                df = pd.DataFrame(budget_data)
                st.table(df)

                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

            # ── Download Buttons ─────────────────────────
            st.markdown("### 📥 Download Your Itinerary")
            col1, col2 = st.columns(2)

            # Download as TXT
            with col1:
                st.download_button(
                    label="📄 Download as TXT",
                    data=itinerary,
                    file_name=f"{destination.strip().replace(' ', '_')}_itinerary.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

            # Download as PDF
            with col2:
                try:
                    pdf_bytes = generate_pdf(itinerary, destination)
                    st.download_button(
                        label="📕 Download as PDF",
                        data=pdf_bytes,
                        file_name=f"{destination.strip().replace(' ', '_')}_itinerary.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"❌ PDF generation failed: {e}")

        elif itinerary is None and not error_occurred:
            # API key is missing — show setup instructions
            st.error(
                "⚠️ **Groq API key not found!**\n\n"
                "Please add your key to the `.env` file:\n"
                "```\nGROQ_API_KEY=gsk_...\n```\n\n"
                "Get a FREE key at: https://console.groq.com/keys"
            )

else:
    # ── Placeholder when no plan has been generated yet ──
    st.markdown(
        """
        ### 👈 Fill in your travel details in the sidebar and hit **Generate**!

        This AI planner will create a **personalized day-wise itinerary**
        including:
        - 📅 Day-by-day plan with morning / afternoon / evening activities
        - 🏛️ Must-visit attractions
        - 🍽️ Local food recommendations
        - 💰 Budget breakdown with summary table
        - 💡 Practical travel tips
        - 🎒 Packing suggestions for your destination
        - 📥 Download as **TXT** or **PDF**

        *Powered by Groq (LLaMA 3) · Built with Streamlit*
        """
    )


# ══════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════

st.markdown(
    """
    <div class="footer">
        Made with ❤️ for the Hackathon &nbsp;|&nbsp; Powered by Groq &amp; Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
