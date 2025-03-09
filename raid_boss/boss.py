import random


class Boss(object):

    result_text = ""
    BASE_HEALTH = 250

    def __init__(self, boss_name="", player_count=4, poison=0):
        self.boss_name = boss_name
        self.player_count = player_count
        self.health = player_count * self.BASE_HEALTH
        self.poison = 0
        self.turn_count = 1
        self.text_result = ""
        self.next_attacks = []
        self.current_attacks = []


class TheManaGod(Boss):

    def __init__(self, boss_name="", player_count=4, poison=0):
        self.boss_name = boss_name
        self.player_count = player_count
        self.health = player_count * self.BASE_HEALTH
        self.poison = 0
        self.turn_count = 1
        self.text_result = ""
        self.next_attacks = []
        self.current_attacks = []

    def two(self):
        return """BOSS SPELL> Each player chooses three: sacrifice all creatures you control, sacrifice all enchantments you control, 
sacrifice all artifacts you control, exile your graveyard. Boss permanents cannot be sacrificed this way."""

    def three(self):
        return """BOSS SPELL> For each player, create a colorless Boss enchantment token named Curse of Confusion under their control with 
“At the beginning of your end step, choose one: sacrifice a permanent, discard a card, or mill 5."""

    def four(self):
        return f"""BOSS SPELL> Create {self.player_count * 4} 1/1 red goblin zombie creature tokens with first strike, decayed, and haste.
 Four tokens attack each player this combat."""

    def five(self):
        return f"""BOSS SPELL> Players discard {2 * self.player_count} divided between players."""

    def six(self):
        return f"""BOSS SPELL> Create {self.player_count * 2} 2/2 black vampire zombie creature tokens with menace, decayed, and haste.
 Two tokens attack each player this combat."""

    def seven(self):
        return f"""BOSS SPELL> Create {self.player_count * 1} 5/5 green beast zombie creature token with trample, decayed, and haste. 
One token attacks each player this combat."""

    def eight(self):
        return f"""BOSS SPELL> Create {self.player_count * 2} 2/2 blue drake zombie creature token with flying, decayed, and haste. 
Two token attacks each player this combat."""

    def nine(self):
        return f"""BOSS SPELL> Players sacrifice {self.player_count} nonland, non-token permanents divided between players."""

    def ten(self):
        self.health += self.player_count * 4
        return f"""BOSS SPELL> Create {self.player_count * 4} 1/1 white cleric zombie creature tokens with 'enters' lifelink (this lifegain cannot be prevented), decayed, 
and haste. Four tokens attack each player this combat. Boss heals {self.player_count * 4} from the clerics!"""

    def eleven(self):
        return """BOSS SPELL> For each player, create a colorless artifact token named Altar of Bleeding under their 
control with 'At the beginning of your end step, you lose 3 life unless you pay 2.'"""

    def twelve(self):
        self.health += self.player_count * 20
        return f"""BOSS SPELL> {self.boss_name} heals {self.player_count * 20}
{self.boss_name}'s health is now {self.health}!"""

    def get_attack_hint(self, num_list):
        result = []
        CHANNEL_TEXT = "The boss is channeling energy!  "
        ATTACK_TEXT = "The boss is amassing armies!  "
        HEAL_TEXT = "The boss is about to heal!  "
        CHANNEL_LIST = [0, 1, 3, 7, 9]
        ATTACK_LIST = [2, 4, 5, 6, 8]
        HEAL_LIST = [10]
        for num in num_list:
            if num in CHANNEL_LIST:
                if CHANNEL_TEXT not in result:
                    result.append(CHANNEL_TEXT)
            if num in ATTACK_LIST:
                if ATTACK_TEXT not in result:
                    result.append(ATTACK_TEXT)
            if num in HEAL_LIST:
                if HEAL_TEXT not in result:
                    result.append(HEAL_TEXT)
        return " ".join(result) + "\n"


# BOSS 2


class HorrorfromtheDepths(Boss):

    def __init__(self, boss_name="", player_count=4, poison=0):
        self.boss_name = boss_name
        self.player_count = player_count
        self.health = player_count * self.BASE_HEALTH
        self.poison = 0
        self.turn_count = 1
        self.text_result = ""
        self.next_attacks = []
        self.current_attacks = []

    def two(self):
        return """BOSS SPELL> Return all nonland, non-boss permanents to their owner's hands."""

    def three(self):
        return """BOSS SPELL> For each player, create a blue enchantment token named
        Curse of Sinking with "Whenever you gain life, mill that many cards."""

    def four(self):
        return f"""BOSS SPELL> Return {self.player_count * 1} nonland, nontoken permanents to their owner's hands."""

    def five(self):
        return f"""BOSS SPELL> For each player, create a blue enchantment token named
        Curse of Rising Tides with "Whenever you draw one or more cards, mill that many cards."""

    def six(self):
        return f"""BOSS SPELL> Create {self.player_count * 1} 1/1 blue tentacle creature tokens with decayed, haste
        and "This creature gets +1/+1 for each instant or sorcery in defending player's graveyard."
        One token attacks each player this combat."""

    def seven(self):
        return f"""BOSS SPELL> Create {self.player_count * 2} 1/1 blue jellyfish creature tokens with first strike, decayed, haste and 
        "When this creature deals combat damage to a player, that player chooses an untapped creature they control, taps it
        and puts a stun counter on it." Two tokens attack each player this combat."""

    def eight(self):
        return f"""BOSS SPELL> Create {self.player_count * 1} 1/1 blue spawn creature tokens with decayed, haste and 
        "This creature gets +1/+0 for each card in defending player's hand." One token attacks each player this combat."""

    def nine(self):
        return f"""BOSS SPELL> For each player, create a blue enchantment token named Curse of Rising Tides with
        "Whenever you draw one or more cards, mill that many cards."""

    def ten(self):
        return f"""BOSS SPELL> Return {self.player_count * 1} nonland, nontoken permanents to their owner's hands."""

    def eleven(self):
        return """BOSS SPELL> For each player, create a blue enchantment token named Curse of Sinking with 
        "Whenever you gain life, mill that many cards."""

    def twelve(self):
        return f"""BOSS SPELL> Return all nonland, non-boss permanents to their owner's hands."""

    def get_attack_hint(self, num_list):
        result = []
        RECOIL_TEXT = (
            "The Horror recoils as it prepares to unleash a massive tidal wave. "
        )
        CHANNEL_TEXT = "The Horror is channeling dark energies. "
        ATTACK_TEXT = "The Horror is summoning beasts from the depths. "
        CHANNEL_LIST = [1, 2, 3, 7, 8, 9]
        ATTACK_LIST = [4, 5, 6]
        RECOIL_LIST = [0, 10]
        for num in num_list:
            if num in CHANNEL_LIST:
                if CHANNEL_TEXT not in result:
                    result.append(CHANNEL_TEXT)
            if num in ATTACK_LIST:
                if ATTACK_TEXT not in result:
                    result.append(ATTACK_TEXT)
            if num in RECOIL_LIST:
                if RECOIL_TEXT not in result:
                    result.append(RECOIL_TEXT)
        return " ".join(result) + "\n"
    

class LunarChanneler(Boss):

    def __init__(self, boss_name="", player_count=4, poison=0):
        self.boss_name = boss_name
        self.player_count = player_count
        self.health = (self.BASE_HEALTH - 200) * player_count
        self.poison = 0
        self.turn_count = 1
        self.text_result = ""
        self.next_attacks = []
        self.current_attacks = []

    def two(self):
        return f"""BOSS SPELL> create {self.player_count * 1}  X/X Spirit Zombie Cleric with “when this creature attacks, tap target creature defending player controls at random”
        where X is the total number of cards in all graveyards with haste, decayed, menace. 1 token attacks each player this combat. """

    def three(self):
        return """BOSS SPELL> Lunar Channeler creates “Moon’s Presence” an enchantment aura with “enchant player. 
        Lunar Light Soldier creatures the boss controls gain +1/+1 for each Aura attached to players.” Randomly attach it to a player."""

    def four(self):
        return f"""BOSS SPELL> Create {self.player_count * 3} Lunar Light Soldiers with haste and decayed. 3 tokens attack each player this combat."""

    def five(self):
        return f"""BOSS SPELL> create {self.player_count * 2} 1/1 Lunar Light Soldiers with decayed and haste"""

    def six(self):
        return f"""BOSS SPELL> Lunar Channeler creates “Curse of the full Moon” an enchantment with “enchant player. 
        Enchanted player’s creatures get -X/0 where X is the number of cards in enchanted players hand.” Randomly attach it to a player."""

    def seven(self):
        return f"""BOSS SPELL> Make a Pumpkin Totem artifact enchantment token with “enchant player. at your end step the boss heals 5.” Randomly attach it to a player. """

    def eight(self):
        return f"""BOSS SPELL> Lunar Channeler creates “Moon’s Watcher” an enchantment with “enchant player. 
        Whenever enchanted player attacks with one or more creatures, this enchantment becomes a 0/1 indestructible white Lunar Statue. 
        It gains “this creature blocks the creature with the highest power among attacking creatures.” Randomly attach it to a player."""

    def nine(self):
        return f"""BOSS SPELL> create {self.player_count * 2} white Lunar Light Soldiers with haste and decayed."""

    def ten(self):
        return f"""BOSS SPELL> Create {self.player_count * 1} white and blue Moon’s Disciple an X/X Spirit with decayed, haste and flying and this creature gets +1/+1 where X is the number of turns the boss has taken (including this one).."""

    def eleven(self):
        return f"""BOSS SPELL> create {self.player_count * 3} white Lunar Light Soldiers with haste and decayed. 3 tokens attach each player this combat."""

    def twelve(self):
        return f"""BOSS SPELL> Create {self.player_count * 1} 5/5 Reflection of Emrakul, Freed from the Moon, an Eldrazi creature with haste, decayed, trample, flying and Annihilator 1."""

    def get_attack_hint(self, num_list):
        result = []
        EMRAKUL_TEXT = (
            "An unsettling energy eminates from the moon... "
        )
        ZOMBIE_TEXT = "The ground begins to open at Lunar Channeler's feet."
        CHANNEL_TEXT = "Lunar Channeler begins chanting at the moon."
        ATTACK_TEXT = "Lunar Channeler is conjuring entities."
        CHANNEL_LIST = [1,4,5,6]
        ATTACK_LIST = [2,3,7,8,9]
        EMRAKUL_LIST = [10]
        ZOMBIE_LIST = [0]
        for num in num_list:
            if num in CHANNEL_LIST:
                if CHANNEL_TEXT not in result:
                    result.append(CHANNEL_TEXT)
            if num in ATTACK_LIST:
                if ATTACK_TEXT not in result:
                    result.append(ATTACK_TEXT)
            if num in EMRAKUL_LIST:
                if EMRAKUL_TEXT not in result:
                    result.append(EMRAKUL_TEXT)
            if num in ZOMBIE_LIST:
                if ZOMBIE_TEXT not in result:
                    result.append(ZOMBIE_TEXT)
        return " ".join(result) + "\n"