import cv2
import numpy as np
from mandelbrot import render_frame, zoom
from tqdm import tqdm
from decimal import Decimal

frame_size = (
    int(3840),
    int(2160)
)
frame_center = ( element // 2 for element in frame_size )
frame_amount = 300
frame_per_second = 10

video = cv2.VideoWriter(
    filename = "output_video.mkv",
    fourcc = cv2.VideoWriter_fourcc(*"FFV1"),
    fps = frame_per_second,
    frameSize = frame_size
)
# video = cv2.VideoWriter(
#     filename = "output_video.avi",
#     fourcc = cv2.VideoWriter_fourcc(*"AVdn"),
#     fps = frame_per_second,
#     frameSize = frame_size
# )

x_range = ( np.longdouble(-2000000), np.longdouble(1000000) )
y_range = ( np.longdouble(-1300000), np.longdouble(1300000) )

frame = np.full(
    shape = ( frame_size[1], frame_size[0], 3 ),
    fill_value = ( 0, 0, 255 ),
    dtype = np.uint8
)

for current_frame in tqdm(range(frame_amount), leave = False):
    transformed_range = zoom(
        x_range,
        y_range,
        ( np.longdouble(-747724.8450182964), np.longdouble(-78842.67482387545) ),
        3.5
    )

    x_range = transformed_range["x_range"]
    y_range = transformed_range["y_range"]

    render_frame(
        frame,
        x_range,
        y_range,
        resolution = 512
    )

    video.write(frame)


video.release()
cv2.destroyAllWindows()