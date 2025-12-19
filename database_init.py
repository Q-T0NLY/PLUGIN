"""
Database initialization and schema setup for Hyper Registry
"""
import asyncio
import os
from sqlalchemy import text, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncpg


class DatabaseInitializer:
    """Handles database schema initialization"""

    def __init__(self, db_url: str):
        self.db_url = db_url
        self.async_db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

    async def init_database(self):
        """Initialize database schema"""
        print("🔧 Initializing Hyper Registry Database...")

        # Create async engine
        engine = create_async_engine(self.async_db_url, echo=False)

        async with engine.begin() as conn:
            # Enable pgvector extension
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            print("✓ pgvector extension enabled")

            # Create registry_entries table
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS registry_entries (
                    entry_id VARCHAR(255) PRIMARY KEY,
                    category VARCHAR(100) NOT NULL,
                    title VARCHAR(500) NOT NULL,
                    description TEXT,
                    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
                    owner_id VARCHAR(255),
                    created_by VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata JSONB DEFAULT '{}',
                    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
                    keywords TEXT[] DEFAULT ARRAY[]::TEXT[],
                    ai_category VARCHAR(100),
                    ai_confidence FLOAT DEFAULT 0.0,
                    vector_embedding vector(384),
                    summary TEXT,
                    parent_id VARCHAR(255),
                    child_ids TEXT[] DEFAULT ARRAY[]::TEXT[],
                    related_ids TEXT[] DEFAULT ARRAY[]::TEXT[],
                    security_context JSONB,
                    compliance_status VARCHAR(50),
                    encrypted BOOLEAN DEFAULT FALSE,
                    access_count INT DEFAULT 0,
                    last_accessed TIMESTAMP,
                    version VARCHAR(50),
                    checksum VARCHAR(255)
                );
                CREATE INDEX idx_category ON registry_entries(category);
                CREATE INDEX idx_status ON registry_entries(status);
                CREATE INDEX idx_owner ON registry_entries(owner_id);
                CREATE INDEX idx_created_at ON registry_entries(created_at);
                CREATE INDEX idx_vector ON registry_entries USING ivfflat (vector_embedding vector_cosine_ops);
                CREATE INDEX idx_tags ON registry_entries USING GIN (tags);
            """))
            print("✓ registry_entries table created with indexes")

            # Create relationships table
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS relationships (
                    relationship_id VARCHAR(255) PRIMARY KEY,
                    source_id VARCHAR(255) NOT NULL REFERENCES registry_entries(entry_id) ON DELETE CASCADE,
                    target_id VARCHAR(255) NOT NULL REFERENCES registry_entries(entry_id) ON DELETE CASCADE,
                    relationship_type VARCHAR(100) NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    strength FLOAT DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    bidirectional BOOLEAN DEFAULT FALSE
                );
                CREATE INDEX idx_source ON relationships(source_id);
                CREATE INDEX idx_target ON relationships(target_id);
                CREATE INDEX idx_type ON relationships(relationship_type);
                CREATE INDEX idx_strength ON relationships(strength);
            """))
            print("✓ relationships table created with indexes")

            # Create metrics table
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS metrics (
                    metric_id SERIAL PRIMARY KEY,
                    metric_name VARCHAR(255) NOT NULL,
                    metric_value FLOAT NOT NULL,
                    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tags JSONB DEFAULT '{}',
                    unit VARCHAR(50)
                );
                CREATE INDEX idx_metric_name ON metrics(metric_name);
                CREATE INDEX idx_metric_timestamp ON metrics(metric_timestamp);
            """))
            print("✓ metrics table created with indexes")

            # Create search_cache table
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS search_cache (
                    cache_key VARCHAR(255) PRIMARY KEY,
                    search_results JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    hit_count INT DEFAULT 0
                );
                CREATE INDEX idx_expires ON search_cache(expires_at);
            """))
            print("✓ search_cache table created")

            # Create audit_log table
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    log_id SERIAL PRIMARY KEY,
                    entry_id VARCHAR(255),
                    action VARCHAR(100) NOT NULL,
                    actor_id VARCHAR(255),
                    changes JSONB,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address VARCHAR(45)
                );
                CREATE INDEX idx_entry_id ON audit_log(entry_id);
                CREATE INDEX idx_action ON audit_log(action);
                CREATE INDEX idx_timestamp ON audit_log(timestamp);
            """))
            print("✓ audit_log table created")

        await engine.dispose()
        print("✅ Database initialization complete!")

    async def health_check(self):
        """Check database health"""
        try:
            engine = create_async_engine(self.async_db_url, echo=False)
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            await engine.dispose()
            print("✅ Database health check: OK")
            return True
        except Exception as e:
            print(f"❌ Database health check failed: {e}")
            return False


async def main():
    """Initialize database"""
    db_url = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/hyper_registry"
    )
    
    initializer = DatabaseInitializer(db_url)
    
    try:
        await initializer.init_database()
        await initializer.health_check()
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
