"""Streamlit interface for the two-drop scenario."""

from src.core import CardProbabilityCalculator

OPENING_HAND_SIZE = 4


def render() -> None:
    import streamlit as st

    st.header("two_drops")
    st.write("Find the chance of seeing at least one playable target by a turn.")

    deck_size = int(
        st.number_input("Deck size", min_value=1, value=39, step=1)
    )
    target_cards = int(
        st.number_input("Target cards", min_value=0, value=11, step=1)
    )
    cards_mulliganed = int(
        st.number_input("Cards mulliganed", min_value=0, max_value=2, value=2)
    )
    turn = int(st.number_input("Turn", min_value=0, value=2, step=1))
    cards_seen = OPENING_HAND_SIZE + cards_mulliganed + turn

    try:
        calculator = CardProbabilityCalculator(
            deck_size=deck_size,
            target_cards=target_cards,
            cards_drawn=cards_seen,
        )
    except (TypeError, ValueError) as error:
        st.error(str(error))
        return

    st.caption(f"Cards seen: {cards_seen}")
    first, second, third = st.columns(3)
    first.metric("At least one", f"{calculator.at_least(1):.2%}")
    second.metric("Exactly two", f"{calculator.exactly(2):.2%}")
    third.metric("No copies", f"{calculator.exactly(0):.2%}")
