# discord-bot-from-scratch
This is a discord bot created from scratch in python using only WebSocket and REST API, as a research project on the discord API.

# YAML format
```yaml
token: token-goes-here
prefix: prefix-goes-here
```

# Requirements
- websocket-client
- json
- requests
- yaml

# Files and Directories
- src: The source directory
  - main.py: The main python file
- config.yml: Config file
- requirements.txt: List of all dependencies
- response.json: An example json response from discord

# Library and API used
- This project does not use any third-party discord bot libraries
- The project only uses [Discord API](https://discord.com/developers/docs/intro) and the [Discord Gateway](https://discord.com/developers/docs/topics/gateway)

# Getting Started
- 1. Create a config.yml file, write the token and the prefix into it
- 2. Set the path of the config.yml file in the main.py script
- 3. Start the bot with `python3 main.py`

# Code Style
- This project uses the [Google Python Coding Style](https://google.github.io/styleguide/pyguide.html)

# LICENSE
- [MIT License](https://github.com/maxxie114/discord-bot-from-scratch/blob/main/LICENSE)

# Contribution
- Contribution is allowed with a pull request, please make sure you follow the code style
