import random
from collections import Counter

NUM_DICE = 5
NUM_TURNS = 13
CATEGORIES = [
    "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
    "Three of a Kind", "Four of a Kind", "Full House",
    "Small Straight", "Large Straight", "Yahtzee", "Chance"
]

def roll_dice(current_dice=None, held=[]):
    if current_dice is None:
        current_dice = [0] * NUM_DICE
    return [current_dice[i] if i in held else random.randint(1, 6) for i in range(NUM_DICE)]

def display_dice(dice):
    positions = ' '.join(str(i+1) for i in range(len(dice)))
    values = ' '.join(str(d) for d in dice)
    print(f"Positions: {positions}")
    print(f"Your dice: {values}")

def reroll(dice):
    for roll_num in range(2):
        held_indices = input(f"Roll {roll_num + 2}: Enter positions to hold (e.g., 1 3 5), or press Enter to reroll all: ")
        if not held_indices.strip():
            dice = roll_dice()
        else:
            try:
                held = [int(i)-1 for i in held_indices.strip().split()]
                if all(0 <= i < NUM_DICE for i in held):
                    dice = roll_dice(dice, held)
                else:
                    print("Invalid input. Try again.")
                    continue
            except ValueError:
                print("Invalid input. Try again.")
                continue
        display_dice(dice)
    return dice

def score_dice(dice, category):
    counts = Counter(dice)
    sorted_dice = sorted(dice)

    if category == "Ones":
        return dice.count(1) * 1
    elif category == "Twos":
        return dice.count(2) * 2
    elif category == "Threes":
        return dice.count(3) * 3
    elif category == "Fours":
        return dice.count(4) * 4
    elif category == "Fives":
        return dice.count(5) * 5
    elif category == "Sixes":
        return dice.count(6) * 6
    elif category == "Three of a Kind":
        return sum(dice) if any(v >= 3 for v in counts.values()) else 0
    elif category == "Four of a Kind":
        return sum(dice) if any(v >= 4 for v in counts.values()) else 0
    elif category == "Full House":
        return 25 if sorted(counts.values()) == [2, 3] else 0
    elif category == "Small Straight":
        straights = [{1,2,3,4},{2,3,4,5},{3,4,5,6}]
        return 30 if any(straight.issubset(set(dice)) for straight in straights) else 0
    elif category == "Large Straight":
        return 40 if set(dice) in [set([1,2,3,4,5]), set([2,3,4,5,6])] else 0
    elif category == "Yahtzee":
        return 50 if any(v == 5 for v in counts.values()) else 0
    elif category == "Chance":
        return sum(dice)
    return 0

def main():
    used_categories = set()
    total_score = 0

    print("Welcome to Yahtzee!\n")

    for turn in range(NUM_TURNS):
        print(f"\n--- Turn {turn + 1} ---")
        dice = roll_dice()
        display_dice(dice)
        dice = reroll(dice)

        print("\nAvailable categories:")
        available = [cat for cat in CATEGORIES if cat not in used_categories]
        for i, cat in enumerate(available):
            print(f"{i + 1}. {cat}")

        while True:
            try:
                choice = int(input("Choose a category number: ")) - 1
                if 0 <= choice < len(available):
                    category = available[choice]
                    break
                else:
                    print("Invalid choice. Please select a number from the list.")
            except ValueError:
                print("Enter a valid number.")

        score = score_dice(dice, category)
        print(f"Scored {score} points in {category}")
        total_score += score
        used_categories.add(category)

    print(f"\nGame over! Your total score: {total_score}")

if __name__ == "__main__":
    main()
