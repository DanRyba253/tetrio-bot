import threading
import cv2
from cv2.typing import MatLike
from mss import mss
import numpy as np
from global_hotkeys import *
from keyboard import press_and_release as pr
import time
from . import adapter as a

class Adapter(a.Adapter):
    def __init__(self, activation_key: str):
        self.bot_active = threading.Event()
        bindings = [{
            "hotkey": activation_key,
            "on_press_callback": self.on_key_press,
            "on_release_callback": None,
        }]
        register_hotkeys(bindings)
        start_checking_hotkeys()

    def deinit(self):
        pass

    def wait_until_active(self) -> None:
        self.bot_active.wait()

    def make_screenshot(self) -> None | MatLike:
        img_bgr = None
        with mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            img_bgra = np.array(sct_img)
            img_bgr = cv2.cvtColor(img_bgra, cv2.COLOR_BGRA2BGR)
        return img_bgr

    def make_moves(self, moves: str):
        for c in moves:
            match c:
                case 'l':
                    pr("z")
                case 'r':
                    pr("x")
                case '<':
                    pr("left")
                case '>':
                    pr("right")
                case 'v':
                    pr("space")
                case 'h':
                    pr("c")

    def on_key_press(self):
        if self.bot_active.is_set():
            self.bot_active.clear()
        else:
            self.bot_active.set()

