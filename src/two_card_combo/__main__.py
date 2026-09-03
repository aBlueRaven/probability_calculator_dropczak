import argparse

from src.two_card_combo import TwoCardComboCalculator

OPENING_HAND_SIZE = 4


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate the odds of drawing both pieces of an A+B combo.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--deck_size", type=int, default=39, help="total cards in the deck"
    )
    parser.add_argument(
        "--card_a_copies", type=int, default=3, help="copies of card A in the deck"
    )
    parser.add_argument(
        "--card_b_copies", type=int, default=3, help="copies of card B in the deck"
    )
    parser.add_argument(
        "--mulliganed",
        type=int,
        choices=range(3),
        default=2,
        help="cards placed on the bottom by the mulligan",
    )
    parser.add_argument(
        "--turn", type=int, default=2, help="turn by which both cards are needed"
    )
    args = parser.parse_args()
    if args.turn < 0:
        parser.error("--turn cannot be negative")
    return args


def main() -> None:
    args = parse_args()
    cards_seen = OPENING_HAND_SIZE + args.mulliganed + args.turn
    combo = TwoCardComboCalculator(
        deck_size=args.deck_size,
        card_a_copies=args.card_a_copies,
        card_b_copies=args.card_b_copies,
        cards_seen=cards_seen,
    )

    print("############################")
    print(f"Assume deck size {args.deck_size}")
    print(f"{args.card_a_copies} copies of card A")
    print(f"{args.card_b_copies} copies of card B")
    print(f"{args.mulliganed} cards mulliganed")
    print(f"turn {args.turn}")
    print("############################")
    print(f"While seeing {cards_seen} cards")
    print(f"At least one card A and one card B: {combo.success_probability():.2%}")


if __name__ == "__main__":
    main()
