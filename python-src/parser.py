import cv2
from cv2.typing import MatLike
import numpy as np
import boardstate as bs
from boardstate import BoardState
from boardstate import Color

def parseImg(img: MatLike, corners_count: int, min_dist: int) -> BoardState:
    height, width = img.shape[:2]
    half_height = height // 2

    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(img_grey, 220, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(img_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    min_area = height * width // 1000

    for cnt in contours:
        if cv2.contourArea(cnt) < min_area:
            cv2.drawContours(img_bin, [cnt], -1, (255, 255, 255), -1)

    corners = cv2.goodFeaturesToTrack(
            img_bin[:half_height, :],
            maxCorners=corners_count,
            qualityLevel=0.01,
            minDistance=min_dist)
    assert corners is not None

    top_left = (width, 0)
    top_right = (0, 0)

    for i in np.int32(corners):
        x, y = i.ravel()
        if (x < top_left[0]):
            top_left = (x, y)
        if (x > top_right[0]):
            top_right = (x, y)

    w = top_right[0] - top_left[0]

    tl = (int(top_left[0] + w * 0.247), top_left[1])
    tr = (int(top_left[0] + w * 0.72), top_left[1])

    cell_size = (tr[0] - tl[0]) / 10

    future = (int(top_left[0] + w * 0.89), int(tl[1] + 2.7 * cell_size))

    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
    boardState = bs.initBoardState()

    for j in range(20):
        for i in range(10):
            x = int((i + 0.5) * cell_size + tl[0])
            y = int((j + 0.5) * cell_size + tl[1])
            boardState.board[j][i] = getColor(img_lab, y, x)

    for i in range(5):
        boardState.future[i] = getColor(img_lab, future[1], future[0])
        future = (future[0], int(future[1] + 3 * cell_size))

    hold = (int(top_left[0] + w * 0.12), int(tl[1] + 2.7 * cell_size))
    boardState.hold = getColor(img_lab, hold[1], hold[0])

    current_x = int(tl[0] + 4.5 * cell_size)
    current_y = int(tl[1] - 0.5 * cell_size)
    boardState.current = getColor(img_lab, current_y, current_x)

    return boardState

palete_lab = [
    [163, 126, 183],
    [87, 163, 75],
    [107, 180, 154],
    [171, 93, 185],
    [129, 156, 169],
    [133, 199, 89],
    [166,  82, 143],
    [0, 128, 128],
]


def getColor(img, y, x) -> Color:
    l, a, b = img[y, x]
    closest_index = -1
    smallest_dist = 1_000_000_000
    for i, target in enumerate(palete_lab):
        dist = (int(l)-int(target[0]))**2 + (int(a)-int(target[1]))**2 + (int(b)-int(target[2]))**2
        if (dist < smallest_dist):
            smallest_dist = dist
            closest_index = i
    return list(Color)[closest_index]


