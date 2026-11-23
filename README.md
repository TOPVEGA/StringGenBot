<div align="center">

# VEGA STRING GENERATOR

### Telegram Session & Bot Session Generator

A Telegram bot built with Python and Pyrogram for generating supported Pyrogram and Telethon session strings through an interactive chat workflow.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![License](https://img.shields.io/badge/License-See%20Repository-lightgrey?style=for-the-badge)

</div>

---

## Overview

**VEGA STRING GENERATOR** is a Telegram bot project that provides an interactive interface for creating Telegram session strings using Pyrogram/Kurigram or Telethon. Users select a session type, complete the relevant Telegram authentication flow, and receive the generated session string.

The project also includes user registration, mandatory-channel membership checking, owner notifications, basic user statistics, broadcasting, and administrative utilities.

## Features

### Session Generation
- Interactive session-generation menu with inline buttons.
- Support for Pyrogram V1 mode.
- Support for Pyrogram V2 mode.
- Support for Telethon user sessions.
- Support for Pyrogram bot sessions.
- Support for Telethon bot sessions.
- Phone-number authentication for user sessions.
- OTP verification with support for spaced code input.
- Two-step verification password handling when Telegram requests it.
- Bot-token authentication for bot sessions.
- Session export after successful authentication.
- Session metadata including session type, user ID, username, account type, and creation timestamp.
- Clear handling for common authentication errors, including invalid API credentials, invalid phone numbers, incorrect or expired OTP codes, and invalid two-step verification passwords.

### Interactive User Experience
- `/start` and `/help` entry points.
- Inline buttons for selecting the session type.
- Step-by-step prompts for phone numbers, bot tokens, OTP codes, and two-step verification passwords.
- `/cancel` to cancel an active input flow.
- `/restart` to return to the session-generation menu.
- Configurable input timeouts.
- User-facing error messages and retry entry points.
- Temporary callback-click restrictions to reduce repeated button interactions.

### Session Delivery & Metadata
- Save generated session strings and metadata to local files.
- Send session information to the configured bot owner.
- Deliver generated user-session information through the user's Telegram Saved Messages flow.
- Deliver generated bot-session information to the requesting user.
- Include the session type and creation timestamp in the session record.
- Display a security warning reminding users not to share session strings.

### User Management
- Register users in MongoDB.
- Store user ID, first name, username, bot status, and join timestamp.
- Record the user's first interaction through the start flow.
- Display the user's join time using the configured Cairo timezone in the welcome message.
- Notify the owner when a new user starts the bot.

### Mandatory Channel Subscription
- Require users to join the configured updates channel before using the bot.
- Check channel membership when users interact with the bot.
- Show an inline join button when membership is missing.
- Provide channel and developer links in the welcome interface.

### Owner & Admin Tools
- View the total number of registered users.
- List registered users with their names, usernames, IDs, and join dates.
- Export long user lists as a text document.
- Broadcast a text message to registered users.
- View successful and failed broadcast delivery counts.
- Receive newly generated session details and metadata.
- Access owner-restricted runtime evaluation and shell utility handlers.

> **Administrative utilities:** Runtime evaluation and shell execution are powerful maintenance capabilities. Keep owner credentials private, restrict access to a trusted operator, and never expose these handlers to ordinary users.

## Supported Session Types

| Session Type | Description |
|---|---|
| Pyrogram V1 | Pyrogram-compatible user session mode |
| Pyrogram V2 | Pyrogram-compatible user session mode |
| Telethon | Telethon user session |
| Pyrogram Bot | Bot session using the Pyrogram client |
| Telethon Bot | Bot session using the Telethon client |

*Compatibility depends on the installed library versions and the Telegram API configuration.*

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pyrogram / Kurigram | Telegram bot and client interactions |
| Telethon | Telethon session generation |
| MongoDB | Registered-user storage |
| Motor | Asynchronous MongoDB access |
| python-dotenv | Environment-variable loading |
| TgCrypto | Optional Telegram cryptographic acceleration |
| asyncio | Asynchronous input and bot workflows |

## Project Structure

```text
Strng/
├── StringGen/
│   ├── __init__.py
│   ├── admin.py        # Owner statistics, user list, and broadcast
│   ├── callbacks.py    # Inline menu and session-type callbacks
│   ├── database.py     # MongoDB connection and users collection
│   ├── eval.py         # Owner-only evaluation and shell utilities
│   ├── generate.py     # Pyrogram and Telethon session workflows
│   ├── save_user.py    # User registration and join timestamp
│   ├── start.py        # Start/help, membership check, owner alerts
│   └── utils.py        # Interactive prompts and reply handling
├── config.py           # Bot and database configuration
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
├── sample.env          # Environment variable template
└── start               # Startup command
```

## Requirements

- Python 3.10 or a compatible version.
- Telegram API ID.
- Telegram API Hash.
- Telegram Bot Token.
- MongoDB connection URI.
- Internet connection.
- A Telegram account or bot that you own or are explicitly authorized to manage.

## Configuration

Create a `.env` file in the project root and set the required values:

```env
API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN
MONGO_URI=YOUR_MONGODB_CONNECTION_URI
OWNER_ID=YOUR_TELEGRAM_USER_ID
```

The application reads these values through `python-dotenv`. `OWNER_ID` has a default value in `config.py`, but setting your own owner ID explicitly is recommended.

## Installation

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd Strng
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create and configure your `.env` file, then start the bot:

```bash
python3 main.py
```

Alternatively, on a compatible Linux environment:

```bash
bash start
```

## User Commands & Workflow

| Command / Action | Description |
|---|---|
| `/start` | Open the welcome menu |
| `/help` | Display the bot entry menu |
| `/generate` | Open the session-generation menu |
| `/gen` | Alias for session generation |
| `/string` | Alias for session generation |
| `/str` | Alias for session generation |
| `/cancel` | Cancel the current input step |
| `/restart` | Restart the current generation flow |

After opening the generation menu, select the required session type and follow the prompts displayed by the bot.

## Owner Commands

The administrative handlers include the following commands:

| Command | Description |
|---|---|
| `/احصائيات` | Show the total registered-user count |
| `/المستخدمين` | List registered users |
| `/شيير <message>` | Broadcast a text message to registered users |
| `/eval <code>` | Owner-only Python evaluation utility |
| `/sh <command>` | Owner-only shell utility |

These handlers are restricted by the configured owner ID where implemented.

## Security & Privacy

**A Telegram session string is highly sensitive. It can provide access to the account it represents. Treat it like a password.**

- Only generate sessions for Telegram accounts or bots you own or are explicitly authorized to manage.
- Never share session strings, OTP codes, two-step verification passwords, API hashes, or bot tokens.
- Store `.env`, generated session files, and backups outside public repositories.
- Restrict access to the bot owner and the server hosting the project.
- Review the session-delivery logic before deployment: the current implementation sends generated session strings and metadata to the configured owner.
- Use a private, trusted MongoDB deployment and protect its credentials.
- Rotate credentials immediately if they are exposed.
- Do not use the bot to collect sessions from other people without their informed authorization.

## Notes & Limitations

- The project uses a configured mandatory channel (`@vegaone`) for membership checks.
- The owner must configure a valid Telegram bot, API credentials, and MongoDB URI.
- The generated session files are written under the `StrngGenBot/` directory at runtime.
- The current project includes owner notification of generated session strings; review this behavior carefully before allowing public access.
- The project contains an owner-only Python evaluation and shell execution feature. These capabilities can affect the host machine and should remain tightly restricted.
- A helper for account deletion exists in the source, but it is not presented as a user-facing feature in the current interaction flow.

## Credits

Developed under the **VEGA** project identity.

- Developer: [@TopVeGa](https://t.me/TopVeGa)
- Updates & Community: [@vegaone](https://t.me/vegaone)
- Source reference: [@Logii3](https://t.me/Logii3)
- Boot file: [@StrngGenBot](https://t.me/StrngGenBot)
## License & Copyright

No standalone `LICENSE` file was included in the supplied archive. Add a license file before redistributing the project, and follow the licenses of all third-party libraries and components.

Respect the rights of original authors and obtain permission before redistributing third-party code or assets.

---

<div align="center">

**VEGA STRING GENERATOR**

*Session Generation • Telegram Automation • Account Tools*

</div>


<!-- ═══════════════════════════════════════════════════════════════════════ --><!--                       Copyright | Footer                              --><!-- ═══════════════════════════════════════════════════════════════════════ --><div align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0:3B82F6,100:0F172A&height=4&width=40%&section=header" />
  <br><br>  <p style="color: #9CA3AF; font-size: 14px;">
    <b style="color: #3B82F6;">Brand:</b> VEGA &amp; Logic &nbsp;|&nbsp;
    <b style="color: #3B82F6;">Copyright:</b> © 2015 - 2025
  </p>
  <p style="color: #6B7280; font-size: 12px;">
  </p>
</div><br><!-- Smooth Gradient Footer Background --><img src="https://capsule-render.vercel.app/api?type=waving&color=0:3B82F6,50:1E3A8A,100:0F172A&height=120&section=footer" width="100%" /></div>


