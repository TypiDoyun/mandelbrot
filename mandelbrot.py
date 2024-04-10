import numpy as np
from numba import njit

@njit(
    cache = True,
    fastmath = True
)
def get_diffusion_speed(c: np.cdouble, resolution: int):
    z = np.cdouble(c.real + c.imag * 1j)

    for i in range(resolution - 1):
        z = np.power(z, 2) + c

        if abs(z) > 2: return (i + 1) / resolution
    
    return -1

@njit(
    cache = True,
    fastmath = True
)
def render_frame(
    frame: np.ndarray,
    x_range: list[np.longdouble],
    y_range: list[np.longdouble],
    resolution: int
):
    frame_height, frame_width, _ = frame.shape
    for y in range(frame_height):
        coord_y = (y_range[0] + (y / (frame_height - 1)) * (y_range[1] - y_range[0])) / 1_000_000
        for x in range(frame_width):
            coord_x = (x_range[0] + (x / (frame_width - 1)) * (x_range[1] - x_range[0])) / 1_000_000

            diffusion_speed = get_diffusion_speed(
                c = np.cdouble(coord_x + coord_y * 1j),
                resolution = resolution
            )

            if diffusion_speed == -1:
                # frame[y, x] = ( 255, 255, 255 )
                frame[y, x] = ( 0, 0, 0 )
            else:
                # frame[y, x] = ( 0, 0, 0 )
                frame[y, x] = (
                    int(25 * diffusion_speed),
                    int(25 + 230 * diffusion_speed),
                    int(25 * diffusion_speed)
                )

           
def zoom(
    x_range: list[np.longdouble],
    y_range: list[np.longdouble],
    origin: list[np.longdouble],
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