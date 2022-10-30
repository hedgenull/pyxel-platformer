import time

import pyxel

# Constants
WINDOW_WIDTH = 128
WINDOW_HEIGHT = 148
STAGE_WIDTH = 512
STAGE_HEIGHT = 128
PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
STARTING_PLAYER_X = 8
STARTING_PLAYER_Y = 112
PLAYER_SPEED = 4
PLAYER_JUMP_SPEED = 2
MAX_PLAYER_JUMP_HEIGHT = 2 * PLAYER_HEIGHT
PLAYER_JUMP_COOLDOWN = 0.5
WALL = (2, 0)  # Location of wall tile in sprite sheet


def get_tile(tile_x, tile_y):
    return pyxel.tilemap(0).pget(tile_x, tile_y)


def is_wall(x, y):
    tile = get_tile(x // 8, y // 8)
    return tile == WALL


class Player:
    def __init__(self):
        self.x = STARTING_PLAYER_X
        self.y = STARTING_PLAYER_Y
        self.jumping_y = self.y
        self.last_jumped = time.time()
        self.jumping = True

    def check_jumping(self):
        """Make the player jump/fall."""
        if self.jumping:  # Player is jumping
            if not self.colliding("up") and self.jumping_y - self.y < MAX_PLAYER_JUMP_HEIGHT:
                self.y -= PLAYER_JUMP_SPEED
                self.jumping_y += PLAYER_JUMP_SPEED
            else:
                self.jumping = False
        elif not self.colliding("down"):  # Player is falling and not touching floor
            self.y += PLAYER_JUMP_SPEED
            self.jumping_y -= PLAYER_JUMP_SPEED

    def colliding(self, direction):
        if direction == "left":
            if is_wall(self.x - PLAYER_WIDTH // 2, self.y):
                return True
        elif direction == "right":
            if is_wall(self.x + PLAYER_WIDTH, self.y):
                return True
        elif direction == "up":
            if is_wall(self.x, self.y):
                return True
        elif direction == "down":
            if is_wall(self.x, self.y + PLAYER_HEIGHT):
                return True
        return False

    def update(self):
        """Helper function to update the player's position."""
        # Move player left
        if pyxel.btn(pyxel.KEY_LEFT) and not self.colliding("left"):
            self.x -= PLAYER_SPEED

        # Move player right
        if pyxel.btn(pyxel.KEY_RIGHT) and not self.colliding("right"):
            self.x += PLAYER_SPEED

        # Make player jump
        if pyxel.btn(pyxel.KEY_UP) and not self.jumping and time.time() - self.last_jumped > PLAYER_JUMP_COOLDOWN:
            self.jumping = True

        self.check_jumping()


class App:
    """Main application class. Instantiate to run the game."""

    def __init__(self):
        self.player = Player()
        self.camera_x = 0
        self.camera_y = 0
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT)
        pyxel.load("pyxel_game.pyxres")
        pyxel.run(self.update, self.draw)

    def _update_camera(self):
        """Helper function to update the camera's position."""
        self.camera_x = self.player.x - WINDOW_WIDTH // 2
        pyxel.camera(self.camera_x, self.camera_y)

    def update(self):
        """Update the game elements."""
        # Player movement
        self.player.update()
        self._update_camera()

    def draw(self):
        """Draw the game elements."""
        # Clear/fill the screen
        pyxel.cls(0)

        # Draw the player
        # blt(x, y, image index, column, row, width, height, transparency color)
        pyxel.blt(self.player.x, self.player.y, 0, 8, 0, PLAYER_WIDTH, PLAYER_HEIGHT, 14)

        # Draw the tilemap
        # bltm(x, y, tilemap index, column, row, width, height, transparency color)
        pyxel.bltm(0, 0, 0, 0, 0, STAGE_WIDTH, STAGE_HEIGHT, 14)

        # Debugging info
        pyxel.text(self.camera_x + 5, 5, f"X: {self.player.x}, Y: {self.player.y}", 8)
        pyxel.text(
            self.camera_x + 5,
            15,
            "\n".join([f"{d}: {self.player.colliding(d)}" for d in ["left", "right", "up", "down"]]),
            8,
        )
        pyxel.pset(self.player.x, self.player.y, 7)


App()
