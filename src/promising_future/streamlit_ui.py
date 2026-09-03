"""Streamlit interface for the Promising Future scenario."""

from src.promising_future import PromisingFutureScenario


def render() -> None:
    import streamlit as st

    st.header("promising_future")
    st.write("Find the chance that a Promising Future chain reveals an Aurora.")

    auroras_in_hand = int(
        st.number_input(
            "Auroras in hand", min_value=0, max_value=3, value=0, step=1
        )
    )
    promising_futures_in_hand = int(
        st.number_input(
            "Promising Futures in hand",
            min_value=0,
            max_value=3,
            value=1,
            step=1,
        )
    )
    cards_mulliganed = int(
        st.number_input("Cards mulliganed", min_value=0, max_value=2, value=2)
    )
    turn = int(st.number_input("Turn", min_value=0, value=2, step=1))

    try:
        scenario = PromisingFutureScenario(
            auroras_in_hand=auroras_in_hand,
            promising_futures_in_hand=promising_futures_in_hand,
            cards_mulliganed=cards_mulliganed,
            turn=turn,
        )
    except (TypeError, ValueError) as error:
        st.error(str(error))
        return

    st.metric("Total chance to find Aurora", f"{scenario.success_probability():.2%}")
    st.caption(
        f"{scenario.cards_remaining} reachable cards, "
        f"{scenario.auroras_remaining} Auroras, and "
        f"{scenario.promising_futures_remaining} PFs remain in the deck."
    )

    conditional_successes = scenario.conditional_successes_by_cast()
    results = []
    for cast_number, probability in scenario.successes_by_cast().items():
        conditional = "Always played"
        if cast_number > 1:
            conditional = f"{conditional_successes[cast_number]:.2%}"
        results.append(
            {
                "PF cast": f"#{cast_number}",
                "Success from initial scenario": f"{probability:.2%}",
                "Success when this PF is played": conditional,
            }
        )

    if results:
        st.table(results)
    else:
        st.info("At least one Promising Future must be in hand to start the chain.")

    st.caption(
        "The conditional percentage considers only games where that PF was "
        "reached and played."
    )
