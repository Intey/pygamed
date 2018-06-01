from random import random
import typing as t


def randomPos(w:int, h:int) -> t.Tuple[int, int]:
    return (int(random() * w), int(random() * h))
