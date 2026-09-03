"""Streamlit interface for the two-card combo scenario."""

from src.two_card_combo import TwoCardComboCalculator

OPENING_HAND_SIZE = 4


def render() -> None:
    import streamlit as st

    st.header("two_card_combo")
    st.write("Find the chance of seeing at least one copy of both card A and B.")

    deck_size = int(
        st.number_input("Deck size", min_value=1, value=39, step=1)
    )
    card_a_copies = int(
        st.number_input("Copies of card A", min_value=0, value=3, step=1)
    )
    card_b_copies = int(
        st.number_input("Copies of card B", min_value=0, value=3, step=1)
    )
    cards_mulliganed = int(
        st.number_input("Cards mulliganed", min_value=0, max_value=2, value=2)
    )
    turn = int(st.number_input("Turn", min_value=0, value=2, step=1))
    cards_seen = OPENING_HAND_SIZE + cards_mulliganed + turn

    try:
        calculator = TwoCardComboCalculator(
            deck_size=deck_size,
            card_a_copies=card_a_copies,
            card_b_copies=card_b_copies,
            cards_seen=cards_seen,
        )
    except (TypeError, ValueError) as error:
        st.error(str(error))
        return

    st.caption(f"Cards seen: {cards_seen}")
    st.metric(
        "At least one card A and one card B",
        f"{calculator.success_probability():.2%}",
    )
