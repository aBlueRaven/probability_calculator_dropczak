import argparse

from src.core import CardProbabilityCalculator

OPENING_HAND_SIZE = 4


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate the odds of drawing a two-cost card.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--deck_size", type=int, default=39, help="total cards in the deck"
    )
    parser.add_argument(
        "--target_cards",
        type=int,
        default=11,
        help="two-cost cards in the deck",
    )
    parser.add_argument(
        "--mulliganed",
        type=int,
        choices=range(3),
        default=2,
        help="cards placed on the bottom by the mulligan",
    )
    parser.add_argument(
        "--turn", type=int, default=2, help="turn by which the card is needed"
    )
    args = parser.parse_args()
    if args.turn < 0:
        parser.error("--turn cannot be negative")
    return args


def main() -> None:
    args = parse_args()
    cards_seen = OPENING_HAND_SIZE + args.mulliganed + args.turn
    opening_hand = CardProbabilityCalculator(
        deck_size=args.deck_size,
        target_cards=args.target_cards,
        cards_drawn=cards_seen,
    )

    print("############################")
    print(f"Assume deck size {args.deck_size}")
    print(f"{args.target_cards} target cards")
    print(f"{args.mulliganed} cards mulliganed")
    print(f"turn {args.turn}")
    
    print("############################")
    print(f"While seeing {opening_hand.cards_drawn} cards the odds of hitting")
    print(f"At least one copy: {opening_hand.at_least(1):.2%}")
    print(f"Exactly two copies: {opening_hand.exactly(2):.2%}")
    print(f"No copies: {opening_hand.exactly(0):.2%}")


if __name__ == "__main__":
    main()
