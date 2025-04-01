from dataclasses import dataclass
from typing import List, Optional
import math
import random

from boss import Boss, TheManaGod, HorrorfromtheDepths, LunarChanneler


@dataclass
class GameState:
    num_players: int = 0
    boss_name: str = ""
    boss: Optional[Boss] = None
    phase: int = 0
    store_prerolls: List[List[int]] = None
    defeated_players: int = 0

    def __post_init__(self):
        self.store_prerolls = self._preroll_boss_actions()

    def _preroll_boss_actions(self) -> List[List[int]]:
        store_prerolls = []
        for i in range(100):
            innerlist = []
            reps = math.floor(0.5 * i)
            for _ in range(reps):
                innerlist.append(self._roll())
            store_prerolls.append(innerlist)
        return store_prerolls

    @staticmethod
    def _roll() -> int:
        DICE_ROLL = [0, 1, 2, 3, 4, 5]
        return random.choice(DICE_ROLL) + random.choice(DICE_ROLL)

    def initialize_boss(self, boss_type: str) -> None:
        if boss_type == "1":
            self.boss = TheManaGod(
                player_count=self.num_players, 
                boss_name=self.boss_name
            )
        elif boss_type == "2":
            self.boss = HorrorfromtheDepths(
                player_count=self.num_players, 
                boss_name=self.boss_name
            )
        elif boss_type == "3":
            self.boss = LunarChanneler(
                player_count=self.num_players, 
                boss_name=self.boss_name
            )

    def process_damage(self, damage: int) -> None:
        if self.boss:
            self.boss.health -= damage

    def is_game_over(self) -> bool:
        return self.boss and self.boss.health <= 0 