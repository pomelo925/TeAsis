<div align="center">

# TeAsis - Discord Bot  

<p align="center">
  <strong>Multifunctional Discord Bot</strong>
</p>


[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


</div>

<div align="center" style="max-width: 80%; margin: 0 auto;">

A Python Discord bot built with discord.py featuring gaming interactions, text-to-speech, and admin management. Containerized with Docker for easy deployment.

</div>

<div align="center">

</br>

## Quick Start

</div>

### Prerequisites

- Linux OS Server
- Docker & Docker Compose
- Discord Bot Token from [Discord Developer Portal](https://discord.com/developers/applications)

### Setup

1. Clone and configure:
   ```bash
   git clone https://github.com/pomelo925/discord-bot-tea-girl.git
   cd discord-bot-tea-girl/docker
   echo "DISCORD_TOKEN=your_bot_token_here" > .env
   ```

2. Run the bot:
   ```bash
   cd .. && ./run.sh
   ```

<div align="center">

</br>

## Features

</div>

- **🎮 Games**: `/pong`, `/ping`, `/whoami` - Interactive gaming commands
- **🎵 Voice**: `/tts <text>` - Text-to-speech with Chinese support  
- **⚙️ Admin**: `!sync`, `!reload`, `!status` - Bot management commands

<div align="center">

</br>

## Architecture

</div>

```
discord-bot-tea-girl/
├── run.sh                    # Bot startup script
├── discord-bot/              # Main bot source code
│   ├── bot.py               # Bot core and event handlers
│   ├── admin/               # Admin commands (sync, reload, status)
│   ├── cmds/game/           # Game commands (pong, whoami)
│   └── cmds/voice/          # Voice commands (tts)
└── docker/                  # Docker configuration
    ├── Dockerfile           # Python 3.13 Alpine + FFmpeg
    ├── compose.yml          # Dev/prod services
    └── requirements.txt     # discord.py[voice], gTTS
```

**Tech Stack**: Python 3.13, discord.py, Docker, FFmpeg, gTTS

<div align="center">

</br>

## License

</div>

Distributed under the MIT License. See `LICENSE` for more information.

</br>

<div align="center">

## Contributors

</div>

<a href="https://github.com/pomelo925/discord-bot-tea-girl/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=pomelo925/discord-bot-tea-girl" />
</a>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/pomelo925/discord-bot-tea-girl.svg?style=for-the-badge
[contributors-url]: https://github.com/pomelo925/discord-bot-tea-girl/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/pomelo925/discord-bot-tea-girl.svg?style=for-the-badge
[forks-url]: https://github.com/pomelo925/discord-bot-tea-girl/network/members
[stars-shield]: https://img.shields.io/github/stars/pomelo925/discord-bot-tea-girl.svg?style=for-the-badge
[stars-url]: https://github.com/pomelo925/discord-bot-tea-girl/stargazers
[issues-shield]: https://img.shields.io/github/issues/pomelo925/discord-bot-tea-girl.svg?style=for-the-badge
[issues-url]: https://github.com/pomelo925/discord-bot-tea-girl/issues
[license-shield]: https://img.shields.io/github/license/pomelo925/discord-bot-tea-girl.svg?style=for-the-badge
[license-url]: https://github.com/pomelo925/discord-bot-tea-girl/blob/main/LICENSE