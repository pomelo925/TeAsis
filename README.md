<div align="center">

# TeAsis - Discord Bot  

<3. Run the bot:
   ```bash
   ./run.sh dcbot deploy
   ```

<details>
<summary>Available Commands</summary>

- `./run.sh` - Show usage help
- `./run.sh dcbot dev` - Run bot in development mode (interactive shell)
- `./run.sh dcbot deploy` - Run bot in production mode
- `./run.sh tower` - Run Watchtower for automatic Docker updates
- `./run.sh all` - Run bot (deploy mode) + Watchtower

</details>

<div align="center">

</br>

## Features

</div><strong>Multifunctional Discord Bot</strong>
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
   git clone https://github.com/pomelo925/TeAsis
   ```

2. Configure these files:  
     * `docker/config/dcbot.token.env`: Set your Discord bot token
     * `docker/config/docker.token.env`: Set Docker registry credentials

3. Run the bot:
   ```bash
   ./run.sh dcbot deploy
   ```

  ### Available Commands

  - `./run.sh` - Show usage help
  - `./run.sh dcbot dev` - Run bot in development mode (interactive shell)
  - `./run.sh dcbot deploy` - Run bot in production mode
  - `./run.sh tower` - Run Watchtower for automatic Docker updates
  - `./run.sh all` - Run bot (deploy mode) + Watchtower

<div align="center">

</br>

## Architecture

</div>

```
discord-bot-tea-girl/
├── run.sh                    # Enhanced startup script with multiple modes
├── discord-bot/              # Main bot source code
│   ├── bot.py               # Bot core and event handlers
│   ├── admin/               # Admin commands (sync, reload, status)
│   ├── cmds/game/           # Game commands (pong, whoami)
│   └── cmds/voice/          # Voice commands (tts)
└── docker/                  # Docker configuration
    ├── dockerfile.dcbot     # Python 3.13 Alpine + FFmpeg
    ├── compose.dcbot.yml    # Discord bot services (dev/deploy)
    ├── compose.watchtower.yml # Watchtower auto-update service
    ├── requirements.txt     # discord.py[voice], gTTS
    └── config/              # Configuration files
        ├── dcbot.token.env  # Discord bot token
        └── docker.token.env # Docker registry credentials
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