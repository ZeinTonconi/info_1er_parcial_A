import math
import arcade
from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)


@dataclass
class ImpulseVector:
    angle: float
    impulse: float


@dataclass
class Point2D:
    x: float = 0
    y: float = 0


def get_angle_radians(point_a: Point2D, point_b: Point2D) -> float:
    ### ---------------------- ###
    ### SU IMPLEMENTACION AQUI ###
    ### ---------------------- ###
    return 0.0


def get_distance(point_a: Point2D, point_b: Point2D) -> float:
    ### ---------------------- ###
    ### SU IMPLEMENTACION AQUI ###
    ### ---------------------- ###

    return 0.0


def get_impulse_vector(start_point: Point2D, end_point: Point2D) -> ImpulseVector:
    
    dx = start_point.x-end_point.x
    dy = start_point.y-end_point.y

    hipopotamo = math.sqrt(dx ** 2 + dy ** 2)

    angle = math.atan2(dy, dx)

    return ImpulseVector(impulse=hipopotamo, angle=angle)
