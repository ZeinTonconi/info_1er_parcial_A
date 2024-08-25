import math
import arcade
import pymunk
from game_logic import ImpulseVector


class Bird(arcade.Sprite):
    """
    Bird class. This represents an angry bird. All the physics is handled by Pymunk,
    the init method only set some initial properties
    """

    def __init__(
            self,
            image_path: str,
            impulse_vector: ImpulseVector,
            x: float,
            y: float,
            space: pymunk.Space,
            mass: float = 5,
            radius: float = 12,
            max_impulse: float = 100,
            power_multiplier: float = 50,
            elasticity: float = 0.8,
            friction: float = 1,
            collision_layer: int = 0,
            scale: int = 1
    ):
        super().__init__(image_path, scale)
        # body
        moment = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, moment)
        body.position = (x, y)

        impulse = min(max_impulse, impulse_vector.impulse) * power_multiplier
        impulse_pymunk = impulse * pymunk.Vec2d(1, 0)

        self.speedVector = impulse_pymunk.rotated(impulse_vector.angle)
        # apply impulse
        body.apply_impulse_at_local_point(self.speedVector)
        # shape
        shape = pymunk.Circle(body, radius)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer

        space.add(body, shape)

        self.body = body
        self.shape = shape

    def update(self):
        """
        Update the position of the bird sprite based on the physics body position
        """
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle

    def isFlying(self):
        return self.center_y > 100
    
    def power(self, sprites, birds, space):
        pass


class YellowBird(Bird):
    def __init__(
            self,
            impulse_vector: ImpulseVector,
            x: float,
            y: float,
            space: pymunk.Space,
            mass: float = 5,
            radius: float = 12,
            max_impulse: float = 100,
            power_multiplier: float = 50,
            elasticity: float = 0.8,
            friction: float = 1,
            collision_layer: int = 0,
            impulse_multiplier: int = 2
    ):
        super().__init__(
            image_path='assets/img/yellow.png',
            impulse_vector=impulse_vector,
            x=x,
            y=y,
            space=space,
            mass=mass,
            radius=radius,
            max_impulse=max_impulse,
            power_multiplier=power_multiplier,
            elasticity=elasticity,
            friction=friction,
            collision_layer=collision_layer
        )
        self.impulse = False
        self.impulse_multiplier = impulse_multiplier

    def get_impulse(self):
        return self.impulse

    def duplicate_impulse(self):
        if not self.impulse:
            self.impulse = True

            boost_impulse = self.body.mass * self.impulse_multiplier * self.body.velocity.length
            boost_vector = pymunk.Vec2d(boost_impulse, 0)
            self.body.apply_impulse_at_local_point(boost_vector.rotated(self.body.angle))
    
    def power(self, sprites, birds, space):
        self.duplicate_impulse()

class BlueBird(Bird):
    def __init__(
        self,
        impulse_vector: ImpulseVector,
        x: float,
        y: float,
        space: pymunk.Space,
        powerActivated: bool = False
     ):
         super().__init__( "assets/img/blue.png", impulse_vector, x, y, space, scale = 0.2)
         self.powerActivated = powerActivated

    def power(self, sprites, birds, space):
        if not self.powerActivated:
            degrees30 = math.pi/6

            bird = BlueBird( ImpulseVector(0,0), self.center_x, self.center_y, space, True)
            bird.body.velocity = self.body.velocity.rotated(degrees30)

            sprites.append(bird)
            birds.append(bird)

            bird = BlueBird( ImpulseVector(0,0), self.center_x, self.center_y, space, True)
            bird.body.velocity = self.body.velocity.rotated(-degrees30)

            sprites.append(bird)
            birds.append(bird)

            self.powerActivated = True


class Pig(arcade.Sprite):
    def __init__(
            self,
            x: float,
            y: float,
            space: pymunk.Space,
            mass: float = 2,
            elasticity: float = 0.8,
            friction: float = 0.4,
            collision_layer: int = 0,
    ):
        super().__init__("assets/img/pig_failed.png", 0.15)
        moment = pymunk.moment_for_circle(mass, 0, self.width / 2 - 3)
        body = pymunk.Body(mass, moment)
        body.position = (x, y)
        shape = pymunk.Circle(body, self.width / 2 - 3)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer
        space.add(body, shape)
        self.body = body
        self.shape = shape

    def update(self):
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle


class PassiveObject(arcade.Sprite):
    """
    Passive object that can interact with other objects.
    """

    def __init__(
            self,
            image_path: str,
            x: float,
            y: float,
            space: pymunk.Space,
            mass: float = 2,
            elasticity: float = 0.8,
            friction: float = 1,
            collision_layer: int = 0,
    ):
        super().__init__(image_path, 1)

        moment = pymunk.moment_for_box(mass, (self.width, self.height))
        body = pymunk.Body(mass, moment)
        body.position = (x, y)
        shape = pymunk.Poly.create_box(body, (self.width, self.height))
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer
        space.add(body, shape)
        self.body = body
        self.shape = shape

    def update(self):
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle


class Column(PassiveObject):
    def __init__(self, x, y, space):
        super().__init__("assets/img/column.png", x, y, space)

class FallenColumn(PassiveObject):
    def __init__(self, x, y, space):
        super().__init__("assets/img/beam.png", x, y, space)


class StaticObject(arcade.Sprite):
    def __init__(
            self,
            image_path: str,
            x: float,
            y: float,
            space: pymunk.Space,
            mass: float = 2,
            elasticity: float = 0.8,
            friction: float = 1,
            collision_layer: int = 0,
    ):
        super().__init__(image_path, 1)
