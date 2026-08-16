# KnowledgeOps AI

Backend foundation for an enterprise knowledge platform focused on knowledge operations,
document processing, RAG, and AI agent workflows.

## Current Scope

- FastAPI backend foundation
- PostgreSQL
- async SQLAlchemy
- health checks
- Docker
- tests

## Run Locally

```bash
cp .env.example .env
docker compose up --build
```

## Check Health

```bash
curl http://localhost:8000/health/live
curl http://localhost:8000/health/ready
```

## Development

```bash
pytest
ruff check .
ruff format --check .
mypy src
```

## Planned

- organizations
- documents
- LangChain
- LlamaIndex
- RAG
- LangGraph agents
- Qdrant
- Redis
