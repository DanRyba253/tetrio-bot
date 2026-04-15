from cv2.typing import MatLike
from . import adapter as a

class Adapter(a.Adapter):
    def __init__(self, activation_key: str):
        # используйте для инициализации адаптера
        # activation_key - выбранная пользователем клавиша аквтивации/деактивации бота
        pass

    def deinit(self) -> None:
        # вызывается один раз в конце работы бота
        pass

    def wait_until_active(self) -> None:
        # должен блокировать ход программы если пользователь деактивировал бота
        # нажатием на activation_key
        # должен блокировать пока пользователь на активирует бота
        # повторным нажатием на activation_key
        raise RuntimeError("метод wait_until_active не реализован")

    def make_screenshot(self) -> None | MatLike:
        # должен возвращать скриншот экрана или игрового окна в пространстве BGR если это в данный момент возможно
        raise RuntimeError("метод make_screenshot не реализован")

    def make_moves(self, moves: str) -> None:
        # должен производить виртуальные нажатия на клавиши для каждого символа в
        # строке moves по следующему правилу:
        # |символ в moves|    клавиша    |
        # |      >       | левая стрелка |
        # |      <       | правая стрелка|
        # |      l       |       z       |
        # |      r       |       x       |
        # |      h       |       c       |
        # |      v       |    пробел     |
        raise RuntimeError("метод make_moves не реализован")
