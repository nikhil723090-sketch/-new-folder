# Module 4 - Voice Support

This module adds voice input and spoken output.

## Flow

```text
Microphone / Audio File
        |
        v
Speech-to-Text
        |
        v
Context-Aware Chatbot
        |
        v
Text-to-Speech
        |
        v
Audio Answer
```

## Supported Providers

Speech-to-text:

- Whisper
- Google Speech-to-Text
- Azure Speech

Text-to-speech:

- gTTS
- Azure neural voices

Kannada can be used with `kn` or `kn-IN`, depending on the provider.

## Environment

```bash
STT_PROVIDER=whisper
WHISPER_MODEL=small
TTS_PROVIDER=gtts
```

For Azure:

```bash
STT_PROVIDER=azure
TTS_PROVIDER=azure
AZURE_SPEECH_KEY=your_key
AZURE_SPEECH_REGION=centralindia
AZURE_TTS_VOICE=kn-IN-SapnaNeural
```

For Google STT, configure Google Cloud credentials and use:

```bash
STT_PROVIDER=google
```

## Run API

From `karnatakaa pulice`:

```bash
uvicorn module_4_voice_support.api:app --reload --port 8002
```

Example:

```bash
curl -X POST http://127.0.0.1:8002/voice-chat \
  -F "session_id=investigator-1" \
  -F "language=kn" \
  -F "audio=@question.wav"
```
