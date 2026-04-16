import parser
import subprocess as sp
import time
import sys
import cv2
import config
import signal

from boardstate import Color, BoardState

def engine_interact(engine, message):
    try:
        assert(engine.stdin is not None)
        assert(engine.stdout is not None)
        engine.stdin.write(message + "\n")
        engine.stdin.flush()
    except:
        print("write to engine failed")
        return ""
    response = ""
    try:
        response = engine.stdout.readline()
    except:
        print("read from engine failed")
        return ""
    return response.strip()

def engine_send_board_state(engine, boardState: BoardState) -> str:
    message = ""
    for row in boardState.board:
        for cell in row:
            message += colorToString(cell)
    message += colorToString(boardState.current)
    for piece in boardState.future:
        message += colorToString(piece)
    message += colorToString(boardState.hold)
    return engine_interact(engine, message)

def colorToString(c: Color) -> str:
    match c:
        case Color.YELLOW:
            return 'y'
        case Color.BLUE:
            return 'b'
        case Color.RED:
            return 'r'
        case Color.GREEN:
            return 'g'
        case Color.ORANGE:
            return 'o'
        case Color.MAGENTA:
            return 'm'
        case Color.CYAN:
            return 'c'
        case Color.BLACK:
            return '_'

adapter_module = None
engine_path = ""
conf = config.try_parse_config(sys.argv[1])
if conf.adapter == "Windows x64":
    from adapters import windows
    adapter_module = windows
    engine_path = "../engine/engine-windows-x86_64.exe"

if conf.adapter == "Linux x86_64 (Niri)":
    from adapters import niri
    adapter_module = niri
    engine_path = "../engine/engine-linux-x86-64"

assert(adapter_module is not None)
assert(engine_path != "")

adapter = adapter_module.Adapter(conf.activation_key)
engine = sp.Popen([engine_path], stdin=sp.PIPE, stdout=sp.PIPE, text=True)
fail_counter = 0

def signal_handler(*_):
    adapter.deinit()
    engine.terminate()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

while True:
    adapter.wait_until_active()
    try:
        img = adapter.make_screenshot()
        assert img is not None
    except:
        print("screenshot failed")
        continue
    try:
        cv2.waitKey(0)
        boardState = parser.parseImg(img, conf.corners_count, conf.corners_min_dist)
    except:
        print("parsing failed")
        continue
    if (boardState.current == Color.BLACK):
        fail_counter += 1
        if (fail_counter >= conf.retry_count):
            adapter.make_moves("v")
            time.sleep(conf.sleep_after_fail_ms / 1000)
            fail_counter = 0
        continue
    fail_counter = 0
    response = engine_send_board_state(engine, boardState)
    print("move: ", response)
    try:
        adapter.make_moves(response)
        time.sleep(conf.sleep_after_move_ms / 1000)
    except:
        print("make move failed")
