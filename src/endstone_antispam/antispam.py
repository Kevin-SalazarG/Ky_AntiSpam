from endstone import ColorFormat
from endstone.event import event_handler, PlayerChatEvent
from endstone.plugin import Plugin
import time
import os
import tomllib
import tomlkit


class AntiSpam(Plugin):
    api_version = "0.5"
    config_file = "config.toml"
    config = {}

    player_last_message = {}
    player_last_time = {}
    player_warnings = {}

    def on_enable(self) -> None:
        self.load_config()
        self.register_events(self)
        self.logger.info(f"{ColorFormat.GREEN} AntiSpam enabled!")

    def on_disable(self) -> None:
        self.logger.info(f"{ColorFormat.RED} AntiSpam disabled.")

    def load_config(self) -> None:
        config_path = os.path.join(self.data_folder, self.config_file)
        if not os.path.exists(config_path):
            default_config = {
                "blocked_words": ["fuck", "nigga", "horion.download"],
                "message_delay": 0.5,
                "max_caps": 3,
                "max_warns": 3,
                "kick_message": "You have been kicked for receiving too many warnings!"
            }
            os.makedirs(self.data_folder, exist_ok=True)
            with open(config_path, "w") as config_file:
                config_data = tomlkit.document()
                config_data.update(default_config)
                config_file.write(tomlkit.dumps(config_data))
            self.config = default_config
            self.logger.info(f"{ColorFormat.YELLOW} Default config created at {config_path}")
        else:
            with open(config_path, "rb") as config_file:
                self.config = tomllib.load(config_file)
            self.logger.info(f"{ColorFormat.YELLOW} Config loaded from {config_path}")

    @event_handler
    def on_player_chat(self, event: PlayerChatEvent):
        player = event.player
        unique_id = player.unique_id

        message = event.message
        self.logger.info(f"{player.name}: {message}")

        last_message = self.player_last_message.get(unique_id)
        if last_message and message == last_message:
            self.warn_player(player, "You cannot send the same message twice!")
            event.cancelled = True
            return

        last_time = self.player_last_time.get(unique_id, 0)
        if time.time() - last_time < self.config["message_delay"]:
            self.warn_player(player, "You are sending messages too quickly!")
            event.cancelled = True
            return

        if sum(1 for c in message if c.isupper()) > self.config["max_caps"]:
            event.message = self.reduce_caps(message)
            self.warn_player(player, "Your message has too many capital letters.")

        if any(bad_word in message.lower() for bad_word in self.config["blocked_words"]):
            self.warn_player(player, "Your message contains blocked words!")
            event.cancelled = True
            return

        self.player_last_message[unique_id] = message
        self.player_last_time[unique_id] = time.time()

    def reduce_caps(self, message: str) -> str:
        caps_count = 0
        new_message = []
        for char in message:
            if char.isupper() and caps_count < self.config["max_caps"]:
                new_message.append(char)
                caps_count += 1
            else:
                new_message.append(char.lower())
        return ''.join(new_message)

    def warn_player(self, player, reason: str) -> None:
        unique_id = player.unique_id
        max_warns = self.config.get("max_warns", 3)
        warns = self.player_warnings.get(unique_id, 0) + 1
        self.player_warnings[unique_id] = warns
        player.send_message(f"{ColorFormat.YELLOW} Warning {warns}/{max_warns}: {reason}")

        if warns >= max_warns:
            kick_message = self.config.get("kick_message", "You have been kicked for receiving too many warnings!")
            player.kick(kick_message)
            self.logger.info(f"{player.name} was kicked for exceeding warnings.")
            self.player_warnings[unique_id] = 0