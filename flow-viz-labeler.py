#! /usr/bin/env python3

import copy
import math
import os
import sys

import cv2
import numpy as np

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
    global x0, y0, is_drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        is_drawing = True
        x0, y0 = x, y
        cv2.circle(params["image"], (x0, y0), 5, (0, 255, 0), -1)

    elif event == cv2.EVENT_MOUSEMOVE:
        radius =  int(math.sqrt((x - x0)**2 + (y - y0)**2))
        if is_drawing:
            cv2.circle(params["image"], (x, y), 2, (0, 0, 255), -1)

    elif event == cv2.EVENT_LBUTTONUP:
        radius =  int(math.sqrt((x - x0)**2 + (y - y0)**2))
        cv2.circle(params["image"], (x0, y0), radius, (0, 255, 0), 3)
        is_drawing = False

        record = {
            "filename": params["input_filename"],
            "center": [x0, y0],
            "radius": radius
        }
        with open(params["output_filepath"], 'a') as f:
            f.write(str(record) + "\n")


def render_image(filepath):
    try:
        img = load_image(filepath)
    except InvalidFiletypeError:
        ext = os.path.splitext(filepath)[1]
        sys.stderr(f"Found incompatible file extension {ext}. Extensions must be one among {VALID_EXTS}.")
        return

    cv2.namedWindow(IMG_PANE_NAME)
    params = {"image": img, "input_filename": os.path.basename(filepath), "output_filepath": output_filepath}
    cv2.setMouseCallback(IMG_PANE_NAME, draw_circle, params)

    while True:
        cv2.imshow(IMG_PANE_NAME, img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr(f"Usage: ./flow-viz-labeler.py <input_dir_path/input_image_path> <output_filepath>")
        sys.exit(-1)

    dirpath = sys.argv[1]
    output_filepath = sys.argv[2]

    print("[q] Quit")

    if os.path.isfile(dirpath):
        render_image(dirpath)
    elif os.path.isdir(dirpath):
        for filename in sorted(os.listdir(dirpath)):
            render_image(os.path.join(dirpath, filename))
    else:
        sys.stderr(f'Could not open file/directory at "{dirpath}".')
        sys.exit(-1)

# import numpy as np
# import cv2 as cv

# drawing = False # true if mouse is pressed
# mode = True # if True, draw rectangle. Press 'm' to toggle to curve
# ix,iy = -1,-1
# # mouse callback function
# def draw_circle(event,x,y,flags,param):
#     global ix,iy,drawing,mode
#     if event == cv.EVENT_LBUTTONDOWN:
#         drawing = True
#         ix,iy = x,y
#     elif event == cv.EVENT_MOUSEMOVE:
#         if drawing == True:
#             cv.circle(img,(x,y),5,(0,0,255),-1)
#     elif event == cv.EVENT_LBUTTONUP:
#         drawing = False

#     cv.circle(img,(x,y),5,(0,0,255),-1)

# img = np.zeros((512,512,3), np.uint8)
# cv.namedWindow('image')
# cv.setMouseCallback('image',draw_circle)

# while(1):
#     cv.imshow('image',img)
#     k = cv.waitKey(1) & 0xFF
#     if k == ord('m'):
#         mode = not mode
#     elif k == 27:
#         break

# cv.destroyAllWindows()
