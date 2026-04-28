import json


class BibleLoader:
    def __init__(self, version) -> None:
        self.dictionary: dict = self.loadVersion(version)

    def loadVersion(self, version):
        with open(
            rf".\assets\{version}\{version}_bible.json", "r", encoding="utf-8"
        ) as file:
            return json.load(file)


class Helper:
    def __init__(self, verbose) -> None:
        self.verbose = verbose

    def get_color_str(self, text, color="") -> str:
        match color:
            case "blue":
                return f"\033[34m{text}\033[0m"
            case "yellow":
                return f"\033[33m{text}\033[0m"
            case "red":
                return f"\033[31m{text}\033[0m"
            case "green":
                return f"\033[32m{text}\033[0m"
            case "purple":
                return f"\033[35m{text}\033[0m"
            case "cyan":
                return f"\033[36m{text}\033[0m"
            case "gray":
                return f"\033[37m{text}\033[0m"

            case _:
                return f"\033[37m{text}\033[0m"

    def color_print(self, text, color="", end="\n"):
        print(self.get_color_str(text, color), end=end)

    def debug_print(self, text, color="blue"):
        if not self.verbose:
            return
        self.color_print(text, color)
