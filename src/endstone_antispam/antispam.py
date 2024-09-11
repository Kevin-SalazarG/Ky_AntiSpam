from endstone import ColorFormat
from endstone.event import event_handler, PlayerChatEvent, PlayerQuitEvent
from endstone.plugin import Plugin
import time
import os
import tomllib
import tomlkit

from endstone_antispam.commands.globalmute import GlobalMuteCommand
from endstone_antispam.commands.mute import MuteCommand
from endstone_antispam.commands.unmute import UnMuteCommand
from endstone_antispam.commands.mutelist import MuteListCommand
from endstone_antispam.mutemanager import MuteManager
from collections import defaultdict
import re


class AntiSpam(Plugin):
    api_version = "0.5"
    config_file = "config.toml"
    config = {}

    commands = {
        "mute": {
            "description": "Mutes a player for a specified duration.",
            "usages": ["/mute <player: player> <duration: int> <reason: message>"],
            "permissions": ["antispam.command.mute"]
        },
        "unmute": {
            "description": "Unmutes a player.",
            "usages": ["/unmute <player: player>"],
            "permissions": ["antispam.command.unmute"]
        },
        "mutelist": {
            "description": "Lists all currently muted players.",
            "usages": ["/mutelist"],
            "permissions": ["antispam.command.mutelist"]
        },
        "globalmute": {
            "description": "Toggles global mute for the entire server.",
            "usages": ["/globalmute"],
            "permissions": ["antispam.command.globalmute"]
        }
    }

    permissions = {
        "antispam.command.mute": {
            "description": "Allow users to use the /mute command.",
            "default": False,
        },
        "antispam.command.unmute": {
            "description": "Unmutes a player.",
            "default": False,
        },
        "antispam.command.mutelist": {
            "description": "Lists all currently muted players.",
            "default": False,
        },
        "antispam.command.globalmute": {
            "description": "Allow users to use the /globalmute command.",
            "default": False,
        }
    }

    def __init__(self):
        super().__init__()
        self.mute_manager = MuteManager()
        self.player_data = defaultdict(lambda: {
            "last_message": "",
            "last_time": 0,
            "warnings": 0
        })
        self.blocked_words_regex = None

    def on_enable(self) -> None:
        self.load_config()
        self.register_events(self)
        self.register_commands()
        self.logger.info(f"{ColorFormat.GREEN}Ky_AntiSpam enabled!")

    def on_disable(self) -> None:
        self.logger.info(f"{ColorFormat.RED}Ky_AntiSpam disabled.")

    def register_commands(self):
        self.get_command("mute").executor = MuteCommand(self.mute_manager)
        self.get_command("unmute").executor = UnMuteCommand(self.mute_manager)
        self.get_command("mutelist").executor = MuteListCommand(self.mute_manager)
        self.get_command("globalmute").executor = GlobalMuteCommand(self.mute_manager)

    def load_config(self) -> None:
        config_path = os.path.join(self.data_folder, self.config_file)
        if not os.path.exists(config_path):
            self.create_default_config(config_path)
        else:
            with open(config_path, "rb") as config_file:
                self.config = tomllib.load(config_file)
        self.blocked_words_regex = re.compile(r'|'.join(map(re.escape, self.config["blocked_words"])))

    def create_default_config(self, config_path):
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

    @event_handler
    def on_player_chat(self, event: PlayerChatEvent):
        player = event.player
        name = player.name

        if self.check_mute_status(player, event):
            return

        if player.has_permission("antispam.message.bypass"):
            return

        message = event.message

        if self.check_message_violations(player, name, message):
            event.cancelled = True
            return

        if self.has_too_many_caps(message):
            event.message = self.reduce_caps(message)
            self.warn_player(player, "Your message has too many capital letters.")

        self.update_player_stats(name, message)

    def check_mute_status(self, player, event):
        if self.mute_manager.isGlobalMuteActive() and not player.has_permission("antispam.message.globalmute"):
            player.send_message(f"{ColorFormat.RED} The server is in global mute. You cannot chat at this time.")
            event.cancelled = True
            return True

        if self.mute_manager.isPlayerMuted(player.name):
            mute_info = self.mute_manager.getMuteInfo(player.name)
            remaining_time = mute_info["remaining_time"]
            player.send_message(f"{ColorFormat.RED} You are muted. You can speak again in {int(remaining_time)} seconds.")
            event.cancelled = True
            return True

        return False

    def check_message_violations(self, player, name, message):
        player_data = self.player_data[name]
        last_message = player_data["last_message"]
        last_time = player_data["last_time"]

        if last_message == message:
            self.warn_player(player, "You cannot send the same message twice!")
            return True

        if time.monotonic() - last_time < self.config["message_delay"]:
            self.warn_player(player, "You are sending messages too quickly!")
            return True

        if self.blocked_words_regex.search(message.lower()):
            self.warn_player(player, "Your message contains blocked words!")
            return True

        return False

    def has_too_many_caps(self, message):
        return sum(1 for c in message if c.isupper()) > self.config["max_caps"]

    def reduce_caps(self, message: str) -> str:
        upper_count = 0
        new_message = []
        max_caps = self.config["max_caps"]

        for char in message:
            if char.isupper():
                upper_count += 1
                if upper_count > max_caps:
                    new_message.append(char.lower())
                else:
                    new_message.append(char)
            else:
                new_message.append(char)

        return ''.join(new_message)

    def update_player_stats(self, name, message):
        self.player_data[name]["last_message"] = message
        self.player_data[name]["last_time"] = time.monotonic()

    def warn_player(self, player, reason: str) -> None:
        name = player.name
        max_warns = self.config.get("max_warns", 3)
        player_data = self.player_data[name]

        warns = player_data["warnings"] + 1
        player_data["warnings"] = warns

        player.send_message(f"{ColorFormat.YELLOW} Warning {warns}/{max_warns}: {reason}")

        if warns >= max_warns:
            kick_message = self.config.get("kick_message", "You have been kicked for receiving too many warnings!")
            player.kick(kick_message)
            self.logger.info(f"{player.name} was kicked for exceeding warnings.")
            self.player_data.pop(name, None)

    @event_handler
    def on_player_quit(self, event: PlayerQuitEvent):
        player = event.player

        self.player_data.pop(player.name, None)