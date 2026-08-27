import unittest

from hypergeometric import CardProbabilityCalculator
from promising_future import PromisingFutureScenario


class CardProbabilityCalculatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.opening_hand = CardProbabilityCalculator(60, 4, 7)

    def test_exactly_zero_matches_known_opening_hand_probability(self) -> None:
        self.assertAlmostEqual(self.opening_hand.exactly(0), 0.6005004, places=7)

    def test_at_least_one_is_complement_of_zero(self) -> None:
        self.assertAlmostEqual(
            self.opening_hand.at_least(1), 1 - self.opening_hand.exactly(0)
        )

    def test_distribution_totals_one(self) -> None:
        self.assertAlmostEqual(sum(self.opening_hand.distribution().values()), 1.0)

    def test_impossible_number_of_hits_is_zero(self) -> None:
        self.assertEqual(self.opening_hand.exactly(5), 0.0)

    def test_invalid_configuration_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            CardProbabilityCalculator(60, 61, 7)


class PromisingFutureScenarioTests(unittest.TestCase):
    def test_no_pf_in_hand_cannot_start_sequence(self) -> None:
        scenario = PromisingFutureScenario(promising_futures_in_hand=0)
        self.assertEqual(scenario.success_probability(), 0.0)

    def test_no_remaining_pf_is_a_single_five_card_search(self) -> None:
        scenario = PromisingFutureScenario(promising_futures_in_hand=3)
        expected = CardProbabilityCalculator(33, 3, 5).at_least(1)
        self.assertAlmostEqual(scenario.success_probability(), expected)
        self.assertEqual(list(scenario.successes_by_cast()), [1])

    def test_chain_can_succeed_on_each_of_three_casts(self) -> None:
        scenario = PromisingFutureScenario(promising_futures_in_hand=1)
        self.assertEqual(list(scenario.successes_by_cast()), [1, 2, 3])

    def test_conditional_success_is_based_on_games_where_pf_is_cast(self) -> None:
        scenario = PromisingFutureScenario(promising_futures_in_hand=1)
        successes = scenario.successes_by_cast()
        chances_to_cast = scenario.chances_to_cast()
        conditional_successes = scenario.conditional_successes_by_cast()

        for cast_number in successes:
            self.assertAlmostEqual(
                successes[cast_number],
                chances_to_cast[cast_number] * conditional_successes[cast_number],
            )
        self.assertGreater(conditional_successes[2], successes[2])
        self.assertGreater(conditional_successes[3], successes[3])

    def test_two_pfs_in_one_reveal_do_not_allow_a_third_cast(self) -> None:
        distribution = PromisingFutureScenario._calculate_chain(11, 1, 2, 5)

        # A third cast is possible only when exactly one of the two PFs is in
        # each earlier reveal. Seeing both in the first reveal bottoms one.
        self.assertAlmostEqual(float(distribution[2]), 5 / 99)

    def test_mulliganed_blanks_improve_search_probability(self) -> None:
        without_mulligan = PromisingFutureScenario(cards_mulliganed=0)
        with_two_mulligans = PromisingFutureScenario(cards_mulliganed=2)
        self.assertGreater(
            with_two_mulligans.success_probability(),
            without_mulligan.success_probability(),
        )


if __name__ == "__main__":
    unittest.main()
