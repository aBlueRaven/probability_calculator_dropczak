"""Probability calculations for Riftbound card sequences."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from math import comb


@dataclass(frozen=True)
class PromisingFutureScenario:
    """Calculate the chance that a Promising Future chain finds an Aurora.

    ``turn`` includes the card drawn on that turn. For example, turn 2 means
    that the opening four cards and two turn draws have been seen.

    Mulliganed cards are assumed to contain neither an Aurora nor a Promising
    Future. They are on the bottom of the deck and cannot appear in this chain.
    """

    auroras_in_hand: int = 0
    promising_futures_in_hand: int = 1
    cards_mulliganed: int = 0
    turn: int = 2

    deck_size: int = 39
    opening_hand_size: int = 4
    total_auroras: int = 3
    total_promising_futures: int = 3
    promising_future_look_size: int = 5

    def __post_init__(self) -> None:
        values = (
            self.auroras_in_hand,
            self.promising_futures_in_hand,
            self.cards_mulliganed,
            self.turn,
            self.deck_size,
            self.opening_hand_size,
            self.total_auroras,
            self.total_promising_futures,
            self.promising_future_look_size,
        )
        if not all(isinstance(value, int) for value in values):
            raise TypeError("all scenario values must be integers")
        if self.deck_size <= 0:
            raise ValueError("deck_size must be positive")
        if self.opening_hand_size < 0 or self.turn < 0:
            raise ValueError("opening_hand_size and turn cannot be negative")
        if not 0 <= self.total_auroras <= self.deck_size:
            raise ValueError("total_auroras must fit in the deck")
        if not 0 <= self.total_promising_futures <= self.deck_size:
            raise ValueError("total_promising_futures must fit in the deck")
        if self.total_auroras + self.total_promising_futures > self.deck_size:
            raise ValueError("the key cards do not fit in the deck")
        if self.cards_mulliganed not in range(3):
            raise ValueError("cards_mulliganed must be 0, 1, or 2")
        if not 0 <= self.auroras_in_hand <= self.total_auroras:
            raise ValueError("auroras_in_hand is outside the available copies")
        if not 0 <= self.promising_futures_in_hand <= self.total_promising_futures:
            raise ValueError(
                "promising_futures_in_hand is outside the available copies"
            )
        if self.promising_future_look_size <= 0:
            raise ValueError("promising_future_look_size must be positive")
        if self.cards_seen > self.deck_size:
            raise ValueError("the scenario sees more cards than the deck contains")
        if self.key_cards_in_hand > self.current_hand_size:
            raise ValueError("more key cards were specified than can be in hand")
        remaining_key_cards = (
            self.auroras_remaining + self.promising_futures_remaining
        )
        if remaining_key_cards > self.cards_remaining:
            raise ValueError("the remaining key cards do not fit in the deck")

    @property
    def current_hand_size(self) -> int:
        """Number of cards held before casting the first Promising Future."""
        return self.opening_hand_size + self.turn

    @property
    def cards_seen(self) -> int:
        """Cards in hand or placed on the bottom through mulligans."""
        return self.current_hand_size + self.cards_mulliganed

    @property
    def key_cards_in_hand(self) -> int:
        return self.auroras_in_hand + self.promising_futures_in_hand

    @property
    def cards_remaining(self) -> int:
        """Cards still reachable from the top of the deck."""
        return self.deck_size - self.cards_seen

    @property
    def auroras_remaining(self) -> int:
        return self.total_auroras - self.auroras_in_hand

    @property
    def promising_futures_remaining(self) -> int:
        return self.total_promising_futures - self.promising_futures_in_hand

    def success_probability(self) -> float:
        """Return the chance that the full PF chain finds an Aurora."""
        return float(sum(self._successes_by_cast_fraction()))

    def successes_by_cast(self) -> dict[int, float]:
        """Return success probability contributed by each PF in the chain."""
        return {
            cast_number: float(probability)
            for cast_number, probability in enumerate(
                self._successes_by_cast_fraction(), start=1
            )
            if probability
        }

    def chances_to_cast(self) -> dict[int, float]:
        """Return the probability that each PF in the chain is played."""
        return {
            cast_number: float(probability)
            for cast_number, probability in enumerate(
                self._chances_to_cast_fraction(), start=1
            )
            if probability
        }

    def conditional_successes_by_cast(self) -> dict[int, float]:
        """Return each PF's hit rate among games where that PF is played."""
        successes = self._successes_by_cast_fraction()
        chances_to_cast = self._chances_to_cast_fraction()
        return {
            cast_number: float(success / chance_to_cast)
            for cast_number, (success, chance_to_cast) in enumerate(
                zip(successes, chances_to_cast), start=1
            )
            if chance_to_cast
        }

    def _successes_by_cast_fraction(self) -> tuple[Fraction, ...]:
        if self.promising_futures_in_hand == 0:
            return ()
        return self._calculate_chain_outcomes(
            self.cards_remaining,
            self.auroras_remaining,
            self.promising_futures_remaining,
            self.promising_future_look_size,
        )[0]

    def _chances_to_cast_fraction(self) -> tuple[Fraction, ...]:
        if self.promising_futures_in_hand == 0:
            return ()
        return self._calculate_chain_outcomes(
            self.cards_remaining,
            self.auroras_remaining,
            self.promising_futures_remaining,
            self.promising_future_look_size,
        )[1]

    @staticmethod
    def _calculate_chain(
        cards_remaining: int,
        auroras_remaining: int,
        futures_remaining: int,
        look_size: int,
    ) -> tuple[Fraction, ...]:
        """Return unconditional successes; retained for direct calculations."""
        return PromisingFutureScenario._calculate_chain_outcomes(
            cards_remaining,
            auroras_remaining,
            futures_remaining,
            look_size,
        )[0]

    @staticmethod
    @lru_cache(maxsize=None)
    def _calculate_chain_outcomes(
        cards_remaining: int,
        auroras_remaining: int,
        futures_remaining: int,
        look_size: int,
    ) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
        if cards_remaining == 0:
            return (Fraction(0),), (Fraction(1),)

        cards_looked_at = min(look_size, cards_remaining)
        other_cards = cards_remaining - auroras_remaining - futures_remaining
        total_reveals = comb(cards_remaining, cards_looked_at)
        successes = [Fraction(0) for _ in range(futures_remaining + 1)]
        chances_to_cast = [Fraction(0) for _ in range(futures_remaining + 1)]
        chances_to_cast[0] = Fraction(1)

        for auroras_seen in range(min(auroras_remaining, cards_looked_at) + 1):
            futures_limit = min(
                futures_remaining, cards_looked_at - auroras_seen
            )
            for futures_seen in range(futures_limit + 1):
                other_cards_seen = (
                    cards_looked_at - auroras_seen - futures_seen
                )
                if not 0 <= other_cards_seen <= other_cards:
                    continue

                reveal_probability = Fraction(
                    comb(auroras_remaining, auroras_seen)
                    * comb(futures_remaining, futures_seen)
                    * comb(other_cards, other_cards_seen),
                    total_reveals,
                )

                if auroras_seen:
                    successes[0] += reveal_probability
                elif futures_seen:
                    later_successes, later_chances_to_cast = (
                        PromisingFutureScenario._calculate_chain_outcomes(
                            cards_remaining - cards_looked_at,
                            auroras_remaining,
                            futures_remaining - futures_seen,
                            look_size,
                        )
                    )
                    for index, probability in enumerate(later_successes, start=1):
                        successes[index] += reveal_probability * probability
                    for index, probability in enumerate(
                        later_chances_to_cast, start=1
                    ):
                        chances_to_cast[index] += reveal_probability * probability

        return tuple(successes), tuple(chances_to_cast)
