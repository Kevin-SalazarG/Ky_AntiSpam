from endstone import Player, ColorFormat
from endstone.command import CommandExecutor, CommandSender, Command


class MuteCommand(CommandExecutor):
    def __init__(self, mute_manager):
        super().__init__()
        self.mute_manager = mute_manager

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if not isinstance(sender, Player):
            sender.send_error_message("This command can only be executed by a player.")
            return False

        if len(args) < 2:
            sender.send_error_message("Usage: /mute <player: player> <duration: int> <reason: message>")
            return False

        player_name = args[0].strip('"')
        if player_name == "@s":
            target = sender
        else:
            target = sender.server.get_player(player_name)
            if target is None:
                sender.send_error_message(f"Player {player_name} not found.")
                return True

        if target == sender:
            sender.send_error_message("You cannot mute yourself.")
            return False

        try:
            duration = int(args[1])
            if duration <= 0:
                sender.send_error_message("Duration must be a positive number.")
                return False
        except ValueError:
            sender.send_error_message("Invalid duration. It must be a valid number in seconds.")
            return False

        reason = "No reason provided" if len(args) < 3 else ' '.join(args[2:])
        current_mute_info = self.mute_manager.getMuteInfo(target.unique_id)

        if current_mute_info:
            new_duration = max(duration, current_mute_info["remaining_time"])
            self.mute_manager.mutePlayer(target.unique_id, new_duration, reason)
            sender.send_message(f"{ColorFormat.GREEN}Player {ColorFormat.WHITE}{target.name} {ColorFormat.GREEN}is already muted. Duration updated to {ColorFormat.WHITE}{new_duration} {ColorFormat.GREEN}seconds.")
            target.send_message(f"{ColorFormat.RED}Your mute has been updated. New duration: {ColorFormat.WHITE}{new_duration} {ColorFormat.RED}seconds. Reason: {ColorFormat.WHITE}{reason}")
        else:
            self.mute_manager.mutePlayer(target.unique_id, duration, reason)
            sender.send_message(f"{ColorFormat.GREEN}Player {ColorFormat.WHITE}{target.name} {ColorFormat.GREEN}has been muted for {ColorFormat.WHITE}{duration} {ColorFormat.GREEN}seconds.")
            target.send_message(f"{ColorFormat.RED}You have been muted for {ColorFormat.WHITE}{duration} {ColorFormat.RED}seconds. Reason: {ColorFormat.WHITE}{reason}")

        return True