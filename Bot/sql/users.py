from Bot.sql import get_session, BASE
from sqlalchemy import Column, Integer, UnicodeText, DateTime, select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

class Users(BASE):
    """
    Represents a user in the database.
    This model is compatible with both sync and async sessions.
    """
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(UnicodeText)
    first_name = Column(UnicodeText)
    last_name = Column(UnicodeText)
    join_date = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

    def __init__(self, user_id, username, first_name=None, last_name=None):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"<User {self.user_id}>"

async def add_user(user_id, username, first_name=None, last_name=None):
    """
    Adds a new user to the database or updates an existing one asynchronously.
    Returns True if a new user was created, False otherwise.
    """
    async with await get_session() as session:
        user = await session.get(Users, user_id)
        if not user:
            # Create a new user instance
            user = Users(user_id, username, first_name, last_name)
            session.add(user)
            await session.commit()
            return True
        else:
            # Update existing user's details
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.last_seen = datetime.utcnow()
            await session.commit()
            return False

async def id_to_username(user_id):
    """
    Retrieves a user's username by their user_id asynchronously.
    """
    async with await get_session() as session:
        user = await session.get(Users, user_id)
        if user:
            return user.username
        return None

async def get_user(user_id):
    """
    Retrieves a full user object by their user_id asynchronously.
    """
    async with await get_session() as session:
        return await session.get(Users, user_id)

async def get_all_users():
    """
    Retrieves a list of all user objects from the database asynchronously.
    """
    async with await get_session() as session:
        # Construct a select statement for the Users table.
        stmt = select(Users)
        # Execute the statement and get scalar results.
        result = await session.execute(stmt)
        return result.scalars().all()

async def update_last_seen(user_id):
    """
    Updates the last_seen timestamp for a specific user asynchronously.
    Returns True if the user was found and updated, False otherwise.
    """
    async with await get_session() as session:
        user = await session.get(Users, user_id)
        if user:
            user.last_seen = datetime.utcnow()
            await session.commit()
            return True
        return False