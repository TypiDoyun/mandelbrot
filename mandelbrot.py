import numpy as np
from tqdm import tqdm

def get_diffusion_speed(c: complex, resolution: int):
    z = complex(c.real, c.imag)

    for i in range(resolution - 1):
        z = pow(z, 2) + c

        if abs(z) > 2: return (i + 1) / resolution
    
    return -1

def render_frame(
    frame: np.ndarray,
    x_range: list[int],
    y_range: list[int],
    resolution: int
):
    frame_height, frame_width, _ = frame.shape
    for y in tqdm(range(frame_height), leave = False):
        coord_y = (y_range[0] + (y / (frame_height - 1)) * (y_range[1] - y_range[0])) / 1_000_000
        for x in range(frame_width):
            coord_x = (x_range[0] + (x / (frame_width - 1)) * (x_range[1] - x_range[0])) / 1_000_000

            diffusion_speed = get_diffusion_speed(
                c = complex( coord_x, coord_y ),
                resolution = resolution
            )

            if diffusion_speed == -1:
                frame[y, x] = ( 255, 255, 255 )
                # frame[y, x] = ( 0, 0, 0 )
            else:
                frame[y, x] = ( 0, 0, 0 )
                # frame[y, x] = (
                #     int(25 * diffusion_speed),
                #     int(25 * diffusion_speed),
                #     int(25 + 230 * diffusion_speed)
                # )


                
def zoom(
    x_range: list[int],
    y_range: list[int],
    origin: list[float],
    p: float
):
    transformed_x_range = (
        (x_range[0] - x_range[1]) * (1 - p / 100) / 2 + origin[0],
        (x_range[1] - x_range[0]) * (1 - p / 100) / 2 + origin[0],
    )

    transformed_y_range = (
        (y_range[0] - y_range[1]) * (1 - p / 100) / 2 + origin[1],
        (y_range[1] - y_range[0]) * (1 - p / 100) / 2 + origin[1],
    )

    return {
        "x_range": transformed_x_range,
        "y_range": transformed_y_range
    }