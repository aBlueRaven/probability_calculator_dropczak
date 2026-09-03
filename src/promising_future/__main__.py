import argparse

from src.promising_future import PromisingFutureScenario


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate the odds that a Promising Future chain finds Aurora.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=(
            "Hit with PF #N is measured from the initial scenario. The bracketed "
            "percentage is the chance that PF itself finds Aurora, considering "
            "only games where that PF was reached and played."
        ),
    )
    parser.add_argument(
        "--auroras_in_hand",
        type=int,
        default=0,
        help="Auroras already in hand",
    )
    parser.add_argument(
        "--PF_in_hand",
        dest="promising_futures_in_hand",
        type=int,
        default=1,
        help="Promising Futures already in hand",
    )
    parser.add_argument(
        "--mulliganed",
        dest="cards_mulliganed",
        type=int,
        default=2,
        help="cards placed on the bottom by the mulligan",
    )
    parser.add_argument(
        "--turn", type=int, default=2, help="turn on which PF is played"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scenario = PromisingFutureScenario(
        auroras_in_hand=args.auroras_in_hand,
        promising_futures_in_hand=args.promising_futures_in_hand,
        cards_mulliganed=args.cards_mulliganed,
        turn=args.turn,
    )
    print("############################")
    print(f"Assume {args.auroras_in_hand} auroras in hand")
    print(f"{args.promising_futures_in_hand} promising future in hand")
    print(f"{args.cards_mulliganed} cards mulliganed")
    print(f"turn {args.turn}")

    print("############################")
    print(f"Cards reachable before PF: {scenario.cards_remaining}")
    print(f"Auroras left in deck: {scenario.auroras_remaining}")
    print(f"PFs left in deck: {scenario.promising_futures_remaining}")
    print(f"Total chance to find Aurora: {scenario.success_probability():.2%}")

    conditional_successes = scenario.conditional_successes_by_cast()
    for cast_number, probability in scenario.successes_by_cast().items():
        conditional_result = ""
        if cast_number > 1:
            conditional_result = (
                " (% of success from PF in game: "
                f"{conditional_successes[cast_number]:.2%})"
            )
        print(f"Hit with PF #{cast_number}: {probability:.2%}{conditional_result}")


if __name__ == "__main__":
    main()
