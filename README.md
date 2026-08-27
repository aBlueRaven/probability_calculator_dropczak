# Hypergeometric Card Calculator

A small, dependency-free Python project for calculating the chance of drawing cards from a deck without replacement.

### Use `python calculate_two_drops.py --help` or `python calculate_promising_future.py --help` to see all available flags.

## Project structure

Python files and functions use `snake_case`, while classes use `PascalCase`.
Reusable probability logic lives in domain-named modules, runnable scripts begin
with the verb `calculate`, and test files begin with `test_`:

- `hypergeometric.py`: defines `CardProbabilityCalculator`.
- `promising_future.py`: defines `PromisingFutureScenario`.
- `calculate_two_drops.py`: runs the two-drop calculation.
- `calculate_promising_future.py`: runs the Promising Future calculation.
- `test_calculators.py`: contains the automated tests.

## Usage

```python
from hypergeometric import CardProbabilityCalculator

# 39-card deck, 3 copies of a card, 6 cards drawn.
calculator = CardProbabilityCalculator(39, 3, 6)

print(calculator.at_least(1))  # Chance of seeing one or more copies.
print(calculator.exactly(2))   # Chance of seeing exactly two copies.
print(calculator.at_most(1))   # Chance of seeing zero or one copy.
print(calculator.between(1, 3))
print(calculator.distribution())
```

Run the two-drop calculator with its defaults:

```bash
python calculate_two_drops.py
```

Override any default with flags named after the calculator variables:

```bash
python calculate_two_drops.py --deck_size 39 --target_cards 8 --mulliganed 2 --turn 2
```

The two-drop calculator counts the four-card opening hand, mulliganed cards, and
one card drawn per turn. With two cards mulliganed on turn 2, it calculates the
chance of finding a target among eight seen cards.

Run the tests with:

```bash
python -m unittest -v
```

## Riftbound Promising Future chains

`PromisingFutureScenario` calculates the chance that one or more chained
Promising Futures find an Aurora. It uses Riftbound defaults: a 39-card deck,
three Auroras, three Promising Futures, a four-card opening hand, and five cards
revealed by each Promising Future.

```python
from promising_future import PromisingFutureScenario

scenario = PromisingFutureScenario(
    auroras_in_hand=0,
    promising_futures_in_hand=1,
    cards_mulliganed=2,
    turn=2,
)

print(f"Any PF finds Aurora: {scenario.success_probability():.2%}")
print(scenario.successes_by_cast())
```

The turn number includes that turn's draw, so turn 2 means six cards have been
drawn into your hand. Each mulligan adds one more known card on the bottom. The
mulliganed cards are assumed to be neither Aurora nor Promising Future; copies
drawn after a mulligan should be included in the two `*_in_hand` arguments.

If a reveal contains multiple Promising Futures but no Aurora, one PF continues
the chain and all other revealed PFs become inaccessible on the bottom.

Each chained PF prints two percentages. The first is its contribution measured
from the original scenario. For example, `Hit with PF #2: 9.34%` means 9.34% of
all original games succeed specifically on PF #2. The bracketed percentage is
the chance that the listed PF itself finds Aurora, considering only games where
the earlier PF missed and that PF was reached and played. PF #1 does not need a
bracket because it is played in every valid starting scenario.

Run the Promising Future calculator with its defaults or override its inputs:

```bash
python calculate_promising_future.py
python calculate_promising_future.py --auroras_in_hand 1 --PF_in_hand 1 --mulliganed 0 --turn 3
```

