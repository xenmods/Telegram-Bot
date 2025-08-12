from Bot import bot
from Bot.sql.users import add_user, get_user, get_all_users
from Bot.core.decorators.tracking import track_user
from Bot.core.decorators.error_handler import handle_errors
from Bot.core.utils.formatting import format_user_mention

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@bot.on_message(filters.command("start"))
@track_user
@handle_errors
async def start(_, message: Message):
    user = message.from_user
    await add_user(user.id, user.username, user.first_name, user.last_name)
    
    # Create welcome message with user info
    welcome_text = (
        f"👋 Hello {user.first_name}!\n\n"
        f"I'm a Telegram bot template with a modular structure and database integration.\n\n"
        f"<blockquote>Use /help to see available commands.</blockquote>"
    )
    
    # Create inline keyboard with help button
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Help", callback_data="help")]
    ])
    
    await message.reply_text(welcome_text, reply_markup=keyboard)

@bot.on_message(filters.command("help"))
@track_user
@handle_errors
async def help(_, message: Message):
    help_text = (
        "🤖 **Available Commands:**\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/info - Show information about yourself\n"
        "/stats - Show bot statistics\n\n"
        "For more information, visit the [GitHub repository](https://github.com/yourusername/Telegram-Bot)."
    )
    
    await message.reply_text(help_text, disable_web_page_preview=True)

@bot.on_message(filters.command("info"))
@track_user
@handle_errors
async def info(_, message: Message):
    user = message.from_user
    db_user = await get_user(user.id)
    
    if not db_user:
        await message.reply_text("You are not registered in the database.")
        return
    
    # Format join date
    join_date = db_user.join_date.strftime("%Y-%m-%d %H:%M:%S")
    last_seen = db_user.last_seen.strftime("%Y-%m-%d %H:%M:%S")
    
    info_text = (
        f"👤 **User Information:**\n\n"
        f"ID: `{user.id}`\n"
        f"Username: {format_user_mention(user.id, user.username)}\n"
        f"First Name: {user.first_name}\n"
        f"Last Name: {user.last_name or 'N/A'}\n"
        f"Join Date: {join_date}\n"
        f"Last Seen: {last_seen}"
    )
    
    await message.reply_text(info_text)

@bot.on_message(filters.command("stats"))
@track_user
@handle_errors
async def stats(_, message: Message):

    
    users = await get_all_users()
    total_users = len(users)
    
    stats_text = (
        f"📊 **Bot Statistics:**\n\n"
        f"Total Users: {total_users}\n"
        f"Active Users: {total_users}"
    )
    
    await message.reply_text(stats_text)

@bot.on_callback_query(filters.regex(r"^help$"))
@handle_errors
async def callback_handler(_, callback_query):
    if callback_query.data == "help":
        await callback_query.answer()
        await help(_, callback_query.message)
