#Python packages
import random
import math

#My Packages
import boss

#Lil dice roll function for usage in main- Note: indexing starts at zero so we need to x-1 the dice results
DICE_ROLL = [0,1,2,3,4,5]
def roll():
    return random.choice(DICE_ROLL) + random.choice(DICE_ROLL) 

if __name__ == "__main__":
    #Some initial player input to set up the game. We need number of players and a name for the raid boss
    num_players = int(input("Welcome to Raid Boss! How many people are playing? > "))
    boss_name = str(input(f"Ahh! Welcome to the dungeon, ye {num_players} brave wizard(s)! Who have you come here to slay? > "))
    print(f"\nHere comes {boss_name} now! Prepare thyselves for a whimsical battle! Best of luck!")
    #Unsure if doing this yet lol
    #print("If at any time you need a list of commands, type 'help' and I will give them to you!")
    #Instantiate the boss
    stinky = boss.RaidBoss1(player_count=num_players, boss_name=boss_name)
    #TODO add a phase two event that only triggers once somehow
    BOSS_HEALTH = stinky.health
    EVENT_TRIGGER_AMOUNT = BOSS_HEALTH/2
    trigger = True
    #There's probably a better way to do this.. but I'm adding all boss funcs to a list and then snagging them via die result in the main loop
    boss_funcs = [stinky.two, stinky.three, stinky.four, 
                  stinky.five, stinky.six, stinky.seven,
                  stinky.eight, stinky.nine, stinky.ten,
                  stinky.eleven, stinky.twelve
                ]
    #Main loop, keep doing this shit until boss has died or players have died
    while stinky.health > 0:
        #Check for half health event
        if stinky.health <= EVENT_TRIGGER_AMOUNT and trigger:
            print("The boss unleashes a hellish energy...")
            trigger = False
        #Need loop for each player
        for i in range(0, stinky.player_count):
            try:
                damage_done = int(input(f"PLAYER {i+1} TURN: Enter damage dealt! (Even if it's zero) and press enter!> "))
                stinky.health -= damage_done
            except ValueError:
                print("Invalid response, I'll assume you meant 0!")
                damage_done = 0
            print(f"Boss health at {stinky.health}")
            #Check for kill, break from player loop
            if stinky.health <= 0:
                    break
        #Check again becasue we have to break from main loop as well. Should maybe be a function but fuck it
        if stinky.health <= 0:
            break

        num_boss_rolls = math.floor(stinky.turn_count/2)
        next_num_boss_rolls = math.floor(stinky.turn_count/2) + 1
        if num_boss_rolls == 0:
            print(f"{boss_name} cannot attack on turn 1! You're safe until next turn.")
        #Get current attacks
        for num in stinky.current_attacks:
            dice_result = roll()
            stinky.text_result += "\n" + str(boss_funcs[num]()) + "\n"
        #Reset current attacks to be set later on
        stinky.current_attacks = []
        #Get next attacks
        for i in range (0, next_num_boss_rolls):
            stinky.next_attacks.append(roll())

        print("The boss gets " + str(num_boss_rolls) + " roll(s) this turn! Brace yourself!")
        print("TURN COUNT: " + str(stinky.turn_count))
        #If turn one, no attack- no need to tell the player there will be an attack if there actually won't be one
        if stinky.turn_count != 1:
            print(f"""\n\nTHE BOSS ATTACKS!
                {stinky.text_result}
            """)
        #Alert the player about next attacks
        #print("NEXT ROLLS " + str(stinky.next_attacks))
        print("Arcane intuition tells you...")
        print(stinky.get_attack_hint(stinky.next_attacks))
        #Reset next attacks for usage in subsequent loop - set to be current attacks
        stinky.current_attacks = stinky.next_attacks
        stinky.next_attacks = []

        try:
            death_count = int(input("How many players were defeated this turn? (enter 0 if no one was defeated) > "))
            stinky.player_count -= death_count
        except ValueError:
            print("Invalid response! I'm going to assume everyone is still in the fight!")
        if stinky.player_count <= 0:
            print(f"{boss_name} has defeated you!!!! Retreat and come back- next time cast better spells!")
            break
        #Reset rules text result, reset attack hint container up turn number, check for player elims
        stinky.turn_count += 1
        stinky.text_result = ""

#The end :)
if stinky.health < 0:
    print(f"Congratulations! You have defeated {boss_name}! They cower away from your SUPREME WHIMSY! Thanks for playing!")
else:
    print("Retry? Run the program again!")



    
