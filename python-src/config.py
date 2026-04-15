import copy
from dataclasses import dataclass

@dataclass
class Config:
    adapter: str
    activation_key: str
    sleep_after_move_ms: int
    retry_count: int
    sleep_after_fail_ms: int
    corners_count: int
    corners_min_dist: int
    lang: str



default_config: Config = Config("Windows x64", "N", 200, 20, 200, 20, 10, "ru")

def try_parse_config(config_path: str) -> Config:
    try:
        with open(config_path, "r") as config_file:
            lines = config_file.read().splitlines()
            config = copy.copy(default_config)
            if (len(lines) > 0):
                config.adapter = lines[0]
            if (len(lines) > 1):
                config.activation_key = lines[1]
            if (len(lines) > 2):
                config.sleep_after_move_ms = int(lines[2])
            if (len(lines) > 3):
                config.retry_count = int(lines[3])
            if (len(lines) > 4):
                config.sleep_after_fail_ms = int(lines[4])
            if (len(lines) > 5):
                config.corners_count = int(lines[5])
            if (len(lines) > 6):
                config.corners_min_dist = int(lines[6])
            if (len(lines) > 7):
                config.lang = lines[7]
            return config
    except:
        return copy.copy(default_config)

def save_config(config: Config, config_path: str):
    with open(config_path, "w") as config_file:
        lines = [
            config.adapter,
            config.activation_key,
            str(config.sleep_after_move_ms),
            str(config.retry_count),
            str(config.sleep_after_fail_ms),
            str(config.corners_count),
            str(config.corners_min_dist),
            config.lang,
        ]
        for line in lines:
            config_file.write(line)
            config_file.write("\n")



