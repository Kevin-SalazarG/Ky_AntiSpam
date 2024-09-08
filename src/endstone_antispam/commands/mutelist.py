from endstone import Player, ColorFormat
from endstone.command import CommandExecutor, CommandSender, Command


class MuteListCommand(CommandExecutor):
    def __init__(self, mute_manager):
        super().__init__()
        self.mute_manager = mute_manager

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if not isinstance(sender, Player):
            sender.send_error_message("This command can only be executed by a player.")
            return False

        muted_players = self.mute_manager.getAllMutedPlayers()

        if not muted_players:
            sender.send_message(f"{ColorFormat.YELLOW} There are no players currently muted.")
            return True

        message = f"{ColorFormat.GREEN}List of muted players:"
        for unique_id, mute_info in muted_players.items():
            player_name = sender.server.get_player(unique_id).name
            remaining_time = int(mute_info["remaining_time"])
            reason = mute_info.get("reason", "No reason provided")
            message += f"\n{ColorFormat.WHITE}{player_name} - {ColorFormat.RED}{remaining_time} seconds - Reason: {ColorFormat.WHITE}{reason}"

        sender.send_message(message)
        return True
