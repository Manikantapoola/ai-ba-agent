# 📊 AI Business Analyst Agent

> Upload any sales CSV or Excel file and get instant AI-powered business insights, KPI analysis, and action recommendations — automatically.

🔗 **Live Demo:** [Click here to try it][https://ai-ba-agent-lfrsqffyjraxnejwocjq3l.streamlit.app]
---

## What It Does

1. You upload a CSV or Excel sales file
2. The agent **automatically cleans** the data (removes duplicates, fixes empty cells, parses dates)
3. It **computes KPIs** — revenue by region, monthly trends, top products
4. It sends the KPIs to **Claude AI** which acts as a Senior Business Analyst
5. You get an **executive summary, insights, risks, and recommendations** with interactive charts

## Example AI Output

> *"West region revenue dropped 38% in Q3-Q4 2024. Repeat customer revenue declined faster than new customer revenue, suggesting a retention problem. Recommend launching a customer loyalty programme targeting the West region immediately."*

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| pandas | Data cleaning and KPI computation |
| Anthropic Claude AI | Business insights generation |
| Streamlit | Web dashboard |
| Plotly | Interactive charts |
| SQLite | SQL-based KPI queries |

## How to Run Locally (Windows)

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/ai-ba-agent
cd ai-ba-agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file with:
```
ANTHROPIC_API_KEY=your-key-here
MODEL=claude-sonnet-4-5
```

Then run:
```
streamlit run app.py
```

## Project Structure

```
ai-ba-agent/
  src/
    config.py           # API key loader
    data_loader.py      # CSV/Excel reader
    data_cleaner.py     # Automated cleaning
    kpi_engine.py       # KPI computation
    prompt_builder.py   # AI prompt engineering
    ai_agent.py         # Claude API caller
  data/
    sample_sales.csv    # Test data
  app.py                # Streamlit dashboard
```

## Skills Demonstrated
Python · pandas · AI/LLM APIs · Prompt Engineering · Streamlit · Plotly · SQL · Data Cleaning · Business Analysis
