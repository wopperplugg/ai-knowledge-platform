import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://knowledge_ops:knowledge_ops@localhost:5432/knowledge_ops",
)
