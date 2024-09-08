from endstone import Player, ColorFormat
from endstone.command import CommandExecutor, CommandSender, Command


class GlobalMuteCommand(CommandExecutor):
    def __init__(self, mute_manager):
        super().__init__()
        self.mute_manager = mute_manager
        self.global_mute_active = False

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if not isinstance(sender, Player):
            sender.send_error_message("This command can only be executed by a player.")
            return False

        is_active = self.mute_manager.toggleGlobalMute()

        if is_active:
            sender.server.broadcast_message(f"{ColorFormat.RED}Global mute is now active. Players cannot chat.")
        else:
            sender.server.broadcast_message(f"{ColorFormat.GREEN}Global mute is now disabled. Players can chat again.")
        return True