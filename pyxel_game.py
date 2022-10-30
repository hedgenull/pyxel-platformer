import time

import pyxel

# Constants
WINDOW_WIDTH = 148
WINDOW_HEIGHT = 129
STAGE_WIDTH = 1024
STAGE_HEIGHT = 129
SCROLL_BORDER_X = 80
PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
STARTING_PLAYER_X = 105 * 8
STARTING_PLAYER_Y = 8
PLAYER_SPEED = 2
PLAYER_JUMP_SPEED = 6
JUMP_COOLDOWN_SECONDS = 0.5
BRICKS = (2, 0)  # Location of wall tile in sprite sheet
PLATFORM = (2, 1)
scroll_x = 0


def get_tile(tile_x, tile_y):
    return pyxel.tilemap(0).pget(tile_x, tile_y)


def is_wall(x, y):
    tile = get_tile(x // 8, y // 8)
    return tile == BRICKS


def detect_collision(x, y, dy, tiles=None):
    if tiles is None:
        tiles = [BRICKS, PLATFORM]
    x1 = x // 8
    y1 = y // 8
    x2 = (x + 8 - 1) // 8
    y2 = (y + 8 - 1) // 8
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if get_tile(xi, yi) in tiles:
                return True
    if dy > 0 and y % 8 == 1:
        for xi in range(x1, x2 + 1):
            if get_tile(xi, y1 + 1) in tiles:
                return True
    return False


def push_back(x, y, dx, dy):
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    if abs_dx > abs_dy:
        sign = 1 if dx > 0 else -1
        for _ in range(abs_dx):
            if detect_collision(x + sign, y, dy):
                break
            x += sign
        sign = 1 if dy > 0 else -1
        for _ in range(abs_dy):
            if detect_collision(x, y + sign, dy):
                break
            y += sign
    else:
        sign = 1 if dy > 0 else -1
        for _ in range(abs_dy):
            if detect_collision(x, y + sign, dy):
                break
            y += sign
        sign = 1 if dx > 0 else -1
        for _ in range(abs_dx):
            if detect_collision(x + sign, y, dy):
                break
            x += sign
    return x, y, dx, dy


class Player:
    def __init__(self):
        self.x = STARTING_PLAYER_X
        self.y = STARTING_PLAYER_Y
        self.dx = 0
        self.dy = 0
        self.direction = 1
        self.is_falling = False
        self.last_jumped = 0

    def update(self):
        global scroll_x
        last_y = self.y
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.dx = -PLAYER_SPEED
            self.direction = -1

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.dx = PLAYER_SPEED
            self.direction = 1

        self.dy = min(self.dy + 1, 3)

        if (
            (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A))
            and time.time() - self.last_jumped > JUMP_COOLDOWN_SECONDS
            and not self.is_falling
        ):
            self.dy = -PLAYER_JUMP_SPEED
            self.last_jumped = time.time()

        self.x, self.y, self.dx, self.dy = push_back(self.x, self.y, self.dx, self.dy)
        if self.x - SCROLL_BORDER_X < scroll_x:
            scroll_x = self.x - SCROLL_BORDER_X
        self.y = max(self.y, 0)
        self.dx = int(self.dx * 0.8)
        self.is_falling = self.y > last_y

        if self.x > scroll_x + SCROLL_BORDER_X:
            scroll_x = min(self.x - SCROLL_BORDER_X, 240 * 8)


class App:
    """Main application class. Instantiate to run the game."""

    def __init__(self):
        self.player = Player()
        self.end = False
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="Pyxel Platformer")
        pyxel.load("pyxel_game.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        """Update the game elements."""
        if not self.end:
            # Player movement
            self.player.update()
            if detect_collision(self.player.x, self.player.y, self.player.dy, [(1, 1)]):
                # Touched the portal!!!
                self.end = True
        elif pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        """Draw the game elements."""
        if not self.end:
            # Clear/fill the screen
            pyxel.cls(0)
            pyxel.camera(scroll_x, 0)

            # Draw the player
            # blt(x, y, image index, column, row, width, height, transparency color)
            pyxel.blt(self.player.x, self.player.y, 0, 8, 0, PLAYER_WIDTH, PLAYER_HEIGHT, 14)

            # Draw the tilemap
            # bltm(x, y, tilemap index, column, row, width, height, transparency color)
            pyxel.bltm(0, 0, 0, 0, 0, STAGE_WIDTH, STAGE_HEIGHT, 14)
        else:
            pyxel.cls(0)
            pyxel.camera()
            pyxel.text(5, 5, "You Won!!!\nThanks for playing!\n[Q]uit\n\n\nPyxel Platformer by Hedge Fleming", 8)


App()
