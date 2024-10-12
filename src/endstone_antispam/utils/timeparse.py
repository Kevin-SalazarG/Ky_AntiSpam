import re
from typing import Dict


class TimeParse:
    TIME_UNITS: Dict[str, int] = {
        'd': 24 * 60 * 60 * 1000,
        'h': 60 * 60 * 1000,
        'm': 60 * 1000,
        's': 1000,
        'ms': 1
    }

    @staticmethod
    def parse_time_to_milliseconds(time_string: str) -> int:
        parts = re.findall(r'(\d+)([a-zA-Z]+)', time_string)
        if not parts:
            raise ValueError("No valid time unit found in string.")

        return sum(int(amount) * TimeParse.TIME_UNITS[unit.lower()]
                   for amount, unit in parts
                   if unit.lower() in TimeParse.TIME_UNITS)

    @staticmethod
    def format_time(milliseconds: int) -> str:
        if milliseconds < 0:
            raise ValueError("Milliseconds cannot be negative")

        seconds, ms = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"