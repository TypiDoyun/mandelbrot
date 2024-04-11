import cv2
import numpy as np
from math import cos, sin, pi
from mandelbrot import render_frame, zoom
from tqdm import tqdm

frame_size = (
    int(4096 // 2),
    int(2160 // 2)
)
# frame_size = (
#     int(1024),
#     int(540)
# )
frame_center = ( element // 2 for element in frame_size )
frame_amount = 300
frame_per_second = 30

# video = cv2.VideoWriter(
#     filename = "output_video.mkv",
#     fourcc = cv2.VideoWriter_fourcc(*"FFV1"),
#     fps = frame_per_second,
#     frameSize = frame_size
# )
video = cv2.VideoWriter(
    filename = "output_video.mp4",
    fourcc = cv2.VideoWriter_fourcc(*"MJPG"),
    fps = frame_per_second,
    frameSize = frame_size
)

x_range = ( np.longdouble(-2000000), np.longdouble(1000000) )
y_range = ( np.longdouble(-1000000), np.longdouble(1000000) )
coord_center = (
    (x_range[0] + x_range[1]) / 2,
    (y_range[0] + y_range[1]) / 2,
)
point = (
    -42881.01196289065, -989774.8110245687
)

frame = np.full(
    shape = ( frame_size[1], frame_size[0], 3 ),
    fill_value = ( 0, 0, 255 ),
    dtype = np.uint8
)

t = 0

def lerf(start: list[np.longdouble], end: list[np.longdouble], t: float):
    if t == 0: return start
    elif t == 1: return end
    return [
        (1 - t) * start[0] + t * end[0],
        (1 - t) * start[1] + t * end[1],
    ]

def ease(x: float):
    return (6 * x ** 5 - 15 * x ** 4 + 10 * x ** 3); 


for current_frame in tqdm(range(frame_amount), leave = True):

    transformed_range = zoom(
        x_range,
        y_range,
        lerf(coord_center, point, ease(min(1, (t + 1) / frame_amount * 8))),
        5
    )

    x_range = transformed_range["x_range"]
    y_range = transformed_range["y_range"]

    render_frame(
        frame,
        x_range,
        y_range,
        resolution = 2048
    )

    video.write(frame)

    t += 1


video.release()
cv2.destroyAllWindows()