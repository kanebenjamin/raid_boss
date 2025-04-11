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
        self._text_templates = {
            "welcome": "Welcome to Raid Boss! How many people are playing? > ",
            "player_count": "Wonderful! {num_players} player(s) are ready to slay some spells!",
            "boss_name": "Who have you come here to slay? > ",
            "boss_intro": "\nHere comes {boss_name} now! Prepare thyselves for a whimsical battle! Best of luck!",
            "boss_selection": {
                "header": "\nChoose your boss:",
                "options": ["1. TheManaGod", "2. HorrorfromtheDepths", "3. LunarChanneler"],
                "prompt": "\nEnter your choice (1-3) > "
            },
            "boss_confirm": "\nYou have chosen {boss_name}!",
            "battle_start": {
                "announcement": "The battle begins!",
                "health": "\n{boss_name}'s Health: {health}",
                "prompt": "PLAYER 1 TURN: Enter damage dealt! (Even if it's zero) and press enter! > "
            },
            "damage_report": {
                "damage": "\nDamage dealt: {damage}",
                "health": "{boss_name}'s Health: {health}"
            },
            "boss_rage": "\nThe boss unleashes a hellish energy...",
            "boss_turn": {
                "attack_count": "\n{boss_name} gets {attack_count} roll(s) this turn! Brace yourself!",
                "turn_count": "TURN COUNT: {turn_count}"
            },
            "boss_attack": {
                "announcement": "\nTHE BOSS ATTACKS!",
                "attack": "\n{attack_text}"
            },
            "boss_hint": {
                "header": "\nArcane intuition tells you...",
                "hint": ""
            },
            "defeated_prompt": "\nHow many players were defeated this turn? (enter 0 if no one was defeated) > ",
            "next_turn": "\nPLAYER {player_number} TURN: Enter damage dealt! (Even if it's zero) and press enter! > ",
            "game_over": {
                "victory": {
                    "congrats": "\nCongratulations! You have defeated {boss_name}!",
                    "flavor": "They cower away from your SUPREME WHIMSY!",
                    "thanks": "Thanks for playing!"
                },
                "defeat": {
                    "retry": "\nRetry? Run the program again!"
                }
            },
            "errors": {
                "invalid_player_count": "Please enter a positive number for the number of players.",
                "invalid_boss_name": "Please enter a name for the boss.",
                "invalid_boss_selection": "Please enter 1, 2, or 3 to select your boss.",
                "invalid_damage": "Please enter a non-negative number for damage.",
                "invalid_defeated_players": "Please enter a number between 0 and {num_players} for defeated players."
            }
        }

    def set_output_callback(self, callback):
        """Set the callback function to update the UI when text changes."""
        self._output_callback = callback

    def add_text(self, content: str, text_type: TextType, priority: int = 0) -> None:
        """Add new text to the buffer and update the display."""
        from time import time
        new_text = GameText(content=content, text_type=text_type, timestamp=time(), priority=priority)
        self.text_buffer.append(new_text)
        if len(self.text_buffer) > self.max_buffer_size:
            self.text_buffer = self.text_buffer[-self.max_buffer_size:]
        self._update_display()

    def clear(self) -> None:
        """Clear all text from the buffer."""
        self.text_buffer.clear()
        self._update_display()

    def _update_display(self) -> None:
        """Update the display with formatted text."""
        if self._output_callback is None:
            return
        sorted_text = sorted(self.text_buffer, key=lambda x: x.timestamp)
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

    def _create_text(self, template: str, text_type: TextType, **kwargs) -> GameText:
        """Helper method to create GameText from template."""
        from time import time
        content = template.format(**kwargs) if kwargs else template
        return GameText(content=content, text_type=text_type, timestamp=time())

    def _create_text_dict(self, template_dict: Dict[str, Any], text_type: TextType, **kwargs) -> Dict[str, GameText]:
        """Helper method to create dictionary of GameText from template dictionary."""
        return {
            key: self._create_text(template, text_type, **kwargs)
            for key, template in template_dict.items()
        }

    # Public methods for game text generation
    def get_welcome_message(self) -> GameText:
        return self._create_text(self._text_templates["welcome"], TextType.PROMPT)

    def get_player_count_confirmation(self, num_players: int) -> GameText:
        return self._create_text(self._text_templates["player_count"], TextType.GAME_STATE, num_players=num_players)

    def get_boss_name_prompt(self) -> GameText:
        return self._create_text(self._text_templates["boss_name"], TextType.PROMPT)

    def get_boss_introduction(self, boss_name: str) -> GameText:
        return self._create_text(self._text_templates["boss_intro"], TextType.GAME_STATE, boss_name=boss_name)

    def get_boss_selection_menu(self) -> Dict[str, GameText]:
        templates = self._text_templates["boss_selection"]
        result = {
            "header": self._create_text(templates["header"], TextType.GAME_STATE),
            "prompt": self._create_text(templates["prompt"], TextType.PROMPT)
        }
        for i, option in enumerate(templates["options"], 1):
            result[f"option{i}"] = self._create_text(option, TextType.GAME_STATE)
        return result

    def get_boss_selection_confirmation(self, boss_name: str) -> GameText:
        return self._create_text(self._text_templates["boss_confirm"], TextType.GAME_STATE, boss_name=boss_name)

    def get_battle_start(self, boss_name: str, health: int) -> Dict[str, GameText]:
        return self._create_text_dict(
            self._text_templates["battle_start"],
            TextType.GAME_STATE,
            boss_name=boss_name,
            health=health
        )

    def get_damage_report(self, damage: int, boss_name: str, health: int) -> Dict[str, GameText]:
        return self._create_text_dict(
            self._text_templates["damage_report"],
            TextType.GAME_STATE,
            damage=damage,
            boss_name=boss_name,
            health=health
        )

    def get_boss_rage(self) -> GameText:
        return self._create_text(self._text_templates["boss_rage"], TextType.BOSS_ATTACK)

    def get_boss_turn_info(self, boss_name: str, attack_count: int, turn_count: int) -> Dict[str, GameText]:
        return self._create_text_dict(
            self._text_templates["boss_turn"],
            TextType.GAME_STATE,
            boss_name=boss_name,
            attack_count=attack_count,
            turn_count=turn_count
        )

    def get_boss_attack_announcement(self) -> GameText:
        return self._create_text(self._text_templates["boss_attack"]["announcement"], TextType.BOSS_ATTACK)

    def get_boss_attack(self, attack_text: str) -> GameText:
        return self._create_text(self._text_templates["boss_attack"]["attack"], TextType.BOSS_ATTACK, attack_text=attack_text)

    def get_boss_hint(self) -> Dict[str, GameText]:
        return self._create_text_dict(self._text_templates["boss_hint"], TextType.GAME_STATE)

    def get_defeated_players_prompt(self) -> GameText:
        return self._create_text(self._text_templates["defeated_prompt"], TextType.PROMPT)

    def get_next_player_turn(self, player_number: int) -> GameText:
        return self._create_text(self._text_templates["next_turn"], TextType.PROMPT, player_number=player_number)

    def get_game_over(self, boss_name: str, victory: bool) -> Dict[str, GameText]:
        template_key = "victory" if victory else "defeat"
        return self._create_text_dict(
            self._text_templates["game_over"][template_key],
            TextType.GAME_STATE,
            boss_name=boss_name
        )

    def get_error_messages(self) -> Dict[str, GameText]:
        return self._create_text_dict(self._text_templates["errors"], TextType.ERROR)
