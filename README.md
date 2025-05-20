# Chasovoy Telegram Bot

**[Русская версия README.md](README_rus.md)**

Chasovoy Telegram Bot is a time announcer bot for Telegram. When added as an administrator to a group or channel, it sends an hourly message announcing the current time—such as "It's 2 p.m. in the capital"—with various message templates.

## Features

- **Automatic Hourly Announcements:** Sends the current time every hour to all groups/channels where the bot is an admin.
- **Message Variations:** Uses a wide range of message templates for variety and engagement.
- **Easy Deployment:** Uses Ansible for seamless server setup and deployment.

## Installation & Deployment

### Prerequisites

- **Python:** recommended to use the latest version
- **Ansible** installed on your local machine
- **A server** (VPS or other) where the bot will run
- **Telegram Bot API token** (from @BotFather)

### Steps

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yet-another-artem/chasovoy-telegram-bot.git
    cd chasovoy-telegram-bot
    git checkout develop
    ```

2. **Install Ansible**
    ```bash
    pip install ansible
    ```

3. **Configure Inventory**
    - Add your server details to `./ansible/ansible_inventory.yml`.

4. **Set Telegram Bot Token**
    - Obtain your Telegram bot token from [@BotFather](https://core.telegram.org/bots#botfather).
    - Replace the encrypted token in `./ansible/roles/ansible_deploy_tg_bot_role/vars/main.yml` with your actual API token.

5. **Run the Ansible Playbook**
    ```bash
    ansible-playbook -i ./ansible/ansible_inventory.yml ./ansible/ansible_playbook.yml
    ```

## Configuration

- **ansible/ansible_inventory.yml:** List your server(s) here for deployment.
- **ansible/roles/ansible_deploy_tg_bot_role/vars/main.yml:** Store your Telegram Bot API token here. **Never commit your real token to the repository!**

## Usage

- Add the bot to your Telegram group or channel as an administrator.
- The bot will automatically post the current time every hour.
- Message formats vary for a more engaging experience.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements and bug fixes.

## License

[MIT License](LICENSE)

---

*Made with ❤️ by yet-another-artem*
