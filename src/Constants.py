import math

WIDTH = 1280
HEIGHT = 720

TILE_SIZE = 48

MAP_WIDTH = WIDTH // TILE_SIZE - 3
MAP_HEIGHT = HEIGHT // TILE_SIZE

# MAP_RENDER_OFFSET_X = (WIDTH - (MAP_WIDTH * TILE_SIZE)) // 2
# MAP_RENDER_OFFSET_Y = (HEIGHT - (MAP_HEIGHT * TILE_SIZE)) // 2
MAP_RENDER_OFFSET_X = 0
MAP_RENDER_OFFSET_Y = 0

TILE_TOP_LEFT_CORNER = 54
TILE_TOP_RIGHT_CORNER = 78
TILE_BOTTOM_LEFT_CORNER = 86
TILE_BOTTOM_RIGHT_CORNER = 78

TILE_FLOORS = [
    18, 23, 66, 71,
    11, 12,
    27, 28,
]

TILE_EMPTY = 16

TILE_TOP_WALLS = [55]
TILE_BOTTOM_WALLS = [87]
TILE_LEFT_WALLS = [70]
TILE_RIGHT_WALLS = [78,97,116]

BLOCKADE = [109, 110, 111, 128]