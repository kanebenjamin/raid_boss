from dataclasses import dataclass
from typing import List, Optional
import math
import random

from raid_boss.boss import Boss, TheManaGod, HorrorfromtheDepths, LunarChanneler


@dataclass
class GameState:
    num_players: int = 0
    boss_name: str = ""
    boss: Optional[Boss] = None
    phase: int = 0
    store_prerolls: List[List[int]] = None
    defeated_players: int = 0

    def __init__(self):
        self.store_prerolls = self._preroll_boss_actions()

    def _preroll_boss_actions(self) -> List[List[int]]:
        return [
            [self._roll() for _ in range(math.floor(0.5 * i))]
            for i in range(100)
        ]

    @staticmethod
    def _roll() -> int:
        DICE_ROLL = [0, 1, 2, 3, 4, 5]
        return random.choice(DICE_ROLL) + random.choice(DICE_ROLL)

    def initialize_boss(self, boss_type: str) -> None:
        boss_map = {
            "1": TheManaGod,
            "2": HorrorfromtheDepths,
            "3": LunarChanneler
        }
        if boss_type in boss_map:
            self.boss = boss_map[boss_type](player_count=self.num_players, boss_name=self.boss_name)

    def process_damage(self, damage: int) -> None:
        if self.boss:
            self.boss.health -= damage

    def is_game_over(self) -> bool:
        return self.boss and self.boss.health <= 0
