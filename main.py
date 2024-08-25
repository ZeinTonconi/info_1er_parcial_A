import math
import logging
import arcade
import arcade.key
import pymunk

from game_object import Bird, Column, Pig, YellowBird, BlueBird
from game_logic import get_impulse_vector, Point2D, get_distance

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("arcade").setLevel(logging.WARNING)
logging.getLogger("pymunk").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

logger = logging.getLogger("main")

WIDTH = 1700
HEIGHT = 700
TITLE = "Angry birds"
GRAVITY = -900


class App(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        self.background = arcade.load_texture("assets/img/background3.png")
        # crear espacio de pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0, GRAVITY)

        # contar la cantidad de objetos en la pantalla
        self.obstacles_counter = 0

        # agregar piso
        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_shape = pymunk.Segment(floor_body, [0, 15], [WIDTH, 15], 0.0)
        floor_shape.friction = 10
        self.space.add(floor_body, floor_shape)

        self.sprites = arcade.SpriteList()
        self.birds = arcade.SpriteList()
        self.world = arcade.SpriteList()
        self.add_columns(400)
        self.add_pigs()
        self.bird_type = "red"

        slingshot = arcade.Sprite("assets/img/sling-3.png", 1)
        slingshot.position = (200, 50)
        self.sprites.append(slingshot)

        self.start_point = Point2D(160, 120)
        self.end_point = Point2D()
        self.distance = 0
        self.draw_line = False

        # agregar un collision handler
        self.handler = self.space.add_default_collision_handler()
        self.handler.post_solve = self.collision_handler

    def collision_handler(self, arbiter, space, data):
        impulse_norm = arbiter.total_impulse.length
        if impulse_norm < 100:
            return True
        logger.debug(impulse_norm)
        if impulse_norm > 1200:
            for obj in self.world:
                if obj.shape in arbiter.shapes:
                    obj.remove_from_sprite_lists()
                    self.space.remove(obj.shape, obj.body)
                    self.obstacles_counter = self.obstacles_counter - 1
                    logger.debug(f"Hay {self.obstacles_counter} obstáculos en la pantalla")
        return True

    def add_columns(self, separation):
        for x in range(WIDTH // 2, WIDTH - 300, separation):
            column = Column(x, 50, self.space)
            self.sprites.append(column)
            self.world.append(column)
            self.obstacles_counter = self.obstacles_counter + 1
            logger.debug(f"Hay {self.obstacles_counter} obstáculos en la pantalla")

    def add_pigs(self):
        pig1 = Pig(WIDTH / 2, 100, self.space)
        self.obstacles_counter = self.obstacles_counter+1
        logger.debug(f"Hay {self.obstacles_counter} obstáculos en la pantalla")
        self.sprites.append(pig1)
        self.world.append(pig1)

    def on_update(self, delta_time: float):
        self.space.step(1 / 60.0)  # actualiza la simulacion de las fisicas
        self.sprites.update()

    def isBirdFlying(self):
        for bird in self.birds:
            if bird.isFlying():
                return True
        return False

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.isBirdFlying() and button == arcade.MOUSE_BUTTON_LEFT:
            self.creatingBrid = True
            self.end_point = Point2D(x, y)
            self.draw_line = True
            logger.debug(f"Start Point: {self.start_point}")
        elif button == arcade.MOUSE_BUTTON_LEFT:
            for bird in self.birds:
                if bird.isFlying():
                    bird.power(self.sprites, self.birds, self.space)

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if self.creatingBrid and buttons == arcade.MOUSE_BUTTON_LEFT:
            self.end_point = Point2D(x, y)
            logger.debug(f"Dragging to: {self.end_point}")

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if self.creatingBrid and button == arcade.MOUSE_BUTTON_LEFT:

            logger.debug(f"Releasing from: {self.end_point}")
            self.draw_line = False
            impulse_vector = get_impulse_vector(self.start_point, self.end_point)
            if self.bird_type == "red":
                bird = Bird("assets/img/red-bird3.png", impulse_vector, x, y, self.space)
            elif self.bird_type == "yellow":
                bird = YellowBird(impulse_vector, x, y, self.space)
            else:
                bird = BlueBird(impulse_vector, x,y,self.space)

            self.sprites.append(bird)
            self.birds.append(bird)
            self.creatingBrid = False

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.KEY_1:
            self.bird_type = "red"
        elif symbol == arcade.key.KEY_2:
            self.bird_type = "yellow"
        elif symbol == arcade.key.KEY_3:
            self.bird_type = "blue"
        # pasa al siguiente nivel si ya no hay obstáculos presionando la flecha derecha
        elif symbol == arcade.key.RIGHT and self.obstacles_counter == 0:
            self.new_level()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.background)
        self.sprites.draw()
        if self.draw_line:
            arcade.draw_line(self.start_point.x, self.start_point.y, self.end_point.x, self.end_point.y,
                             arcade.color.BLACK, 3)

    def new_level(self):
        # crea un nuevo nivel
        for bird in self.birds:
            bird.remove_from_sprite_lists()
            self.space.remove(bird.shape, bird.body)

        self.birds = arcade.SpriteList()

        for obj in self.world:
            obj.remove_from_sprite_lists()
            self.space.remove(obj.shape, obj.body)

        self.obstacles_counter = 0
        self.background = arcade.load_texture("assets/img/fondo_segundo_nivel.jpg")

        self.add_columns(100)
        self.add_pigs()

def main():
    app = App()
    arcade.run()


if __name__ == "__main__":
    main()
