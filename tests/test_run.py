import unittest
from raid_boss.run import roll


class TestRun(unittest.TestCase):

    def test_roll(self):
        result = roll()
        self.assertIn(result, range(0, 11))


if __name__ == "__main__":
    unittest.main()
