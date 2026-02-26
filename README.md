# 🌍 AI-Powered Travel Planner

An AI-powered travel itinerary generator built with **Python**, **Streamlit**, and **Groq API (LLaMA 3)**. Enter your destination, preferences, and budget — get a complete, professionally formatted travel plan with structured tables, budget breakdown, packing suggestions, and downloadable PDF.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3-orange?logo=meta)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📋 Trip Overview | Summary table with destination, duration, budget & interests |
| 📅 Day-wise Itinerary | Structured tables with morning, afternoon & evening activities |
| 🏛️ Top Attractions | Must-visit places with descriptions & entry fees |
| 🍽️ Food Recommendations | Local dishes, restaurants & price ranges |
| 💰 Budget Breakdown | Detailed cost table + extracted summary via `st.table()` |
| 💡 Travel Tips | Categorized practical tips in table format |
| 🎒 Packing Suggestions | Dynamic packing list based on destination & duration |
| 📄 Download TXT | Save your itinerary as a plain text file |
| 📕 Download PDF | Professional PDF with styled tables & branded layout |
| 🎨 Custom UI | Gradient hero header, styled cards & Google Fonts |

---

## 🛠️ Tech Stack

- **Frontend** — [Streamlit](https://streamlit.io/)
- **LLM** — [Groq API](https://console.groq.com/) (LLaMA 3.3 70B Versatile)
- **PDF** — [ReportLab](https://pypi.org/project/reportlab/)
- **Data** — [Pandas](https://pandas.pydata.org/) (Budget table display)
- **Config** — [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 📂 Project Structure

```
ai-travel-planner/
├── app.py                  # Streamlit UI (frontend only)
├── llm_handler.py          # Groq API integration (AI logic only)
├── utils/
│   ├── __init__.py         # Package init
│   └── pdf_generator.py    # PDF generation with ReportLab
├── requirements.txt        # Python dependencies
├── .env                    # API key (git-ignored)
├── .gitignore              # Files excluded from version control
└── README.md               # This file
```

> **Architecture**: Clean separation of concerns —
> `app.py` (UI) → `llm_handler.py` (AI) → `utils/pdf_generator.py` (PDF)

---

## ⚙️ How It Works

```
┌──────────────────────┐
│   User enters trip   │
│   details in sidebar │
│   (Streamlit UI)     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  llm_handler.py      │
│  • Builds prompt     │
│  • Calls Groq API    │
│  • Parses budget     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Groq API (LLaMA 3)  │
│  Returns structured  │
│  Markdown itinerary  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  app.py displays:    │
│  • Formatted plan    │
│  • Budget table      │
│  • Download buttons  │
│    (TXT + PDF)       │
└──────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Curious-Cathy/ai-travel-planner.git
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

Create a `.env` file in the project root and add your key:

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
4. View the professionally formatted itinerary with structured tables.
5. Review the **💰 Budget Summary** table extracted below the itinerary.
6. Download your plan as **📄 TXT** or **📕 PDF**.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "feat: add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📝 License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

---

> Built with ❤️ for the Hackathon — Powered by Groq & Streamlit
