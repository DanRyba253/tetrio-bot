from cv2.typing import MatLike

class Adapter:
    def __init__(self):
        pass

    def deinit(self):
        pass

    def wait_until_active(self) -> None:
        raise RuntimeError("метод wait_until_active не реализован")

    def make_screenshot(self) -> None | MatLike:
        raise RuntimeError("метод make_screenshot не реализован")

    def make_moves(self, moves: str) -> None:
        raise RuntimeError("метод make_moves не реализован")
