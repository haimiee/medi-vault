from tortoise import Tortoise

DATABASE_URL = "sqlite://db.sqlite3"  # Can change this to PostgreSQL
# DATABASE_URL = "sqlite://:memory:"  # For in memory only db (resets db when server closes)

# Initialize database
async def init_db():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={"models": ["db.models"]},  # Path to models
    )
    await Tortoise.generate_schemas()