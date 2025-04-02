from dataclasses import dataclass
from typing import Dict, Any, List
from enum import Enum, auto

class TextType(Enum):
    GAME_STATE = auto()
    BOSS_ATTACK = auto()
    PLAYER_ACTION = auto()
    ERROR = auto()
    PROMPT = auto()

@dataclass
class GameText:
    content: str
    text_type: TextType
    timestamp: float
    priority: int = 0  # Higher priority text appears first


class GameTextManager:
    """Centralized manager for all game text content."""

    def __init__(self):
        self.text_buffer: List[GameText] = []
        self.max_buffer_size = 1000  # Prevent memory issues with very long games
        self._output_callback = None

    def set_output_callback(self, callback):
        """Set the callback function to update the UI when text changes."""
        self._output_callback = callback

    def add_text(self, content: str, text_type: TextType, priority: int = 0) -> None:
        """Add new text to the buffer and update the display."""
        from time import time

        new_text = GameText(content=content, text_type=text_type, timestamp=time(), priority=priority)
        self.text_buffer.append(new_text)

        # Keep buffer size manageable
        if len(self.text_buffer) > self.max_buffer_size:
            self.text_buffer = self.text_buffer[-self.max_buffer_size :]

        # Update display
        self._update_display()

    def clear(self) -> None:
        """Clear all text from the buffer."""
        self.text_buffer.clear()
        self._update_display()

    def _update_display(self) -> None:
        """Update the display with formatted text."""
        if self._output_callback is None:
            return

        # Sort text by timestamp (oldest first) to maintain chronological order
        sorted_text = sorted(self.text_buffer, key=lambda x: x.timestamp)

        # Format text with appropriate spacing and styling
        format_map = {
            TextType.ERROR: lambda t: f"{t.content}\n\n",
            TextType.BOSS_ATTACK: lambda t: f"{t.content}\n\n",
            TextType.PROMPT: lambda t: f"{t.content}\n",
        }
        
        formatted_text = ""
        for text in sorted_text:
            formatter = format_map.get(text.text_type, lambda t: f"{t.content}\n\n")
            formatted_text += formatter(text)

        self._output_callback(formatted_text)

    @staticmethod
    def get_welcome_message() -> GameText:
        return GameText(
            content="Welcome to Raid Boss! How many people are playing? > ",
            text_type=TextType.PROMPT,
            timestamp=0,
            priority=0,
        )

    @staticmethod
    def get_player_count_confirmation(num_players: int) -> GameText:
        return GameText(
            content=f"Wonderful! {num_players} player(s) are ready to sling some spells!",
            text_type=TextType.GAME_STATE,
            timestamp=0,
            priority=0,
        )

    @staticmethod
    def get_boss_name_prompt() -> GameText:
        return GameText(
            content="Who have you come here to slay? > ", text_type=TextType.PROMPT, timestamp=0, priority=0
        )

    @staticmethod
    def get_boss_introduction(boss_name: str) -> GameText:
        return GameText(
            content=f"\nHere comes {boss_name} now! Prepare thyselves for a whimsical battle! Best of luck!",
            text_type=TextType.GAME_STATE,
            timestamp=0,
            priority=0,
        )

    @staticmethod
    def get_boss_selection_menu() -> Dict[str, GameText]:
        return {
            "header": GameText(content="\nChoose your boss:", text_type=TextType.GAME_STATE, timestamp=0, priority=0),
            "option1": GameText(content="1. TheManaGod", text_type=TextType.GAME_STATE, timestamp=0, priority=0),
            "option2": GameText(
                content="2. HorrorfromtheDepths", text_type=TextType.GAME_STATE, timestamp=0, priority=0
            ),
            "option3": GameText(content="3. LunarChanneler", text_type=TextType.GAME_STATE, timestamp=0, priority=0),
            "prompt": GameText(
                content="\nEnter your choice (1-3) > ", text_type=TextType.PROMPT, timestamp=0, priority=0
            ),
        }

    @staticmethod
    def get_boss_selection_confirmation(boss_name: str) -> GameText:
        return GameText(
            content=f"\nYou have chosen {boss_name}!", text_type=TextType.GAME_STATE, timestamp=0, priority=0
        )

    @staticmethod
    def get_battle_start(boss_name: str, health: int) -> Dict[str, GameText]:
        return {
            "announcement": GameText(
                content="The battle begins!", text_type=TextType.GAME_STATE, timestamp=0, priority=0
            ),
            "health": GameText(
                content=f"\n{boss_name}'s Health: {health}", text_type=TextType.GAME_STATE, timestamp=0, priority=0
            ),
            "prompt": GameText(
                content="PLAYER 1 TURN: Enter damage dealt! (Even if it's zero) and press enter! > ",
                text_type=TextType.PROMPT,
                timestamp=0,
                priority=0,
            ),
        }

    @staticmethod
    def get_damage_report(damage: int, boss_name: str, health: int) -> Dict[str, GameText]:
        return {
            "damage": GameText(
                content=f"\nDamage dealt: {damage}", text_type=TextType.PLAYER_ACTION, timestamp=0, priority=0
            ),
            "health": GameText(
                content=f"{boss_name}'s Health: {health}", text_type=TextType.GAME_STATE, timestamp=0, priority=0
            ),
        }

    @staticmethod
    def get_boss_rage() -> GameText:
        return GameText(
            content="\nThe boss unleashes a hellish energy...", text_type=TextType.BOSS_ATTACK, timestamp=0, priority=0
        )

    @staticmethod
    def get_boss_turn_info(boss_name: str, attack_count: int, turn_count: int) -> Dict[str, GameText]:
        return {
            "attack_count": GameText(
                content=f"\n{boss_name} gets {attack_count} roll(s) this turn! Brace yourself!",
                text_type=TextType.BOSS_ATTACK,
                timestamp=0,
                priority=0,
            ),
            "turn_count": GameText(
                content=f"TURN COUNT: {turn_count}", text_type=TextType.GAME_STATE, timestamp=0, priority=0
            ),
        }

    @staticmethod
    def get_boss_attack_announcement() -> GameText:
        return GameText(content="\nTHE BOSS ATTACKS!", text_type=TextType.BOSS_ATTACK, timestamp=0, priority=0)

    @staticmethod
    def get_boss_attack(attack_text: str) -> GameText:
        return GameText(content=f"\n{attack_text}", text_type=TextType.BOSS_ATTACK, timestamp=0, priority=0)

    @staticmethod
    def get_boss_hint() -> Dict[str, GameText]:
        return {
            "header": GameText(
                content="\nArcane intuition tells you...", text_type=TextType.GAME_STATE, timestamp=0, priority=0
            ),
            "hint": GameText(
                content="", text_type=TextType.GAME_STATE, timestamp=0, priority=0
            ),  # Content will be set dynamically
        }

    @staticmethod
    def get_defeated_players_prompt() -> GameText:
        return GameText(
            content="\nHow many players were defeated this turn? (enter 0 if no one was defeated) > ",
            text_type=TextType.PROMPT,
            timestamp=0,
            priority=0,
        )

    @staticmethod
    def get_next_player_turn(player_number: int) -> GameText:
        return GameText(
            content=f"\nPLAYER {player_number} TURN: Enter damage dealt! (Even if it's zero) and press enter! > ",
            text_type=TextType.PROMPT,
            timestamp=0,
            priority=0,
        )

    @staticmethod
    def get_game_over(boss_name: str, victory: bool) -> Dict[str, GameText]:
        if victory:
            return {
                "congrats": GameText(
                    content=f"\nCongratulations! You have defeated {boss_name}!",
                    text_type=TextType.GAME_STATE,
                    timestamp=0,
                    priority=0,
                ),
                "flavor": GameText(
                    content="They cower away from your SUPREME WHIMSY!",
                    text_type=TextType.GAME_STATE,
                    timestamp=0,
                    priority=0,
                ),
                "thanks": GameText(
                    content="Thanks for playing!", text_type=TextType.GAME_STATE, timestamp=0, priority=0
                ),
            }
        else:
            return {
                "retry": GameText(
                    content="\nRetry? Run the program again!", text_type=TextType.GAME_STATE, timestamp=0, priority=0
                )
            }

    @staticmethod
    def get_error_messages() -> Dict[str, GameText]:
        return {
            "invalid_player_count": GameText(
                content="Please enter a positive number for the number of players.",
                text_type=TextType.ERROR,
                timestamp=0,
                priority=0,
            ),
            "invalid_boss_name": GameText(
                content="Please enter a name for the boss.", text_type=TextType.ERROR, timestamp=0, priority=0
            ),
            "invalid_boss_selection": GameText(
                content="Please enter 1, 2, or 3 to select your boss.",
                text_type=TextType.ERROR,
                timestamp=0,
                priority=0,
            ),
            "invalid_damage": GameText(
                content="Please enter a non-negative number for damage.",
                text_type=TextType.ERROR,
                timestamp=0,
                priority=0,
            ),
            "invalid_defeated_players": GameText(
                content="Please enter a number between 0 and {num_players} for defeated players.",
                text_type=TextType.ERROR,
                timestamp=0,
                priority=0,
            ),
        }
