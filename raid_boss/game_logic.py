from typing import Optional, Tuple, Any, Callable
from raid_boss.game_state import GameState
from raid_boss.ui_components import GameOutput, TextType
from raid_boss.game_text import GameTextManager


class GameLogic:
    def __init__(self, game_state: GameState, output: GameOutput):
        self.game_state = game_state
        self.output = output
        self.text_manager = GameTextManager()

    def _validate_int_input(
        self, user_input: str, min_val: int, max_val: Optional[int] = None
    ) -> Tuple[bool, Optional[int]]:
        """Validate integer input is within range."""
        try:
            value = int(user_input)
            if value < min_val:
                return False, None
            if max_val is not None and value > max_val:
                return False, None
            return True, value
        except ValueError:
            return False, None

    def _handle_invalid_input(self, error_msg: str, prompt: str) -> None:
        """Display error message and prompt for new input."""
        self.output.add_text(error_msg, TextType.ERROR)
        self.output.add_text(prompt, TextType.PROMPT)

    def _get_valid_input(
        self, user_input: str, validator: Callable[[str], Tuple[bool, Any]], error_msg: str, prompt: str
    ) -> Tuple[bool, Any]:
        """Get and validate input, handling errors."""
        is_valid, value = validator(user_input)
        if not is_valid:
            self._handle_invalid_input(error_msg, prompt)
        return is_valid, value

    def handle_player_count(self, user_input: str) -> None:
        def validate_players(input_str: str) -> Tuple[bool, Optional[int]]:
            return self._validate_int_input(input_str, min_val=1)

        is_valid, player_count = self._get_valid_input(
            user_input,
            validate_players,
            self.text_manager.get_error_messages()["invalid_player_count"].content,
            self.text_manager.get_boss_name_prompt().content,
        )

        if is_valid:
            self.game_state.num_players = player_count
            self.output.add_text(
                self.text_manager.get_player_count_confirmation(player_count).content, TextType.GAME_STATE
            )
            self.output.add_text(self.text_manager.get_boss_name_prompt().content, TextType.PROMPT)
            self.game_state.phase = 1

    def handle_boss_name(self, user_input: str) -> None:
        if not user_input.strip():
            self._handle_invalid_input(
                self.text_manager.get_error_messages()["invalid_boss_name"].content,
                self.text_manager.get_boss_name_prompt().content,
            )
            return

        self.game_state.boss_name = user_input
        self.output.add_text(self.text_manager.get_boss_introduction(user_input).content, TextType.GAME_STATE)

        # Display boss selection menu
        menu = self.text_manager.get_boss_selection_menu()
        for text in menu.values():
            self.output.add_text(text.content, text.text_type)

        self.game_state.phase = 2

    def handle_boss_selection(self, user_input: str) -> None:
        if user_input not in ["1", "2", "3"]:
            self._handle_invalid_input(
                self.text_manager.get_error_messages()["invalid_boss_selection"].content,
                self.text_manager.get_boss_selection_menu()["prompt"].content,
            )
            return

        self.game_state.initialize_boss(user_input)
        self.output.add_text(
            self.text_manager.get_boss_selection_confirmation(self.game_state.boss.boss_name).content,
            TextType.GAME_STATE,
        )

        # Display battle start information
        battle_start = self.text_manager.get_battle_start(self.game_state.boss_name, self.game_state.boss.health)
        for text in battle_start.values():
            self.output.add_text(text.content, text.text_type)

        self.game_state.phase = 3

    def handle_player_damage(self, user_input: str) -> None:
        def validate_damage(input_str: str) -> Tuple[bool, Optional[int]]:
            return self._validate_int_input(input_str, min_val=0)

        is_valid, damage = self._get_valid_input(
            user_input,
            validate_damage,
            self.text_manager.get_error_messages()["invalid_damage"].content,
            self.text_manager.get_next_player_turn(
                self.game_state.boss.turn_count % self.game_state.num_players + 1
            ).content,
        )

        if is_valid:
            self.game_state.process_damage(damage)

            # Display damage report
            damage_report = self.text_manager.get_damage_report(
                damage, self.game_state.boss_name, self.game_state.boss.health
            )
            for text in damage_report.values():
                self.output.add_text(text.content, text.text_type)

            if self.game_state.boss.health <= self.game_state.boss.health / 2:
                self.output.add_text(self.text_manager.get_boss_rage().content, TextType.BOSS_ATTACK)

            self.game_state.boss.current_attacks = self.game_state.store_prerolls[self.game_state.boss.turn_count]
            self.game_state.boss.next_attacks = self.game_state.store_prerolls[self.game_state.boss.turn_count + 1]

            self._process_boss_attacks()
            self._show_boss_hints()

            self.output.add_text(self.text_manager.get_defeated_players_prompt().content, TextType.PROMPT)
            self.game_state.phase = 5

    def handle_defeated_players(self, user_input: str) -> None:
        def validate_defeated(input_str: str) -> Tuple[bool, Optional[int]]:
            return self._validate_int_input(input_str, min_val=0, max_val=self.game_state.num_players)

        is_valid, defeated = self._get_valid_input(
            user_input,
            validate_defeated,
            self.text_manager.get_error_messages()["invalid_defeated_players"].content.format(
                num_players=self.game_state.num_players
            ),
            self.text_manager.get_defeated_players_prompt().content,
        )

        if is_valid:
            self.game_state.defeated_players = defeated
            self.game_state.boss.turn_count += 1

            # Check if all players are defeated
            if defeated >= self.game_state.num_players:
                self.output.add_text("\nAll players have been defeated! The boss wins!", TextType.GAME_STATE)
                self.show_game_over()
                return

            if self.game_state.is_game_over():
                self.show_game_over()
            else:
                self.output.add_text(
                    self.text_manager.get_next_player_turn(
                        self.game_state.boss.turn_count % self.game_state.num_players + 1
                    ).content,
                    TextType.PROMPT,
                )
                self.game_state.phase = 3  # Keep phase at 3 to accept damage input

    def _process_boss_attacks(self) -> None:
        if len(self.game_state.boss.current_attacks) == 0:
            self.output.add_text(
                f"{self.game_state.boss_name} cannot attack on turn 1! You're safe until next turn.\n\n",
                TextType.BOSS_ATTACK,
            )
            return

        # Display turn information
        turn_info = self.text_manager.get_boss_turn_info(
            self.game_state.boss_name, len(self.game_state.boss.current_attacks), self.game_state.boss.turn_count
        )
        for text in turn_info.values():
            self.output.add_text(text.content, text.text_type)

        if self.game_state.boss.turn_count != 1:
            self.output.add_text(self.text_manager.get_boss_attack_announcement().content, TextType.BOSS_ATTACK)
            for num in self.game_state.boss.current_attacks:
                self.output.add_text(
                    self.text_manager.get_boss_attack(str(self.game_state.boss.boss_funcs[num]())).content,
                    TextType.BOSS_ATTACK,
                )

    def _show_boss_hints(self) -> None:
        hint = self.text_manager.get_boss_hint()
        self.output.add_text(hint["header"].content, TextType.GAME_STATE)
        self.output.add_text(
            self.game_state.boss.get_attack_hint(self.game_state.boss.next_attacks), TextType.GAME_STATE
        )

    def show_game_over(self) -> None:
        game_over = self.text_manager.get_game_over(self.game_state.boss_name, self.game_state.is_game_over())
        for text in game_over.values():
            self.output.add_text(text.content, text.text_type)

        # Add final prompt and set phase to 6 (game complete)
        self.output.add_text("\nPress Enter to exit the game...", TextType.PROMPT)
        self.game_state.phase = 6
