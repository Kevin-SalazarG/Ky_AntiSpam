# Ky_AntiSpam

**Ky_AntiSpam** is a plugin designed to prevent spam, control the use of capital letters, block offensive words, and manage warnings on a Minecraft Bedrock server using the Endstone API.

## Configuration

The plugin automatically generates a `config.toml` file on its first run, where you can adjust the following parameters:

```toml
blocked_words = ["fuck", "nigga", "horion.download"]   # Words blocked in chat.
message_delay = 0.5   # Minimum time (in seconds) between messages from the same player.
max_caps = 3          # Maximum number of capital letters allowed per message.
max_warns = 3         # Maximum number of warnings before a player is kicked.
kick_message = "You have been kicked for receiving too many warnings!"   # Message shown when a player is kicked for exceeding warnings.
```

## Features

- **Offensive word blocking**: Filters predefined words and cancels the message if it contains any.
- **Message rate control**: Limits how quickly a player can send messages.
- **Caps control**: Limits the number of capital letters allowed in a message, converting the rest to lowercase.
- **Warning system**: Players will receive warnings when breaking the rules and will be kicked if they exceed the warning limit.
- **Custom kick message**: You can define the message that will be displayed when a player is kicked for too many warnings.
- **/mute**: Temporarily mutes a player for a specified duration.
- **/unmute**: Unmutes a previously muted player.
- **/mutelist**: Lists all currently muted players.
- **/globalmute**: Toggles global mute for the entire server, preventing all players from sending messages while active.

## Commands

- **/mute <player: player> <duration: int> <reason: message>**: Mutes a player for the specified duration. If the player is already muted, the duration will be updated to the maximum of the new and existing duration.
- **/unmute <player: player>**: Unmutes a player.
- **/mutelist**: Displays a list of all currently muted players.
- **/globalmute**: Toggles global mute on or off for the entire server.

## Permissions

- **antispam.command.mute**: Allows the use of the `/mute` command.
- **antispam.command.unmute**: Allows the use of the `/unmute` command.
- **antispam.command.mutelist**: Allows the use of the `/mutelist` command.
- **antispam.command.globalmute**: Allows the use of the `/globalmute` command.
- **antispam.message.bypass**: Allows the player to bypass standard anti-spam restrictions such as message rate limits and duplicate message checks..
