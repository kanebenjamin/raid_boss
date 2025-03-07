import unittest
from kivy.app import App
from raid_boss.main import RaidBossApp


class TestRaidBossApp(unittest.TestCase):

    def test_app_initialization(self):
        app = RaidBossApp()
        self.assertIsInstance(app, App)


if __name__ == "__main__":
    unittest.main()
