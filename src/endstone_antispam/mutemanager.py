import time
from endstone import Player, ColorFormat


class MuteManager:
    def __init__(self):
        self.muted_players = {}
        self.global_mute_active = False

    def mutePlayer(self, unique_idunique_id: str, duration: int, reason: str = "No reason provided"):
        current_time = time.time()
        if unique_idunique_id in self.muted_players:
            existing_info = self.muted_players[unique_idunique_id]
            new_expiration_time = max(existing_info["expiration_time"], current_time + duration)
            self.muted_players[unique_idunique_id] = {
                "expiration_time": new_expiration_time,
                "reason": reason
            }
        else:
            expiration_time = current_time + duration
            self.muted_players[unique_idunique_id] = {
                "expiration_time": expiration_time,
                "reason": reason
            }

    def unmutePlayer(self, unique_idunique_id: str):
        if unique_idunique_id in self.muted_players:
            del self.muted_players[unique_idunique_id]
            return True
        return False

    def isPlayerMuted(self, unique_id: str) -> bool:
        if unique_id in self.muted_players:
            if time.time() > self.muted_players[unique_id]["expiration_time"]:
                del self.muted_players[unique_id]
                return False
            return True
        return False

    def getMuteInfo(self, unique_id: str) -> dict:
        if self.isPlayerMuted(unique_id):
            info = self.muted_players[unique_id]
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
            unique_id: {
                "expiration_time": info["expiration_time"],
                "reason": info["reason"],
                "remaining_time": max(0, info["expiration_time"] - current_time)
            }
            for unique_id, info in self.muted_players.items()
            if current_time <= info["expiration_time"]
        }
        return active_muted_players