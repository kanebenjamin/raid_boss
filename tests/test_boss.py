import unittest
from raid_boss.boss import TheManaGod, HorrorfromtheDepths, LunarChanneler


class TestBoss(unittest.TestCase):

    def test_mana_god_initialization(self):
        boss = TheManaGod(boss_name="Mana God", player_count=4)
        self.assertEqual(boss.boss_name, "Mana God")
        self.assertEqual(boss.player_count, 4)
        self.assertEqual(boss.health, 1000)
        self.assertEqual(boss.turn_count, 1)
        self.assertEqual(boss.current_attacks, [])
        self.assertEqual(boss.next_attacks, [])

    def test_horror_from_the_depths_initialization(self):
        boss = HorrorfromtheDepths(boss_name="Horror", player_count=4)
        self.assertEqual(boss.boss_name, "Horror")
        self.assertEqual(boss.player_count, 4)
        self.assertEqual(boss.health, 1000)
        self.assertEqual(boss.turn_count, 1)
        self.assertEqual(boss.current_attacks, [])
        self.assertEqual(boss.next_attacks, [])

    def test_lunar_channeler_initialization(self):
        boss = LunarChanneler(boss_name="Lunar", player_count=4)
        self.assertEqual(boss.boss_name, "Lunar")
        self.assertEqual(boss.player_count, 4)
        self.assertEqual(boss.health, 1000)
        self.assertEqual(boss.turn_count, 1)
        self.assertEqual(boss.current_attacks, [])
        self.assertEqual(boss.next_attacks, [])

    def test_mana_god_attacks(self):
        boss = TheManaGod(boss_name="Mana God", player_count=4)

        # Test various attack functions
        attack_two = boss.two()
        self.assertIn("sacrifice", attack_two.lower())

        attack_three = boss.three()
        self.assertIn("curse of confusion", attack_three.lower())

        attack_four = boss.four()
        self.assertIn("goblin zombie", attack_four.lower())

        attack_ten = boss.ten()
        self.assertIn("cleric zombie", attack_ten.lower())
        self.assertEqual(boss.health, 1016)  # 1000 + (4 * 4)

    def test_horror_from_the_depths_attacks(self):
        boss = HorrorfromtheDepths(boss_name="Horror", player_count=4)

        # Test various attack functions
        attack_two = boss.two()
        self.assertIn("return", attack_two.lower())

        attack_three = boss.three()
        self.assertIn("curse of sinking", attack_three.lower())

        attack_four = boss.four()
        self.assertIn("permanents", attack_four.lower())

        attack_six = boss.six()
        self.assertIn("tentacle", attack_six.lower())

    def test_lunar_channeler_attacks(self):
        boss = LunarChanneler(boss_name="Lunar", player_count=4)

        # Test various attack functions
        attack_two = boss.two()
        self.assertIn("spirit zombie cleric", attack_two.lower())

        attack_three = boss.three()
        self.assertIn("moon's presence", attack_three.lower())

        attack_four = boss.four()
        self.assertIn("lunar light soldiers", attack_four.lower())

        attack_twelve = boss.twelve()
        self.assertIn("emrakul", attack_twelve.lower())

    def test_mana_god_hints(self):
        boss = TheManaGod(boss_name="Mana God", player_count=4)

        # Test channeling hints
        channel_hints = boss.get_attack_hint([0, 1, 3, 7, 9])
        self.assertIn("channeling energy", channel_hints.lower())

        # Test attack hints
        attack_hints = boss.get_attack_hint([2, 4, 5, 6, 8])
        self.assertIn("amassing armies", attack_hints.lower())

        # Test healing hints
        heal_hints = boss.get_attack_hint([10])
        self.assertIn("about to heal", heal_hints.lower())

    def test_horror_from_the_depths_hints(self):
        boss = HorrorfromtheDepths(boss_name="Horror", player_count=4)

        # Test channeling hints
        channel_hints = boss.get_attack_hint([1, 2, 3, 7, 8, 9])
        self.assertIn("channeling dark energies", channel_hints.lower())

        # Test attack hints
        attack_hints = boss.get_attack_hint([4, 5, 6])
        self.assertIn("summoning beasts", attack_hints.lower())

        # Test recoil hints
        recoil_hints = boss.get_attack_hint([0, 10])
        self.assertIn("recoils", recoil_hints.lower())

    def test_lunar_channeler_hints(self):
        boss = LunarChanneler(boss_name="Lunar", player_count=4)

        # Test channeling hints
        channel_hints = boss.get_attack_hint([1, 4, 5, 6])
        self.assertIn("chanting at the moon", channel_hints.lower())

        # Test attack hints
        attack_hints = boss.get_attack_hint([2, 3, 7, 8, 9])
        self.assertIn("conjuring entities", attack_hints.lower())

        # Test special hints
        emrakul_hints = boss.get_attack_hint([10])
        self.assertIn("unsettling energy", emrakul_hints.lower())

        zombie_hints = boss.get_attack_hint([0])
        self.assertIn("ground begins to open", zombie_hints.lower())


if __name__ == "__main__":
    unittest.main()
