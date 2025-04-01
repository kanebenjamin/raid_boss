import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

import random
import math
import sys
import os

# Add the parent directory to the sys.path to handle standalone execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from raid_boss import boss
from .game_state import GameState
from .ui_components import GameInterface
from .game_logic import GameLogic


class RaidBossApp(App):
    def build(self):
        self.title = "Raid Boss"
        self.game_state = GameState()
        self.interface = GameInterface()
        self.game_logic = GameLogic(self.game_state, self.interface.output)
        
        # Bind input handler
        self.interface.input_box.bind(on_text_validate=self.on_enter)
        
        # Set initial message
        self.interface.output.text = "Welcome to Raid Boss! How many people are playing? > \n"
        
        return self.interface

    def on_enter(self, instance):
        user_input = self.interface.input_box.text
        self.interface.input_box.text = ""

        if self.game_state.phase == 0:
            self.game_logic.handle_player_count(user_input)
        elif self.game_state.phase == 1:
            self.game_logic.handle_boss_name(user_input)
        elif self.game_state.phase == 2:
            self.game_logic.handle_boss_selection(user_input)
        elif self.game_state.phase == 3:
            self.game_logic.handle_player_damage(user_input)
        elif self.game_state.phase == 4:
            self.game_logic.handle_player_damage(user_input)
        elif self.game_state.phase == 5:
            self.game_logic.handle_defeated_players(user_input)
            
            if self.game_state.is_game_over():
                self.game_logic.show_game_over()
            else:
                self.interface.output.text += f"PLAYER {self.game_state.boss.turn_count % self.game_state.num_players + 1} TURN: Enter damage dealt! (Even if it's zero) and press enter! > "
                self.game_state.phase = 4


if __name__ == "__main__":
    RaidBossApp().run()
