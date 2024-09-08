import time
from endstone import Player, ColorFormat


class MuteManager:
    def __init__(self):
        self.muted_players = {}
        self.global_mute_active = False

    def mutePlayer(self, name: str, duration: int, reason: str = "No reason provided"):
        current_time = time.time()
        if name in self.muted_players:
            existing_info = self.muted_players[name]
            new_expiration_time = max(existing_info["expiration_time"], current_time + duration)
            self.muted_players[name] = {
                "expiration_time": new_expiration_time,
                "reason": reason
            }
        else:
            expiration_time = current_time + duration
            self.muted_players[name] = {
                "expiration_time": expiration_time,
                "reason": reason
            }

    def unmutePlayer(self, name: str):
        if name in self.muted_players:
            del self.muted_players[name]
            return True
        return False

    def isPlayerMuted(self, name: str) -> bool:
        if name in self.muted_players:
            if time.time() > self.muted_players[name]["expiration_time"]:
                del self.muted_players[name]
                return False
            return True
        return False

    def getMuteInfo(self, name: str) -> dict:
        if self.isPlayerMuted(name):
            info = self.muted_players[name]
            return {
                "expiration_time": info["expiration_time"],
                "reason": info["reason"],
                "remaining_time": max(0, info["expiration_time"] - time.time())
            }
        return None

    def toggleGlobalMute(self):
        self.global_mute_active = not self.global_mute_active
        return self.global_mute_active

    def isGlobalMuteActive(self) -> bool:
        return self.global_mute_active

    def getAllMutedPlayers(self) -> dict:
        current_time = time.time()
        active_muted_players = {
            name: {
                "expiration_time": info["expiration_time"],
                "reason": info["reason"],
                "remaining_time": max(0, info["expiration_time"] - current_time)
            }
            for name, info in self.muted_players.items()
            if current_time <= info["expiration_time"]
        }
        return active_muted_players