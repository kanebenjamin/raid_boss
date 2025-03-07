import random
import math
import sys
import os

# Add the parent directory to the sys.path to handle standalone execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from raid_boss import boss


DICE_ROLL = [0, 1, 2, 3, 4, 5]


def roll():
    return random.choice(DICE_ROLL) + random.choice(DICE_ROLL)


store_prerolls = []
for i in range(100):
    innerlist = []
    reps = math.floor(0.5 * i)
    for ii in range(reps):
        innerlist.append(roll())
    store_prerolls.append(innerlist)

if __name__ == "__main__":
    num_players = int(input("Welcome to Raid Boss! How many people are playing? > "))
    boss_name = str(
        input(
            f"Ahh! Welcome to the dungeon, ye {num_players} brave wizard(s)! Who have you come here to slay? > "
        )
    )
    print(
        f"\nHere comes {boss_name} now! Prepare thyselves for a whimsical battle! Best of luck!"
    )

    boss_list = [boss.TheManaGod, boss.HorrorfromtheDepths]
    stinky = boss.HorrorfromtheDepths(player_count=num_players, boss_name=boss_name)

    BOSS_HEALTH = stinky.health
    EVENT_TRIGGER_AMOUNT = BOSS_HEALTH / 2
    trigger = True
    boss_funcs = [
        stinky.two,
        stinky.three,
        stinky.four,
        stinky.five,
        stinky.six,
        stinky.seven,
        stinky.eight,
        stinky.nine,
        stinky.ten,
        stinky.eleven,
        stinky.twelve,
    ]

    while stinky.health > 0:
        if stinky.health <= EVENT_TRIGGER_AMOUNT and trigger:
            print("The boss unleashes a hellish energy...")
            trigger = False

        for i in range(0, stinky.player_count):
            try:
                damage_done = int(
                    input(
                        f"PLAYER {i+1} TURN: Enter damage dealt! (Even if it's zero) and press enter!> "
                    )
                )
                stinky.health -= damage_done
            except ValueError:
                print("Invalid response, I'll assume you meant 0!")
                damage_done = 0
            print(f"Boss health at {stinky.health}")
            if stinky.health <= 0:
                break

        if stinky.health <= 0:
            break

        stinky.current_attacks = store_prerolls[stinky.turn_count]
        stinky.next_attacks = store_prerolls[stinky.turn_count + 1]

        if len(store_prerolls[stinky.turn_count]) == 0:
            print(f"{boss_name} cannot attack on turn 1! You're safe until next turn.")
        for num in stinky.current_attacks:
            stinky.text_result += "\n" + str(boss_funcs[num]()) + "\n"

        print(
            "The boss gets "
            + str(len(stinky.current_attacks))
            + " roll(s) this turn! Brace yourself!"
        )
        print("TURN COUNT: " + str(stinky.turn_count))
        if stinky.turn_count != 1:
            print(
                f"""\n\nTHE BOSS ATTACKS!
                {stinky.text_result}
            """
            )
        print("Arcane intuition tells you...")
        print(stinky.get_attack_hint(stinky.next_attacks))

        try:
            death_count = int(
                input(
                    "How many players were defeated this turn? (enter 0 if no one was defeated) > "
                )
            )
            stinky.player_count -= death_count
        except ValueError:
            print(
                "Invalid response! I'm going to assume everyone is still in the fight!"
            )
        if stinky.player_count <= 0:
            print(
                f"{boss_name} has defeated you!!!! Retreat and come back- next time cast better spells!"
            )
            break

        stinky.turn_count += 1
        stinky.text_result = ""

    if stinky.health < 0:
        print(
            f"Congratulations! You have defeated {boss_name}! They cower away from your SUPREME WHIMSY! Thanks for playing!"
        )
    else:
        print("Retry? Run the program again!")
