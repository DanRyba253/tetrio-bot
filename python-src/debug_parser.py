import cv2
import numpy as np

def debug_parser(corners_count: int, min_dist: int, title: str):
    img = cv2.imread("../screenshot.png")
    assert(img is not None)

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

    cv2.circle(img, tl, 3, (0, 0, 255), -1)
    cv2.circle(img, tr, 3, (0, 0, 255), -1)

    cv2.imshow(title, img)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        try:
            if cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) < 1:
                break
        except: break

    cv2.destroyAllWindows()

