from endstone import Player, ColorFormat
from endstone.command import CommandExecutor, CommandSender, Command


class UnMuteCommand(CommandExecutor):
    def __init__(self, mute_manager):
        super().__init__()
        self.mute_manager = mute_manager

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if not isinstance(sender, Player):
            sender.send_error_message("This command can only be executed by a player.")
            return False

        if len(args) < 1:
            sender.send_error_message("Usage: /unmute <player: player>")
            return False

        player_name = args[0].strip('"')
        target = sender.server.get_player(player_name)
        if target is None:
            sender.send_error_message(f"Player {player_name} not found.")
            return True

        if target == sender:
            sender.send_error_message("You cannot unmute yourself.")
            return False

        if self.mute_manager.unmutePlayer(target.unique_id):
            sender.send_message(f"{ColorFormat.GREEN}Player {ColorFormat.WHITE}{target.name} {ColorFormat.GREEN}has been unmuted.")
            target.send_message(f"{ColorFormat.GREEN}You have been unmuted. You can now chat again.")
        else:
            sender.send_error_message(f"Player {player_name} is not currently muted.")

        return True
