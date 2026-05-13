import unittest
from src.cyber_wordle.engine import GameEngine, LetterState

class TestGameEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()
        self.engine.set_word("cyber", "hint", "🤖")

    def test_evaluate_guess_all_correct(self):
        result = self.engine.evaluate_guess("cyber")
        self.assertEqual(result, [LetterState.CORRECT] * 5)

    def test_evaluate_guess_none_correct(self):
        result = self.engine.evaluate_guess("ghost")
        self.assertEqual(result, [LetterState.ABSENT] * 5)

    def test_evaluate_guess_mixed(self):
        # 'c' is correct, 'y' is correct, 'b' is correct, 'e' is correct, 'r' is correct
        # let's try 'berry'
        # c y b e r
        # b e r r y
        # b: present (index 0)
        # e: present (index 1)
        # r: present (index 2)
        # r: correct (index 3)
        # y: present (index 4)
        self.engine.set_word("cyber")
        result = self.engine.evaluate_guess("berry")
        # b: present
        # e: present
        # r: present
        # r: absent (only one 'r' in cyber)
        # y: present
        # Wait, let's re-evaluate:
        # target: c y b e r
        # guess:  b e r r y
        # r at index 3 of guess matches r at index 4 of target? No.
        # let's trace:
        # guess: b e r r y
        # target: c y b e r
        # 1st pass (correct): none
        # 2nd pass (present):
        # b (idx 0) is in cyber? Yes. target -> c y _ e r
        # e (idx 1) is in cyber? Yes. target -> c y _ _ r
        # r (idx 2) is in cyber? Yes. target -> c y _ _ _
        # r (idx 3) is in cyber? No (already used).
        # y (idx 4) is in cyber? Yes. target -> c _ _ _ _

        expected = [
            LetterState.PRESENT, # b
            LetterState.PRESENT, # e
            LetterState.PRESENT, # r
            LetterState.ABSENT,  # r (duplicate)
            LetterState.PRESENT  # y
        ]
        self.assertEqual(result, expected)

    def test_win_condition(self):
        self.engine.add_letter("c")
        self.engine.add_letter("y")
        self.engine.add_letter("b")
        self.engine.add_letter("e")
        self.engine.add_letter("r")
        success, result = self.engine.submit_guess()
        self.assertTrue(success)
        self.assertTrue(self.engine.won)
        self.assertTrue(self.engine.game_over)

    def test_lose_condition(self):
        for _ in range(6):
            self.engine.current_attempt = "wrong"
            self.engine.submit_guess()
        self.assertFalse(self.engine.won)
        self.assertTrue(self.engine.game_over)

if __name__ == "__main__":
    unittest.main()
