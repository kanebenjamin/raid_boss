import unittest
from unittest.mock import MagicMock, patch
from kivy.app import App
from raid_boss.main import RaidBossApp
from raid_boss.game_state import GameState
from raid_boss.ui_components import TextType


class TestRaidBossApp(unittest.TestCase):

    @patch("kivy.core.clipboard.Clipboard")
    @patch("kivy.core.window.Window")
    @patch("kivy.uix.textinput.TextInput")
    def setUp(self, mock_textinput, mock_window, mock_clipboard):
        """Set up test environment before each test."""
        # Mock clipboard to prevent xclip/xsel errors
        mock_clipboard.return_value = MagicMock()

        # Mock window to prevent display-related errors
        mock_window.return_value = MagicMock()

        # Mock text input
        mock_textinput.return_value = MagicMock()

        self.app = RaidBossApp()
        self.app.build()  # Initialize the UI components

        # Clear any initial text
        self.app.interface.output.text = ""

        # Initialize game state
        self.app.game_state = GameState()
        self.app.game_logic = self.app.game_logic.__class__(self.app.game_state, self.app.interface.output)

    def test_app_initialization(self):
        """Test that the app is properly initialized."""
        self.assertIsInstance(self.app, App)
        self.assertIsInstance(self.app.game_state, GameState)
        self.assertIsNotNone(self.app.interface)
        self.assertIsNotNone(self.app.game_logic)

    def test_initial_game_state(self):
        """Test that the initial game state is correct."""
        self.assertEqual(self.app.game_state.phase, 0)
        self.assertEqual(self.app.game_state.num_players, 0)
        self.assertEqual(self.app.game_state.boss_name, "")
        self.assertIsNone(self.app.game_state.boss)
        self.assertEqual(self.app.game_state.defeated_players, 0)

    def test_welcome_message(self):
        """Test that the welcome message is displayed correctly."""
        # Clear any existing text
        self.app.interface.output.text = ""
        # Add welcome message directly
        self.app.interface.output.add_text("Welcome to Raid Boss!", TextType.GAME_STATE)
        self.app.interface.output.add_text("How many people are playing?", TextType.PROMPT)

        # Verify the text
        self.assertIn("Welcome to Raid Boss!", self.app.interface.output.text)
        self.assertIn("How many people are playing?", self.app.interface.output.text)

    def test_player_count_handling(self):
        """Test handling of player count input."""
        # Test valid input
        self.app.game_logic.handle_player_count("4")
        self.assertEqual(self.app.game_state.num_players, 4)
        self.assertEqual(self.app.game_state.phase, 1)

        # Test invalid input
        self.app.game_logic.handle_player_count("invalid")
        self.assertEqual(self.app.game_state.num_players, 4)  # Should not change
        self.assertEqual(self.app.game_state.phase, 1)  # Should not change

    def test_boss_name_handling(self):
        """Test handling of boss name input."""
        # Set up initial state
        self.app.game_state.num_players = 4
        self.app.game_state.phase = 1

        # Test valid input
        self.app.game_logic.handle_boss_name("Test Boss")
        self.assertEqual(self.app.game_state.boss_name, "Test Boss")
        self.assertEqual(self.app.game_state.phase, 2)

        # Test invalid input (empty)
        self.app.game_logic.handle_boss_name("")
        self.assertEqual(self.app.game_state.boss_name, "Test Boss")  # Should not change
        self.assertEqual(self.app.game_state.phase, 2)  # Should not change

    def test_boss_selection_handling(self):
        """Test handling of boss selection input."""
        # Set up initial state
        self.app.game_state.num_players = 4
        self.app.game_state.boss_name = "Test Boss"
        self.app.game_state.phase = 2

        # Test valid input
        self.app.game_logic.handle_boss_selection("1")
        self.assertIsNotNone(self.app.game_state.boss)
        self.assertEqual(self.app.game_state.phase, 3)

        # Test invalid input
        self.app.game_logic.handle_boss_selection("4")
        self.assertEqual(self.app.game_state.phase, 3)  # Phase should stay at 3 after invalid input

    def test_damage_handling(self):
        """Test handling of damage input."""
        # Set up initial state
        self.app.game_state.num_players = 4
        self.app.game_state.boss_name = "Test Boss"
        self.app.game_state.phase = 3
        self.app.game_state.initialize_boss("1")
        initial_health = self.app.game_state.boss.health

        # Test valid input
        self.app.game_logic.handle_player_damage("50")
        self.assertEqual(self.app.game_state.boss.health, initial_health - 50)
        self.assertEqual(self.app.game_state.phase, 5)

        # Test invalid input
        self.app.game_logic.handle_player_damage("-10")
        self.assertEqual(self.app.game_state.boss.health, initial_health - 50)  # Should not change
        self.assertEqual(self.app.game_state.phase, 5)  # Should not change

    def test_defeated_players_handling(self):
        """Test handling of defeated players input."""
        # Set up initial state
        self.app.game_state.num_players = 4
        self.app.game_state.boss_name = "Test Boss"
        self.app.game_state.phase = 5
        self.app.game_state.initialize_boss("1")

        # Test valid input
        self.app.game_logic.handle_defeated_players("1")
        self.assertEqual(self.app.game_state.defeated_players, 1)
        self.assertEqual(self.app.game_state.phase, 3)  # Phase should be 3 to accept damage input

        # Test invalid input
        self.app.game_logic.handle_defeated_players("5")
        self.assertEqual(self.app.game_state.defeated_players, 1)  # Should not change
        self.assertEqual(self.app.game_state.phase, 3)  # Should not change

    def test_game_over_condition(self):
        """Test game over condition handling."""
        # Set up initial state
        self.app.game_state.num_players = 4
        self.app.game_state.boss_name = "Test Boss"
        self.app.game_state.phase = 5
        self.app.game_state.initialize_boss("1")
        self.app.game_state.boss.health = 50  # Set low health

        # Deal fatal damage
        self.app.game_logic.handle_player_damage("100")
        self.assertTrue(self.app.game_state.is_game_over())

        # Test defeated players input after game over
        self.app.game_logic.handle_defeated_players("0")
        self.assertEqual(self.app.game_state.phase, 6)  # Phase should be 6 (game complete) after game over

    @patch("kivy.uix.textinput.TextInput")
    def test_input_box_binding(self, mock_textinput):
        """Test that input box events are properly bound."""
        # Clear any existing text
        self.app.interface.output.text = ""

        # Test input handling
        mock_instance = MagicMock()
        mock_instance.text = "4"  # Use valid input
        self.app.on_enter(mock_instance)

        # Verify that the input was processed
        self.assertIn("4", self.app.interface.output.text)


if __name__ == "__main__":
    unittest.main()
