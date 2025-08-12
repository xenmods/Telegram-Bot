![Telegram Bot Template](https://media.animerealms.org/image/AgACAgUAAx0EboWBewACZHFn_hGcWmshdPqMSzffkdFe9R9x2QACxcAxG1bT8VcemRX3TK9DmgEAAwIAA3kAAzYE)

# Telegram-Bot

A modular Telegram Bot boilerplate with database integration. This project provides a structured foundation for building Telegram bots with a clean architecture that's easy to extend.

## Features

- **Modular Architecture**: Easily add new commands and features.
- **Dual Database Support**:
  - **SQLAlchemy**: For relational database operations (PostgreSQL, SQLite, etc.).
  - **Motor (Asyncio)**: For non-blocking MongoDB operations.
- **Developer Experience**:
  - **CLI Tool**: A `manage.py` script for running the bot, with hot-reloading for development.
  - **Docker Support**: Includes a `Dockerfile` and `docker-compose.yml` for easy containerization.
- **Core Functionality**:
  - **User Tracking**: Tracks user join dates and last seen times.
  - **Rate Limiting & Error Handling**: Decorators to protect and manage your bot's functions.
  - **Utility Functions**: Helpers for common tasks like parsing and formatting.
- **Asynchronous**: Built with `asyncio` and uses `uvloop` on non-Windows systems for high performance.
- **Configuration**: Uses a `.env` file for easy and secure configuration management.

## Requirements

- Python 3.7+
- Docker (optional, for containerized deployment)
- Dependencies listed in `requirements.txt`:
  - Pyrogram (Telegram client library)
  - SQLAlchemy (ORM for database operations)
  - psycopg2-binary (PostgreSQL adapter)
  - motor (Asynchronous MongoDB driver)
  - tgcrypto (Fast cryptography library for Telegram)
  - python-dotenv (Environment variable management)
  - **watchdog** (For file system monitoring and hot-reloading)
  - **typer** (For creating the command-line interface)
  - uvloop (Automatically installed on non-Windows platforms for improved performance)

## Setup

1.  **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/Telegram-Bot.git
    cd Telegram-Bot
    ```

2.  **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure the bot**
    - Copy the sample environment file and edit it with your credentials:
      ```bash
      cp .env.sample .env
      ```
    - Open `.env` and fill in your details (`BOT_TOKEN`, `API_ID`, `API_HASH`, etc.).

## Usage

The bot is managed through a command-line interface in `manage.py`.

### Running the Bot

- **Run normally:**

  ```bash
  python manage.py
  ```

- **Run with hot-reloading for development:**
  This will automatically restart the bot whenever you save a change in the `Bot/` directory.
  ```bash
  python manage.py --reload
  ```

## Docker

This project is fully configured to run with Docker for consistent and isolated deployments.

1.  **Build and run the container:**
    Make sure your `.env` file is configured. Then, run:

    ```bash
    docker-compose up --build
    ```

2.  **Run in the background (detached mode):**

    ```bash
    docker-compose up --build -d
    ```

3.  **To stop the container:**
    ```bash
    docker-compose down
    ```

## Project Structure

```
Telegram-Bot/
├── Bot/                    # Main bot package
│   ├── core/               # Core functionality
│   ├── sql/                 # SQLAlchemy database models
│   ├── mongo/              # MongoDB models
│   ├── modules/            # Bot command modules
│   ├── config.py           # Configuration settings
│   ├── __init__.py         # Bot initialization
│   └── __main__.py         # Entry point
├── .env.sample             # Sample environment variables
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker image definition
├── manage.py               # Command-line interface for management
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

## Environment Configuration

The bot uses environment variables for configuration, which can be set in the `.env` file. This allows for easier deployment across different environments while keeping sensitive information secure.

Available environment variables:

- `BOT_TOKEN`: Telegram bot token from BotFather
- `API_ID`: Telegram API ID
- `API_HASH`: Telegram API Hash
- `DB_URI`: Database connection string for SQLAlchemy
- `MONGO_URI`: MongoDB connection string (optional)

## Database

### SQLAlchemy

The bot uses SQLAlchemy ORM for SQL database operations. By default, it's configured to use SQLite, but you can change the `DB_URI` in `config.py` to use other database engines like PostgreSQL or MySQL.

The SQLAlchemy database module provides:

- A base model system in `db/__init__.py`
- User tracking functionality in `db/users.py` with:
  - User ID and username tracking
  - First and last name storage
  - Join date and last seen tracking

For more detailed information about the SQLAlchemy database structure and operations, see the [Database Documentation](Bot/db/README.md).

### MongoDB

The bot also supports MongoDB for NoSQL database operations using Motor AsyncIO for asynchronous operations. MongoDB integration is optional and will be enabled only if `MONGO_URI` is provided in the configuration.

The MongoDB module provides:

- Asynchronous MongoDB connection setup in `mongo/__init__.py`
- Asynchronous user tracking functionality in `mongo/users.py` with similar features to the SQLAlchemy version
- All database operations are non-blocking, using `async/await` syntax

For more detailed information about the MongoDB structure and operations, see the [MongoDB Documentation](Bot/mongo/README.md).

## Modules

The bot has a modular design that makes it easy to add new commands and features:

1. Create a new Python file in the `Bot/modules/` directory
2. Define your command handlers using the Pyrogram decorator system
3. The module will be automatically loaded at startup

### Available Commands

- `/start` - Start the bot and get a welcome message
- `/help` - Show available commands
- `/info` - Show information about yourself
- `/stats` - Show bot statistics

For more information about creating and customizing modules, see the [Modules Documentation](Bot/modules/README.md).

## Core Functionality

### Decorators

The bot includes several decorators in the `Bot/core/decorators` directory:

- `rate_limit.py` - Rate limit a function to a certain number of calls per time window
- `tracking.py` - Track user activity
- `error_handler.py` - Handle errors in functions

### Utilities

The bot includes utility functions in the `Bot/core/utils` directory:

- `parser.py` - Parse command arguments from a message text
- `formatting.py` - Format user mentions and time intervals

## Deploy to StackHost (Optional):

<div align="left">
  <a href="https://t.me/StackHost">
     <img src="https://graph.org/file/7e91d83f67d20f158cfdc.jpg" alt="Deploy On StackHost" width="200" />
  </a>
</div>

## Extending

To add new features:

1. **New commands**: Add new modules in the `Bot/modules/` directory
2. **Database models**: Create new models in the `Bot/db/` directory
3. **Configuration**: Add new configuration options in `Bot/config.py`
4. **Utility functions**: Add new utility functions in the appropriate directory

## Logging

The bot includes a comprehensive logging system configured in `Bot/__init__.py`. Logs are saved to `log.txt` and also output to the console.

## License

This project is licensed under the terms included in the LICENSE file.
