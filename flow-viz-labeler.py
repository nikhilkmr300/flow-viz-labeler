#! /usr/bin/env python3

import math
import os
import sys

import cv2

VALID_EXTS = {".png", ".jpg", ".jpeg"}
IMG_PANE_NAME = "Vortices"


class InvalidFiletypeError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def load_image(filepath):
    ext = os.path.splitext(filepath)[1]
    if ext not in VALID_EXTS:
        raise InvalidFiletypeError(
            f"Files must have extension among {VALID_EXTS}. Found {ext}."
        )
    img = cv2.imread(filepath)
    if img is None:
        raise FileNotFoundError(f'Could not open image at "{filepath}".')

    return cv2.putText(img, filepath, (50, 50), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 3)

x0, y0 = -1, -1     # Circle center
is_drawing = False
def draw_circle(event, x, y, flags, params):
    global x0, y0, is_drawing, img

    if event == cv2.EVENT_LBUTTONDOWN:
        is_drawing = True
        x0, y0 = x, y
        print("L down")

    elif event == cv2.EVENT_MOUSEMOVE:
        radius =  int(math.sqrt((x - x0)**2 + (y - y0)**2))
        if is_drawing:
            print(f"center={(x0, y0)}, radius={radius}")
            cv2.circle(img, (x0, y0), radius, (0, 0, 255), 3)

    elif event == cv2.EVENT_LBUTTONUP:
        radius =  int(math.sqrt((x - x0)**2 + (y - y0)**2))
        cv2.circle(img, (x0, y0), radius, (0, 0, 255), -1)
        is_drawing = False
        print("L up")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr(f"Usage: ./flow-viz-labeler.py <path>")
        sys.exit(-1)

    dirpath = sys.argv[1]

    if os.path.isfile(dirpath):
        img = load_image(dirpath)
        cv2.imshow(IMG_PANE_NAME, img)
        cv2.waitKey(0)

    elif os.path.isdir(dirpath):
        for filename in sorted(os.listdir(dirpath)):
            try:
                img = load_image(os.path.join(dirpath, filename))
                cv2.imshow(IMG_PANE_NAME, img)
                cv2.setMouseCallback(IMG_PANE_NAME, draw_circle)
                cv2.waitKey(0)
            except InvalidFiletypeError:
                sys.stderr(
                    f'File has invalid type: "{filename}". Files must have extension among {VALID_EXTS}.'
                )

    else:
        sys.stderr(f'Could not open file/directory at "{dirpath}".')
        sys.exit(-1)
