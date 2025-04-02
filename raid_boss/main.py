import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now we can import from raid_boss
from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.core.clipboard.clipboard_sdl2 import ClipboardSDL2
from kivy.core.clipboard.clipboard_dummy import ClipboardDummy
from raid_boss.game_state import GameState
from raid_boss.ui_components import GameInterface, TextType
from raid_boss.game_logic import GameLogic


class RaidBossApp(App):
    def build(self):
        # Initialize game state and interface
        self.game_state = GameState()
        self.interface = GameInterface()
        self.game_logic = GameLogic(self.game_state, self.interface.output)

        # Bind input box events
        self.interface.input_box.bind(on_text_validate=self.on_enter)

        # Set up clipboard with fallback options
        self._setup_clipboard()

        # Add welcome message
        self.interface.output.add_text("Welcome to Raid Boss!", TextType.GAME_STATE)
        self.interface.output.add_text("How many people are playing?", TextType.PROMPT)

        return self.interface

    def _setup_clipboard(self):
        """Set up clipboard with fallback options."""
        try:
            # Try SDL2 first
            Clipboard.register("text", ClipboardSDL2)
        except Exception:
            try:
                # Fall back to dummy clipboard
                Clipboard.register("text", ClipboardDummy)
            except Exception:
                # If all else fails, just ignore clipboard errors
                pass

    def on_enter(self, instance):
        """Handle text input validation."""
        # Process input through game logic
        if self.game_state.phase == 0:
            self.game_logic.handle_player_count(instance.text)
        elif self.game_state.phase == 1:
            self.game_logic.handle_boss_name(instance.text)
        elif self.game_state.phase == 2:
            self.game_logic.handle_boss_selection(instance.text)
        elif self.game_state.phase == 3:
            self.game_logic.handle_player_damage(instance.text)
        elif self.game_state.phase == 5:
            self.game_logic.handle_defeated_players(instance.text)
        elif self.game_state.phase == 6:
            # Exit the game when any input is received after game over
            App.get_running_app().stop()

        # Clear input box
        instance.text = ""


if __name__ == "__main__":
    # Run the app
    RaidBossApp().run()
