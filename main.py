from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional
from enum import Enum


class Triangle(Enum):
    Not = "Not triangle"
    Scalene = "Scalene"
    Rectangular = "Rectangular"
    Isosceles = "Isosceles"
    Equilateral = "Equilateral"


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, triangle_sides, type_triangle) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, triangle_sides, type_triangle) -> None | Triangle:
        if self._next_handler:
            return self._next_handler.handle(triangle_sides, type_triangle)

        return None


class ScaleneHandler(AbstractHandler):
    def handle(self, triangle_sides, type_triangle) -> Triangle:
        if triangle_sides[2] >= triangle_sides[0] + triangle_sides[1]:
            return type_triangle
        else:
            return super().handle(triangle_sides, Triangle.Scalene)


class RectangularHandler(AbstractHandler):
    def handle(self, triangle_sides, type_triangle) -> Triangle:
        if pow(triangle_sides[2], 2) != pow(triangle_sides[0], 2) + pow(triangle_sides[1], 2):
            return super().handle(triangle_sides, type_triangle)
        else:
            return super().handle(triangle_sides, Triangle.Rectangular)


class IsoscelesHandler(AbstractHandler):
    def handle(self, triangle_sides, type_triangle) -> Triangle:
        if triangle_sides[0] == triangle_sides[1] or triangle_sides[1] == triangle_sides[2]:
            return super().handle(triangle_sides, Triangle.Isosceles)
        else:
            return type_triangle


class EquilateralHandler(AbstractHandler):
    def handle(self, triangle_sides, type_triangle) -> Triangle:
        if triangle_sides[0] == triangle_sides[1] == triangle_sides[2]:
            return Triangle.Equilateral
        else:
            return type_triangle


def get_user_input():
    sides = []
    print("Number of elements in array:")
    while len(sides) != 3:
        try:
            sides.append(int(input()))
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")

    return sides


if __name__ == '__main__':
    sides = get_user_input()
    sides.sort()

    scalene = ScaleneHandler()
    rectangular = RectangularHandler()
    isosceles = IsoscelesHandler()
    equilateral = EquilateralHandler()

    scalene.set_next(rectangular).set_next(isosceles).set_next(equilateral)

    print(scalene.handle(sides, Triangle.Not))
