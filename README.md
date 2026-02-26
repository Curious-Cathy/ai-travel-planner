# 🌍 AI-Powered Travel Planner

An AI-powered travel itinerary generator built with **Python**, **Streamlit**, and **Groq API (LLaMA 3)**. Enter your destination, preferences, and budget — get a complete day-wise travel plan in seconds.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3-orange?logo=meta)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📅 Day-wise Itinerary | Morning, afternoon & evening activities for each day |
| 🏛️ Attractions | Top must-visit places with descriptions |
| 🍽️ Food Recommendations | Local dishes & restaurant suggestions |
| 💰 Budget Breakdown | Estimated costs for accommodation, food, transport & more |
| 💡 Travel Tips | Safety, customs, packing & transport advice |
| 📥 Download | Save your itinerary as a `.txt` file |
| 🎨 Custom UI | Polished interface with gradient hero header, styled cards & Google Fonts |

---

## 🛠️ Tech Stack

- **Frontend** — [Streamlit](https://streamlit.io/)
- **LLM** — [Groq API](https://console.groq.com/) (LLaMA 3 · `llama3-8b-8192`)
- **Config** — [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 📂 Project Structure

```
ai-travel-planner/
├── app.py              # Streamlit UI (frontend only)
├── llm_handler.py      # Groq API integration (AI logic only)
├── requirements.txt    # Python dependencies
├── .env                # API key (git-ignored)
├── .gitignore          # Files excluded from version control
└── README.md           # This file
```

> **Architecture**: The project follows a clean separation of concerns —
> `app.py` handles the UI, while `llm_handler.py` handles all AI/prompt logic.

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-travel-planner.git
cd ai-travel-planner
```

### 2. Create & activate a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key

Open the `.env` file and replace the placeholder:

```
GROQ_API_KEY=gsk_your-actual-api-key
```

> 🔑 Get a **FREE** API key at [console.groq.com/keys](https://console.groq.com/keys)

### 5. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at **http://localhost:8501**.

---

## 📸 Usage

1. Open the sidebar and enter your **destination** (e.g. _Tokyo, Japan_).
2. Set the **number of days** (1–30), **budget level** (Low / Medium / High), and **interests** (Food, Adventure, Nature, etc.).
3. Click **🚀 Generate My Travel Plan**.
4. View the beautifully formatted itinerary with day-by-day plans, attractions, food tips, budget breakdown, and travel tips.
5. Optionally **📥 download** the itinerary as a `.txt` file.

---

## 🗂️ Git Commit Suggestions

Use these step-by-step commits for a clean Git history:

```bash
# 1 — Initial project setup
git init
git add requirements.txt .gitignore .env
git commit -m "chore: initial project setup with dependencies and config"

# 2 — AI logic module
git add llm_handler.py
git commit -m "feat: add Groq-powered itinerary generator module"

# 3 — Streamlit UI
git add app.py
git commit -m "feat: add Streamlit UI with sidebar inputs and download"

# 4 — Documentation
git add README.md
git commit -m "docs: add project README with setup instructions"

# 5 — (Optional) Push to GitHub
git remote add origin https://github.com/your-username/ai-travel-planner.git
git branch -M main
git push -u origin main
```

---

## 📝 License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

---

> Built with ❤️ for the Hackathon — Powered by Groq & Streamlit
