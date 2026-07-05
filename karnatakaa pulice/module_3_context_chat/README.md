# Module 3 - Context-Aware Chat

This module stores previous investigator chat turns and resolves short follow-up
questions.

## Example

```text
User: Show murder cases.
AI: There are 126 cases.

User: Only in Mysore.
AI understands: Show murder cases in Mysuru.
```

## Memory Backends

- `memory` - in-process memory for demos
- `redis` - Redis-backed session memory

```bash
CHAT_MEMORY_BACKEND=redis
REDIS_URL=redis://localhost:6379/0
```

## Run API

From `karnatakaa pulice`:

```bash
uvicorn module_3_context_chat.api:app --reload --port 8001
```

Request:

```bash
curl -X POST http://127.0.0.1:8001/context-chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\":\"investigator-1\",\"question\":\"Only in Mysore.\"}"
```
