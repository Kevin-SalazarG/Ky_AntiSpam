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
- **Warning system**: Players will receive warnings when breaking the rules, and will be kicked if they exceed the warning limit.
- **Custom kick message**: You can define the message that will be displayed when a player is kicked for too many warnings.

## Upcoming Features

- **/mute**: Command to temporarily mute a player.
- **/globalmute**: Command to mute the global chat.

