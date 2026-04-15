import signal
import os
import threading
import cv2
from cv2.typing import MatLike
import subprocess as sp
import numpy as np
import time
from . import adapter as a

class Adapter(a.Adapter):
    def __init__(self, activation_key):
        self.bot_active = threading.Event()

        def signal_handler(*_):
            if (self.bot_active.is_set()):
                self.bot_active.clear()
            else:
                self.bot_active.set()

        signal.signal(signal.SIGUSR1, signal_handler)
        home = os.environ.get("HOME")
        if (home == None): return
        pid = os.getpid()
        with open(f"{home}/.config/niri/tetrio-binds.kdl", "w") as config:
            config.write(f"binds {{\n{activation_key} {{ spawn-sh \"kill -10 {pid}\"; }}\n}}")

    def deinit(self):
        home = os.environ.get("HOME")
        if (home == None): return
        with open(f"{home}/.config/niri/tetrio-binds.kdl", "w") as config:
            config.write("")

    def wait_until_active(self):
        self.bot_active.wait()

    def make_screenshot(self) -> None | MatLike:
        screenshot_process = sp.Popen(
            [ "grim", "-t", "ppm", "-" ],
            stdout=sp.PIPE, 
            stderr=sp.PIPE,
            bufsize=10**8
        )
        stdout, stderr = screenshot_process.communicate()

        if stderr:
            print(f"Error: {stderr}")
            return None

        img_np = np.frombuffer(stdout, dtype=np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        return img

    def make_moves(self, moves: str):
        command = ["ydotool", "key"]
        keys = []
        for c in moves:
            match c:
                case 'l':
                    keys.extend(["44:1", "44:0"])
                case 'r':
                    keys.extend(["45:1", "45:0"])
                case '<':
                    keys.extend(["105:1", "105:0"])
                case '>':
                    keys.extend(["106:1", "106:0"])
                case 'v':
                    keys.extend(["57:1", "57:0"])
                case 'h':
                    keys.extend(["46:1", "46:0"])
        if (len(keys) == 0): return
        command.extend(keys)
        sp.run(command)

