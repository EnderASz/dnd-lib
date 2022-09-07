import typing as t

import random


class Dice:
    def __init__(self, max_value: int, interval: int = 1, min_value: int = 1):
        self._roll = lambda: random.randrange(
            min_value,
            max_value + 1,
            interval
        )

    def roll(self, advantage: int | t.Callable[[int], int] = 0) -> int:
        result = self._roll()
        if isinstance(advantage, t.Callable):
            advantage = advantage(result)
        return result + advantage

    def __call__(self, advantage: int | t.Callable[[int], int] = 0) -> int:
        return self.roll(advantage)


COIN_FLIP = Dice(max_value=1, min_value=0)
D4 = Dice(4)
D6 = Dice(6)
D8 = Dice(8)
D10 = Dice(10)
D12 = Dice(12)
D20 = Dice(20)
D100 = Dice(100)