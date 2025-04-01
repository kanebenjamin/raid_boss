from typing import Optional
from .game_state import GameState
from .ui_components import GameOutput

class GameLogic:
    def __init__(self, game_state: GameState, output: GameOutput):
        self.game_state = game_state
        self.output = output

    def handle_player_count(self, user_input: str) -> None:
        self.game_state.num_players = int(user_input)
        self.output.text += f"Wonderful! {self.game_state.num_players} player(s) are ready to sling some spells!\n"
        self.output.text += "Who have you come here to slay? > "
        self.game_state.phase = 1

    def handle_boss_name(self, user_input: str) -> None:
        self.game_state.boss_name = user_input
        self.output.text += f"\nHere comes {self.game_state.boss_name} now! Prepare thyselves for a whimsical battle! Best of luck!\n"
        self.output.text += "Choose your boss: 1 for TheManaGod, 2 for HorrorfromtheDepths, 3 for LunarChanneler > "
        self.game_state.phase = 2

    def handle_boss_selection(self, user_input: str) -> None:
        self.game_state.initialize_boss(user_input)
        self.output.text += f"\nYou have chosen {self.game_state.boss.boss_name}!\n"
        self.game_state.phase = 3

    def handle_player_damage(self, user_input: str) -> None:
        damage = int(user_input)
        self.game_state.process_damage(damage)
        
        if self.game_state.boss.health <= self.game_state.boss.health / 2:
            self.output.text += "The boss unleashes a hellish energy...\n"

        self.game_state.boss.current_attacks = self.game_state.store_prerolls[self.game_state.boss.turn_count]
        self.game_state.boss.next_attacks = self.game_state.store_prerolls[self.game_state.boss.turn_count + 1]

        self._process_boss_attacks()
        self._show_boss_hints()
        
        self.output.text += "How many players were defeated this turn? (enter 0 if no one was defeated) > "
        self.game_state.phase = 5

    def handle_defeated_players(self, user_input: str) -> None:
        self.game_state.defeated_players = int(user_input)
        self.game_state.boss.turn_count += 1
        self.game_state.phase = 3

    def _process_boss_attacks(self) -> None:
        if len(self.game_state.boss.current_attacks) == 0:
            self.output.text += f"{self.game_state.boss_name} cannot attack on turn 1! You're safe until next turn.\n"
        
        for num in self.game_state.boss.current_attacks:
            self.game_state.boss.text_result += "\n" + str(self.game_state.boss.boss_funcs[num]()) + "\n"

        self.output.text += f"The boss gets {len(self.game_state.boss.current_attacks)} roll(s) this turn! Brace yourself!\n"
        self.output.text += f"TURN COUNT: {self.game_state.boss.turn_count}\n"
        
        if self.game_state.boss.turn_count != 1:
            self.output.text += f"\n\nTHE BOSS ATTACKS!\n{self.game_state.boss.text_result}\n"

    def _show_boss_hints(self) -> None:
        self.output.text += "Arcane intuition tells you...\n"
        self.output.text += self.game_state.boss.get_attack_hint(self.game_state.boss.next_attacks)

    def show_game_over(self) -> None:
        if self.game_state.is_game_over():
            self.output.text += f"Congratulations! You have defeated {self.game_state.boss_name}! They cower away from your SUPREME WHIMSY! Thanks for playing!\n"
        else:
            self.output.text += "Retry? Run the program again!\n" 