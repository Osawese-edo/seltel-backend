from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..config import get_settings

settings = get_settings()

raw_url = settings.DATABASE_URL

# Auto-add asyncpg driver if missing (Supabase gives postgresql:// without +asyncpg)
if raw_url.startswith("postgresql://") and "+asyncpg" not in raw_url:
    raw_url = raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Auto-add SSL and pooler-compat params for remote databases
if "localhost" not in raw_url:
    # asyncpg uses 'ssl' not 'sslmode' — convert if present
    raw_url = raw_url.replace("sslmode=require", "ssl=require")
    raw_url = raw_url.replace("sslmode=disable", "ssl=disable")

    separator = "&" if "?" in raw_url else "?"
    if "ssl=" not in raw_url:
        raw_url += f"{separator}ssl=require"
        separator = "&"
    if "prepared_statement_cache_size" not in raw_url:
        raw_url += f"{separator}prepared_statement_cache_size=0"

engine = create_async_engine(raw_url, echo=settings.DEBUG)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        yield session
