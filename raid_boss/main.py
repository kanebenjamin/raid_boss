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


class RaidBossApp(App):
    def build(self):
        self.title = "Raid Boss"
        self.root = BoxLayout(orientation="vertical")

        self.output = Label(size_hint_y=None, height=400, text_size=(400, None))
        self.scroll = ScrollView(size_hint=(1, None), size=(400, 400))
        self.scroll.add_widget(self.output)

        self.input_box = TextInput(size_hint_y=None, height=40, multiline=False)
        self.input_box.bind(on_text_validate=self.on_enter)

        self.root.add_widget(self.scroll)
        self.root.add_widget(self.input_box)

        self.num_players = 0
        self.boss_name = ""
        self.stinky = None
        self.store_prerolls = self.preroll_boss_actions()
        self.phase = 0

        return self.root

    def preroll_boss_actions(self):
        store_prerolls = []
        for i in range(100):
            innerlist = []
            reps = math.floor(0.5 * i)
            for ii in range(reps):
                innerlist.append(self.roll())
            store_prerolls.append(innerlist)
        return store_prerolls

    def roll(self):
        DICE_ROLL = [0, 1, 2, 3, 4, 5]
        return random.choice(DICE_ROLL) + random.choice(DICE_ROLL)

    def on_enter(self, instance):
        user_input = self.input_box.text
        self.input_box.text = ""

        if self.phase == 0:
            self.num_players = int(user_input)
            self.output.text += (
                f"Welcome to Raid Boss! {self.num_players} players are playing.\n"
            )
            self.output.text += "Who have you come here to slay? > "
            self.phase = 1
        elif self.phase == 1:
            self.boss_name = user_input
            self.output.text += f"\nHere comes {self.boss_name} now! Prepare thyselves for a whimsical battle! Best of luck!\n"
            self.output.text += (
                "Choose your boss: 1 for TheManaGod, 2 for HorrorfromtheDepths > "
            )
            self.phase = 2
        elif self.phase == 2:
            if user_input == "1":
                self.stinky = boss.TheManaGod(
                    player_count=self.num_players, boss_name=self.boss_name
                )
            elif user_input == "2":
                self.stinky = boss.HorrorfromtheDepths(
                    player_count=self.num_players, boss_name=self.boss_name
                )
            self.output.text += f"\nYou have chosen {self.stinky.boss_name}!\n"
            self.phase = 3
            self.main_loop()
        else:
            self.output.text += "Invalid input. Please restart the game.\n"

    def main_loop(self):
        while self.stinky.health > 0:
            if self.stinky.health <= self.stinky.health / 2:
                self.output.text += "The boss unleashes a hellish energy...\n"

            for i in range(self.stinky.player_count):
                self.output.text += f"PLAYER {i+1} TURN: Enter damage dealt! (Even if it's zero) and press enter! > "
                self.phase = 4
                return

            self.stinky.current_attacks = self.store_prerolls[self.stinky.turn_count]
            self.stinky.next_attacks = self.store_prerolls[self.stinky.turn_count + 1]

            if len(self.stinky.current_attacks) == 0:
                self.output.text += f"{self.boss_name} cannot attack on turn 1! You're safe until next turn.\n"
            for num in self.stinky.current_attacks:
                self.stinky.text_result += (
                    "\n" + str(self.stinky.boss_funcs[num]()) + "\n"
                )

            self.output.text += f"The boss gets {len(self.stinky.current_attacks)} roll(s) this turn! Brace yourself!\n"
            self.output.text += f"TURN COUNT: {self.stinky.turn_count}\n"
            if self.stinky.turn_count != 1:
                self.output.text += (
                    f"\n\nTHE BOSS ATTACKS!\n{self.stinky.text_result}\n"
                )
            self.output.text += "Arcane intuition tells you...\n"
            self.output.text += self.stinky.get_attack_hint(self.stinky.next_attacks)

            self.output.text += "How many players were defeated this turn? (enter 0 if no one was defeated) > "
            self.phase = 5
            return

        if self.stinky.health < 0:
            self.output.text += f"Congratulations! You have defeated {self.boss_name}! They cower away from your SUPREME WHIMSY! Thanks for playing!\n"
        else:
            self.output.text += "Retry? Run the program again!\n"


if __name__ == "__main__":
    RaidBossApp().run()
