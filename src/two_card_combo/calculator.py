"""Probability calculations for drawing two distinct combo pieces."""

from __future__ import annotations

from dataclasses import dataclass
from math import comb


@dataclass(frozen=True)
class TwoCardComboCalculator:
    """Calculate the chance of seeing at least one copy of both card A and B."""

    deck_size: int
    card_a_copies: int
    card_b_copies: int
    cards_seen: int

    def __post_init__(self) -> None:
        values = (
            self.deck_size,
            self.card_a_copies,
            self.card_b_copies,
            self.cards_seen,
        )
        if not all(isinstance(value, int) for value in values):
            raise TypeError("all calculator values must be integers")
        if self.deck_size <= 0:
            raise ValueError("deck_size must be positive")
        if self.card_a_copies < 0 or self.card_b_copies < 0:
            raise ValueError("card copy counts cannot be negative")
        if self.card_a_copies + self.card_b_copies > self.deck_size:
            raise ValueError("card A and B copies must fit in the deck")
        if not 0 <= self.cards_seen <= self.deck_size:
            raise ValueError("cards_seen must be between 0 and deck_size")

    def success_probability(self) -> float:
        """Return the probability of seeing one or more copies of both cards."""
        total_hands = comb(self.deck_size, self.cards_seen)
        hands_without_a = self._possible_hands(
            self.deck_size - self.card_a_copies
        )
        hands_without_b = self._possible_hands(
            self.deck_size - self.card_b_copies
        )
        hands_without_either = self._possible_hands(
            self.deck_size - self.card_a_copies - self.card_b_copies
        )
        successful_hands = (
            total_hands
            - hands_without_a
            - hands_without_b
            + hands_without_either
        )
        return successful_hands / total_hands

    def _possible_hands(self, available_cards: int) -> int:
        if available_cards < self.cards_seen:
            return 0
        return comb(available_cards, self.cards_seen)
