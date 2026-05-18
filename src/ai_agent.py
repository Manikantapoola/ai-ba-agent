import anthropic
import json
from src.config         import API_KEY, MODEL
from src.prompt_builder import SYSTEM_PROMPT, build_prompt

client = anthropic.Anthropic(api_key=API_KEY)

def run_analysis(kpis, clean_report):
    user_prompt = build_prompt(kpis, clean_report)
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}]
        )
        raw_text = response.content[0].text.strip()
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        return {"error": f"AI returned bad JSON: {e}"}
    except anthropic.AuthenticationError:
        return {"error": "Invalid API key. Check your .env file."}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}