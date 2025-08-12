# Database Module

This directory contains the database models and operations for the Telegram bot. The bot uses SQLAlchemy's `asyncio` extension to interact with the database non-blockingly.

## Structure

The database module consists of:

- `__init__.py` - Sets up the async database connection and defines the base model.
- `users.py` - Implements the async User model and user-related operations.

## Database Connection

The asynchronous database connection is established in `__init__.py`. The connection string must specify an async driver (e.g., `postgresql+asyncpg` or `sqlite+aiosqlite`).

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from Bot.config import DB_URI

# Create async engine
engine = create_async_engine(DB_URI)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

# Create base model
BASE = declarative_base()

# Function to get a session
async def get_session():
    return AsyncSessionLocal()
```

## User Model

The User model (`users.py`) stores information about bot users:

```python
class Users(BASE):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(UnicodeText)
    first_name = Column(UnicodeText)
    last_name = Column(UnicodeText)
    join_date = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
```

### Fields

- `user_id` - Telegram user ID (primary key)
- `username` - Telegram username
- `first_name` - User's first name
- `last_name` - User's last name
- `join_date` - When the user first interacted with the bot
- `last_seen` - When the user last interacted with the bot

## User Operations

The `users.py` file provides several `async` functions for user operations:

- `add_user(user_id, username, first_name, last_name)` - Add a new user or update existing user.
- `get_user(user_id)` - Get a user by their ID.
- `get_all_users()` - Get all users.
- `update_last_seen(user_id)` - Update a user's last seen time.
- `id_to_username(user_id)` - Get a username for a given user ID.

## Example Usage

All database operations are asynchronous and must be awaited.

### Adding or Updating a User

```python
import asyncio
from Bot.sql.users import add_user

async def main():
    # Add a new user or update existing user
    await add_user(
        user_id=123456789,
        username="john_doe",
        first_name="John",
        last_name="Doe"
    )

asyncio.run(main())
```

### Getting User Information

```python
import asyncio
from Bot.sql.users import get_user

async def main():
    # Get user information
    user = await get_user(123456789)
    if user:
        print(f"Username: {user.username}")
        print(f"First name: {user.first_name}")
        print(f"Last seen: {user.last_seen}")

asyncio.run(main())
```

### Updating Last Seen

```python
import asyncio
from Bot.sql.users import update_last_seen

async def main():
    # Update user's last seen time
    await update_last_seen(123456789)

asyncio.run(main())
```

### Getting All Users

```python
import asyncio
from Bot.sql.users import get_all_users

async def main():
    # Get all users
    users = await get_all_users()
    print(f"Total users: {len(users)}")

asyncio.run(main())
```

## Creating New Models

To create a new database model:

1.  Create a new Python file in the `Bot/sql/` directory (e.g., `messages.py`).
2.  Import the necessary components:
    ```python
    from Bot.sql import BASE
    from sqlalchemy import Column, Integer, UnicodeText, DateTime, ForeignKey
    from sqlalchemy.orm import relationship
    from datetime import datetime
    ```
3.  Define your model class, inheriting from `BASE`:
    ```python
    class Messages(BASE):
        __tablename__ = "messages"
        
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('users.user_id'))
        text = Column(UnicodeText)
        timestamp = Column(DateTime, default=datetime.utcnow)
        
        user = relationship("Users", backref="messages")
    ```
4.  Implement async operations for your new model. Table creation is handled automatically at startup by the `initialize_database` function.
    ```python
    from Bot.sql import get_session

    # Add a message
    async def add_message(user_id, text):
        async with await get_session() as session:
            message = Messages(user_id=user_id, text=text)
            session.add(message)
            await session.commit()
            return message
    ```

## Best Practices

1.  Always use an `async with` block to manage session lifecycle. This ensures the session is always closed correctly.
    ```python
    async with await get_session() as session:
        # Perform database operations
        user = await session.get(Users, 12345)
        # ...
        await session.commit()
    ```

2.  Use appropriate column types for your data.

3.  Create indexes for frequently queried columns to improve performance.

4.  Use relationships between models where appropriate.

5.  Keep database operations separate from bot logic.

6.  Ensure all database functions are `async` and are `await`ed when called.
