import unittest
from raid_boss.boss import TheManaGod, HorrorfromtheDepths


class TestBoss(unittest.TestCase):

    def test_mana_god_initialization(self):
        boss = TheManaGod(boss_name="Mana God", player_count=4)
        self.assertEqual(boss.boss_name, "Mana God")
        self.assertEqual(boss.player_count, 4)
        self.assertEqual(boss.health, 1000)

    def test_horror_from_the_depths_initialization(self):
        boss = HorrorfromtheDepths(boss_name="Horror", player_count=4)
        self.assertEqual(boss.boss_name, "Horror")
        self.assertEqual(boss.player_count, 4)
        self.assertEqual(boss.health, 1000)


if __name__ == "__main__":
    unittest.main()
