"""Streamlit entry point for the scenario calculators."""

import streamlit as st

from src.scenario_loader import discover_scenarios


def main() -> None:
    st.set_page_config(
        page_title="Riftbound Probability Lab",
        page_icon=":material/casino:",
        layout="centered",
    )

    st.title("Riftbound Probability Lab")
    st.caption("Explore card probabilities without changing the source code.")

    scenarios, loading_errors = discover_scenarios()
    if not scenarios:
        st.warning("No scenarios with a `streamlit_ui.py` module were found.")
    else:
        selected_name = st.selectbox("Scenario", list(scenarios))
        selected_scenario = scenarios[selected_name]
        try:
            selected_scenario.render()
        except Exception as error:
            st.error(f"The {selected_name} scenario could not be displayed: {error}")

    if loading_errors:
        with st.expander("Scenario loading warnings"):
            for scenario_name, error in loading_errors.items():
                st.warning(f"{scenario_name}: {error}")


if __name__ == "__main__":
    main()
