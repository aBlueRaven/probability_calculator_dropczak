"""Object-oriented helpers for card-draw probabilities."""

from __future__ import annotations

from dataclasses import dataclass
from math import comb


@dataclass(frozen=True)
class CardProbabilityCalculator:
    """Calculate hypergeometric probabilities for drawing cards without replacement.

    Args:
        deck_size: Total number of cards in the deck.
        target_cards: Number of cards considered a success, such as copies of a card.
        cards_drawn: Number of cards drawn from the deck.
    """

    deck_size: int
    target_cards: int
    cards_drawn: int

    def __post_init__(self) -> None:
        if not all(isinstance(value, int) for value in self._parameters):
            raise TypeError("deck_size, target_cards, and cards_drawn must be integers")
        if self.deck_size < 0:
            raise ValueError("deck_size cannot be negative")
        if not 0 <= self.target_cards <= self.deck_size:
            raise ValueError("target_cards must be between 0 and deck_size")
        if not 0 <= self.cards_drawn <= self.deck_size:
            raise ValueError("cards_drawn must be between 0 and deck_size")

    @property
    def _parameters(self) -> tuple[int, int, int]:
        return self.deck_size, self.target_cards, self.cards_drawn

    @property
    def minimum_hits(self) -> int:
        """Smallest possible number of target cards in the draw."""
        return max(0, self.cards_drawn - (self.deck_size - self.target_cards))

    @property
    def maximum_hits(self) -> int:
        """Largest possible number of target cards in the draw."""
        return min(self.target_cards, self.cards_drawn)

    def exactly(self, hits: int) -> float:
        """Return the probability of drawing exactly ``hits`` target cards."""
        if not isinstance(hits, int):
            raise TypeError("hits must be an integer")
        if hits < self.minimum_hits or hits > self.maximum_hits:
            return 0.0

        misses = self.cards_drawn - hits
        outcomes = comb(self.target_cards, hits) * comb(
            self.deck_size - self.target_cards, misses
        )
        return outcomes / comb(self.deck_size, self.cards_drawn)

    def at_least(self, hits: int) -> float:
        """Return the probability of drawing ``hits`` or more target cards."""
        if not isinstance(hits, int):
            raise TypeError("hits must be an integer")
        return sum(self.exactly(count) for count in range(max(hits, self.minimum_hits), self.maximum_hits + 1))

    def at_most(self, hits: int) -> float:
        """Return the probability of drawing ``hits`` or fewer target cards."""
        if not isinstance(hits, int):
            raise TypeError("hits must be an integer")
        return sum(self.exactly(count) for count in range(self.minimum_hits, min(hits, self.maximum_hits) + 1))

    def between(self, minimum: int, maximum: int) -> float:
        """Return the probability of drawing from ``minimum`` through ``maximum`` hits."""
        if not isinstance(minimum, int) or not isinstance(maximum, int):
            raise TypeError("minimum and maximum must be integers")
        if minimum > maximum:
            raise ValueError("minimum cannot be greater than maximum")
        return sum(self.exactly(count) for count in range(max(minimum, self.minimum_hits), min(maximum, self.maximum_hits) + 1))

    def distribution(self) -> dict[int, float]:
        """Return every possible hit count and its probability."""
        return {
            hits: self.exactly(hits)
            for hits in range(self.minimum_hits, self.maximum_hits + 1)
        }
