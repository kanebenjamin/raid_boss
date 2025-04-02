import unittest
from raid_boss.run import roll
import random
from collections import Counter


class TestRun(unittest.TestCase):

    def setUp(self):
        """Set up test environment before each test."""
        # Set random seed for reproducibility
        random.seed(42)

    def test_roll_range(self):
        """Test that roll result is within valid range."""
        result = roll()
        self.assertIn(result, range(0, 11))

    def test_roll_type(self):
        """Test that roll returns an integer."""
        result = roll()
        self.assertIsInstance(result, int)

    def test_multiple_rolls(self):
        """Test multiple rolls to ensure consistent behavior."""
        results = [roll() for _ in range(100)]
        for result in results:
            self.assertIn(result, range(0, 11))
            self.assertIsInstance(result, int)

    def test_roll_distribution(self):
        """Test that roll results follow expected distribution."""
        # Roll many times to get a good sample
        num_rolls = 10000
        results = [roll() for _ in range(num_rolls)]

        # Count occurrences of each value
        counts = Counter(results)

        # Check that all possible values (0-10) appear
        self.assertEqual(set(counts.keys()), set(range(11)))

        # Expected distribution for two dice (0-5 + 0-5)
        expected_distribution = {
            0: 1 / 36,  # Only (0,0)
            1: 2 / 36,  # (0,1) and (1,0)
            2: 3 / 36,  # (0,2), (1,1), (2,0)
            3: 4 / 36,  # (0,3), (1,2), (2,1), (3,0)
            4: 5 / 36,  # (0,4), (1,3), (2,2), (3,1), (4,0)
            5: 6 / 36,  # (0,5), (1,4), (2,3), (3,2), (4,1), (5,0)
            6: 5 / 36,  # (1,5), (2,4), (3,3), (4,2), (5,1)
            7: 4 / 36,  # (2,5), (3,4), (4,3), (5,2)
            8: 3 / 36,  # (3,5), (4,4), (5,3)
            9: 2 / 36,  # (4,5), (5,4)
            10: 1 / 36,  # Only (5,5)
        }

        # Check that the distribution roughly matches expected values
        for value in range(11):
            expected_count = num_rolls * expected_distribution[value]
            actual_count = counts.get(value, 0)
            # Allow 30% deviation due to randomness
            self.assertAlmostEqual(actual_count, expected_count, delta=expected_count * 0.3)

    def test_roll_independence(self):
        """Test that consecutive rolls are independent."""
        # Roll many times and check for patterns
        num_rolls = 1000
        results = [roll() for _ in range(num_rolls)]

        # Check that no value appears too many times in a row
        max_consecutive = 1
        current_consecutive = 1
        for i in range(1, len(results)):
            if results[i] == results[i - 1]:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 1

        # No value should appear more than 5 times in a row
        self.assertLess(max_consecutive, 5)

    def test_roll_edge_cases(self):
        """Test edge cases for roll function."""
        # Test minimum value (0)
        while True:
            result = roll()
            if result == 0:
                break
        self.assertEqual(result, 0)

        # Test maximum value (10)
        while True:
            result = roll()
            if result == 10:
                break
        self.assertEqual(result, 10)

    def test_roll_reproducibility(self):
        """Test that roll results are reproducible with same seed."""
        # Set seed and get first roll
        random.seed(42)
        first_roll = roll()

        # Reset seed and get second roll
        random.seed(42)
        second_roll = roll()

        # Results should be identical
        self.assertEqual(first_roll, second_roll)

    def test_roll_consistency(self):
        """Test that roll function is consistent over time."""
        # Get initial roll
        initial_roll = roll()

        # Wait a bit and get another roll
        import time

        time.sleep(0.1)
        second_roll = roll()

        # Both rolls should be valid
        self.assertIn(initial_roll, range(0, 11))
        self.assertIn(second_roll, range(0, 11))
        self.assertIsInstance(initial_roll, int)
        self.assertIsInstance(second_roll, int)


if __name__ == "__main__":
    unittest.main()
