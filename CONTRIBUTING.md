# Contributing

Thank you for contributing to Water Tracker. This project is a hackathon demo, but changes should still be reviewed with the same care as production-facing code.

## Local checks

Install the development dependencies and Git hooks before committing:

```bash
uv sync --dev
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

Run all configured checks manually with:

```bash
uv run pre-commit run --all-files
uv run pre-commit run --hook-stage pre-push --all-files
```

## Expectations

- Keep formatting and linting clean.
- Add or update tests for behavioral changes.
- Do not commit secrets, credentials, private data, or generated local databases.
- Keep dependency changes intentional and auditable.
- Update documentation when setup, behavior, or operations change.

## Offline Work Guidelines

All internship work should be designed to function without WiFi dependency. Internet connectivity should not block development or testing.

### Local AI Tools

When AI assistance is needed, use local inferencing tools that work offline:

- **Ollama** - Run LLMs locally (Llama, Mistral, CodeLlama, etc.)
- **LM Studio** - User-friendly interface for local LLMs
- **llama.cpp** - Lightweight LLM inference
- **GPT4All** - Desktop application for local AI
- **Code Llama** - Specialized for code generation

### Offline Development Practices

- Download all required documentation and dependencies before disconnecting
- Use local package caches (`pip cache`, `npm cache`)
- Maintain local copies of API documentation
- Test applications in offline mode before deployment
- Use local databases or SQLite for development when possible
