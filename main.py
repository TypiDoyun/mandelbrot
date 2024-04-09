import cv2
import numpy as np
from mandelbrot import render_frame, zoom
from tqdm import tqdm

frame_size = (
    int(1420 // 2),
    int(1080 // 2)
)
frame_center = ( element // 2 for element in frame_size )
frame_amount = 90
frame_per_second = 15

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

x_range = ( -2000000, 1000000 )
y_range = ( -1300000, 1300000 )

frame = np.full(
    shape = ( frame_size[1], frame_size[0], 3 ),
    fill_value = ( 0, 0, 255 ),
    dtype = np.uint8
)

for current_frame in tqdm(range(frame_amount), leave = False):
    transformed_range = zoom(
        x_range,
        y_range,
        (-748600.6054641222, -184722.93474097964),
        10
    )

    x_range = transformed_range["x_range"]
    y_range = transformed_range["y_range"]

    render_frame(
        frame,
        x_range,
        y_range,
        resolution = 128
    )

    video.write(frame)


video.release()
cv2.destroyAllWindows()