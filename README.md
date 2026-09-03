# Hypergeometric Card Calculator

A Python project for calculating the chance of drawing cards from a deck without replacement.

## Web interface

Install the web dependency and run the Streamlit application locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app scans `src/` on each run. Every folder containing a `streamlit_ui.py`
module with a callable `render()` function appears in the scenario selector. A
folder without that module is ignored, and a broken plugin produces a warning
instead of crashing the other scenarios. The selector uses the folder name.

To publish it through Streamlit Community Cloud:

1. Push these files to GitHub.
2. Sign in to Streamlit Community Cloud with GitHub.
3. Create an app and select this repository and branch.
4. Set the entry-point file to `app.py`.
5. Deploy and share the generated `streamlit.app` URL.

Future pushes are redeployed automatically.

Use `--help` on any scenario command to see all available flags. For example:

```bash
python -m src.two_drops --help
```

## Project structure

Python files and functions use `snake_case`, while classes use `PascalCase`.
Each scenario has its own package under `src/`; reusable probability logic lives
in `src/core/`, and automated tests live in `tests/`.

```text
src/
|-- core/
|   `-- hypergeometric.py
|-- two_drops/
|   |-- __main__.py
|   `-- streamlit_ui.py
|-- promising_future/
|   |-- scenario.py
|   |-- __main__.py
|   `-- streamlit_ui.py
`-- two_card_combo/
    |-- calculator.py
    |-- __main__.py
    `-- streamlit_ui.py
tests/
`-- test_calculators.py
```

`__main__.py` is the command-line entry point for a scenario. Its other modules
contain the reusable classes and calculation logic.

### Adding a scenario

Create `src/my_scenario/` with an empty `__init__.py`, a class in a descriptive
module such as `calculator.py`, and a `__main__.py` that reads flags, creates the
object, and prints its result. Add `streamlit_ui.py` with this entry point to
make it appear in the website automatically:

```python
def render() -> None:
    import streamlit as st

    st.header("my_scenario")
    # Read widget values, create the scenario object, and display its result.
```

The command-line version can then run as:

```bash
python -m src.my_scenario
```

## Usage

```python
from src.core import CardProbabilityCalculator

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
python -m src.two_drops
```

Override any default with flags named after the calculator variables:

```bash
python -m src.two_drops --deck_size 39 --target_cards 8 --mulliganed 2 --turn 2
```

The two-drop calculator counts the four-card opening hand, mulliganed cards, and
one card drawn per turn. With two cards mulliganed on turn 2, it calculates the
chance of finding a target among eight seen cards.

## A+B combos

`TwoCardComboCalculator` calculates the chance of seeing at least one copy of
two distinct cards. The CLI uses the same opening-hand, mulligan, and turn logic
as the two-drop calculator.

```bash
python -m src.two_card_combo
python -m src.two_card_combo --card_a_copies 3 --card_b_copies 2 --mulliganed 2 --turn 3
```

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
from src.promising_future import PromisingFutureScenario

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
python -m src.promising_future
python -m src.promising_future --auroras_in_hand 1 --PF_in_hand 1 --mulliganed 0 --turn 3
```
