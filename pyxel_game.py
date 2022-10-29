import time

import pyxel

# Constants
WINDOW_WIDTH = 128
WINDOW_HEIGHT = 128
STAGE_WIDTH = 512
STAGE_HEIGHT = 128
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 8
STARTING_PLAYER_X = 8
STARTING_PLAYER_Y = 112
PLAYER_SPEED = 4
PLAYER_JUMP_SPEED = 2
MAX_PLAYER_JUMP_HEIGHT = 2 * PLAYER_HEIGHT
PLAYER_JUMP_COOLDOWN = 0.5
WALL = (0, 2)  # Location of wall tile in sprite sheet


def get_tile(tile_x, tile_y):
    return pyxel.tilemap(0).pget(tile_x, tile_y)


class Player:
    def __init__(self):
        self.x = STARTING_PLAYER_X
        self.y = STARTING_PLAYER_Y
        self.last_jumped = time.time()
        self.jumping = 0
        self.jumping_y = 0

    def jump(self):
        """Make the player jump/fall."""
        if self.jumping == 1:
            if self.jumping_y < MAX_PLAYER_JUMP_HEIGHT and not self.colliding("up"):
                self.y -= PLAYER_JUMP_SPEED
                self.jumping_y += PLAYER_JUMP_SPEED
            else:
                self.jumping = -1
        elif self.jumping == -1 and not self.colliding("down"):
            self.y += PLAYER_JUMP_SPEED
            self.jumping_y -= PLAYER_JUMP_SPEED
            if self.jumping_y == 0:
                self.jumping = 0
            self.last_jumped = time.time()
        else:
            self.jumping_y = 0

    def colliding(self, direction):
        if direction == "left":
            if get_tile(self.x - PLAYER_WIDTH, self.y) == WALL:
                return True
        elif direction == "right":
            if get_tile(self.x + PLAYER_WIDTH, self.y) == WALL:
                return True
        elif direction == "up":
            if get_tile(self.x, self.y - PLAYER_HEIGHT) == WALL:
                return True
        elif direction == "down":
            if get_tile(self.x, self.y + PLAYER_HEIGHT) == WALL:
                return True
        return False


class App:
    """Main application class. Instantiate to run the game."""

    def __init__(self):
        self.player = Player()
        self.camera_x = 0
        self.camera_y = 0
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT)
        pyxel.load("pyxel_game.pyxres")
        pyxel.run(self.update, self.draw)

    def _update_player(self):
        """Helper function to update the player's position."""
        # Move player left
        if pyxel.btn(pyxel.KEY_LEFT) and not self.player.colliding("left"):
            self.player.x -= PLAYER_SPEED

        # Move player right
        if pyxel.btn(pyxel.KEY_RIGHT) and not self.player.colliding("right"):
            self.player.x += PLAYER_SPEED

        # self.player.jumping = -1

        if (
            pyxel.btn(pyxel.KEY_UP)
            and not self.player.jumping
            and time.time() - self.player.last_jumped > PLAYER_JUMP_COOLDOWN
        ):
            self.player.jumping = 1

        self.player.jump()

    def _update_camera(self):
        """Helper function to update the camera's position."""
        self.camera_x = self.player.x - WINDOW_WIDTH // 2
        pyxel.camera(self.camera_x, self.camera_y)

    def update(self):
        """Update the game elements."""
        # Player movement
        self._update_player()
        self._update_camera()

    def draw(self):
        """Draw the game elements."""
        # Clear/fill the screen
        pyxel.cls(0)

        # Draw the player
        # blt(x, y, image index, column, row, width, height, transparency color)
        pyxel.blt(self.player.x, self.player.y, 0, 0.4, 0.4, PLAYER_WIDTH, PLAYER_HEIGHT, 14)

        # Draw the tilemap
        # bltm(x, y, tilemap index, column, row, width, height, transparency color)
        pyxel.bltm(0, 0, 0, 0, 0, STAGE_WIDTH, STAGE_HEIGHT, 14)

        # Debugging
        pyxel.text(self.camera_x + 5, 5, f"X: {self.player.x}, Y: {self.player.y}", 7)
        pyxel.text(self.camera_x + 5, 15, f"Block: {get_tile(0, 0)}", 7)
        pyxel.tilemap(0).pset(0, 0, (0, 0))


App()
