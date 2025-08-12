import pkgutil
import importlib
from pathlib import Path
from Bot import LOGGER
from Bot.config import Config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# --- Dynamic Module Loading ---
def _load_all_modules():
    """Dynamically loads all modules from this package to register models with BASE."""
    package_path = str(Path(__file__).parent.resolve())
    for _, module_name, _ in pkgutil.walk_packages([package_path]):
        full_module_path = f"{__name__}.{module_name}"
        try:
            importlib.import_module(full_module_path)
        except Exception as e:
            LOGGER.error(f"Could not import module {module_name}: {e}")

# --- SQLAlchemy Setup ---

# 1. Declarative Base for all models
BASE = declarative_base()

# 2. Create the async engine.
engine = create_async_engine(Config.DB_URI)

# 3. Create an async session factory
#    expire_on_commit=False is recommended for async usage to prevent
#    issues with accessing objects after the session is closed.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

# --- Public Functions ---

async def get_session():
    """Provides a new async session instance from the factory."""
    return AsyncSessionLocal()

async def initialize_database():
    """
    Loads all model modules and then creates all tables in the database.
    This should be an async function called ONCE when your bot starts up.
    """
    # Load all modules to ensure models are registered with BASE
    _load_all_modules()

    LOGGER.info("Creating database tables...")
    async with engine.begin() as conn:
        # This command runs the synchronous create_all in an async-safe way
        await conn.run_sync(BASE.metadata.create_all)
    LOGGER.info("Connected to the database and all tables are created!")

