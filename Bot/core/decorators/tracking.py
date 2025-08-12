from functools import wraps
from Bot.sql.users import update_last_seen

def track_user(func):
    """Decorator to track user activity."""
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        # Update user's last seen time
        await update_last_seen(message.from_user.id)
        
        return await func(client, message, *args, **kwargs)
    
    return wrapper 