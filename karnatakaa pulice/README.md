# Karnatakaa Pulice - SCRB Conversational AI Platform

This folder contains the SCRB platform modules requested for the Karnataka
police crime intelligence system.

## Completed Modules

- `module_2_ai_chatbot/` - Natural-language chatbot that converts investigator
  questions into safe SQL queries and returns human-readable answers.
- `module_3_context_chat/` - Conversation memory for follow-up questions such
  as "Only in Mysore."
- `module_4_voice_support/` - Speech-to-text and text-to-speech pipeline with
  Kannada-capable providers.
- `module_5_crime_pattern_detection/` - Pandas analytics for peak hours,
  seasons, districts, repeat offenders, repeat locations, and visual reports.

## Existing Dependency

Module 2 connects to the crime database module in:

```text
../crime_database/
```

The chatbot expects the `crime_records` table created by Module 1.
