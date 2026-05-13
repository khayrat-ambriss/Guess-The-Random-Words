from enum import Enum
from typing import List, Tuple

class LetterState(Enum):
    ABSENT = "absent"
    PRESENT = "present"
    CORRECT = "correct"
    EMPTY = "empty"

class GameEngine:
    def __init__(self):
        self.target_word = ""
        self.hint = ""
        self.emoji = ""
        self.max_attempts = 6
        self.reset()

    def reset(self):
        self.attempts = []
        self.current_attempt = ""
        self.game_over = False
        self.won = False

    def set_word(self, word: str, hint: str = "", emoji: str = ""):
        self.target_word = word.lower()
        self.hint = hint
        self.emoji = emoji
        self.reset()

    def add_letter(self, char: str):
        if len(self.current_attempt) < len(self.target_word) and not self.game_over:
            self.current_attempt += char.lower()
            return True
        return False

    def remove_letter(self):
        if len(self.current_attempt) > 0 and not self.game_over:
            self.current_attempt = self.current_attempt[:-1]
            return True
        return False

    def submit_guess(self) -> Tuple[bool, List[LetterState]]:
        if len(self.current_attempt) != len(self.target_word):
            return False, []

        result = self.evaluate_guess(self.current_attempt)
        self.attempts.append((self.current_attempt, result))

        if self.current_attempt == self.target_word:
            self.won = True
            self.game_over = True
        elif len(self.attempts) >= self.max_attempts:
            self.game_over = True

        self.current_attempt = ""
        return True, result

    def evaluate_guess(self, guess: str) -> List[LetterState]:
        guess = guess.lower()
        target = list(self.target_word)
        result = [LetterState.ABSENT] * len(guess)

        # First pass: Correct letters
        for i in range(len(guess)):
            if guess[i] == target[i]:
                result[i] = LetterState.CORRECT
                target[i] = None # Mark as used

        # Second pass: Present letters
        for i in range(len(guess)):
            if result[i] != LetterState.CORRECT:
                if guess[i] in target:
                    result[i] = LetterState.PRESENT
                    target[target.index(guess[i])] = None # Mark as used

        return result

    def get_letter_states_realtime(self) -> List[LetterState]:
        """Provides real-time feedback as the user types (optional feature)"""
        result = [LetterState.EMPTY] * len(self.target_word)
        target_list = list(self.target_word)

        # This is tricky for real-time because we don't know the full guess yet.
        # But we can show what matches so far.
        for i, char in enumerate(self.current_attempt):
            if char == self.target_word[i]:
                result[i] = LetterState.CORRECT
            elif char in self.target_word:
                result[i] = LetterState.PRESENT
            else:
                result[i] = LetterState.ABSENT
        return result
