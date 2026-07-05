# Module 2 - AI Chatbot

This module lets investigators ask crime database questions in natural language
instead of writing SQL.

## Flow

```text
Natural Language
        |
        v
Rule Planner or LLM
        |
        v
Safe SQL Query
        |
        v
Crime Database
        |
        v
Human-readable Answer
```

## Example

User:

```text
How many theft cases happened in Bangalore in June?
```

Generated SQL:

```sql
SELECT COUNT(*) AS total_cases
FROM crime_records
WHERE district = :district
AND crime_type = :crime_type
AND EXTRACT(MONTH FROM crime_date) = :month
AND EXTRACT(YEAR FROM crime_date) = :year
```

Answer:

```text
There were 248 matching crime cases for your question.
```

## Supported LLM Options

Set `AI_PROVIDER` to choose the backend:

- `none` - offline fallback plus rule-based planner
- `openai` - OpenAI API
- `gemini` - Gemini API
- `ollama` - local Ollama model

The rule-based planner already handles common questions like:

- burglary cases in Mysore during last 6 months
- theft cases in Bangalore in June
- robbery cases in Mysuru
- vehicle theft in Bengaluru

## Environment Variables

```bash
DATABASE_URL=postgresql+psycopg://scrb:scrb@localhost:5432/scrb
AI_PROVIDER=none
```

For OpenAI:

```bash
AI_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4.1-mini
```

For Gemini:

```bash
AI_PROVIDER=gemini
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-1.5-flash
```

For Ollama:

```bash
AI_PROVIDER=ollama
OLLAMA_MODEL=llama3.1
OLLAMA_URL=http://localhost:11434/api/generate
```

## Run Demo

From the `karnatakaa pulice` folder:

```bash
python -m module_2_ai_chatbot.demo "How many theft cases happened in Bangalore in June?"
```

## Run API

From the `karnatakaa pulice` folder:

```bash
uvicorn module_2_ai_chatbot.api:app --reload
```

Then call:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"Show burglary cases in Mysore during last 6 months.\"}"
```

## Security Controls

- Executes only `SELECT` queries.
- Blocks destructive SQL keywords.
- Requires queries to use the `crime_records` table.
- Adds a default `LIMIT` to non-aggregate queries.
- Uses SQLAlchemy parameter binding in the rule-based planner.
