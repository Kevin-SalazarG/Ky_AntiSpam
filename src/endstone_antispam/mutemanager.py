import time
from collections import defaultdict
from endstone import Player, ColorFormat


class MuteManager:
    def __init__(self):
        self.muted_players = defaultdict(lambda: {
            "expiration_time": 0,
            "reason": "No reason provided"
        })
        self.global_mute_active = False

    def mutePlayer(self, name: str, duration: int, reason: str = "No reason provided"):
        current_time = time.time()
        expiration_time = current_time + duration
        existing_info = self.muted_players[name]
        new_expiration_time = max(existing_info["expiration_time"], expiration_time)
        self.muted_players[name] = {
            "expiration_time": new_expiration_time,
            "reason": reason
        }

    def unmutePlayer(self, name: str) -> bool:
        if name in self.muted_players:
            del self.muted_players[name]
            return True
        return False

    def isPlayerMuted(self, name: str) -> bool:
        mute_info = self.muted_players.get(name)
        if mute_info and time.time() <= mute_info["expiration_time"]:
            return True
        self.muted_players.pop(name, None)  # Remove expired mute
        return False

    def getMuteInfo(self, name: str) -> dict:
        mute_info = self.muted_players.get(name)
        if mute_info and time.time() <= mute_info["expiration_time"]:
            return {
                "expiration_time": mute_info["expiration_time"],
                "reason": mute_info["reason"],
                "remaining_time": max(0, mute_info["expiration_time"] - time.time())
            }
        return None

    def toggleGlobalMute(self) -> bool:
        self.global_mute_active = not self.global_mute_active
        return self.global_mute_active

    def isGlobalMuteActive(self) -> bool:
        return self.global_mute_active

    def getAllMutedPlayers(self) -> dict:
        current_time = time.time()
        return {
            name: {
                "expiration_time": info["expiration_time"],
                "reason": info["reason"],
                "remaining_time": max(0, info["expiration_time"] - current_time)
            }
            for name, info in self.muted_players.items()
            if current_time <= info["expiration_time"]
        }