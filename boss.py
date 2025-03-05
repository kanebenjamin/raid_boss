import random

class Boss(object):

    def __init__(self, boss_name="", player_count=4, poison=0):
        self.boss_name = boss_name
        self.player_count = player_count
        self.health = player_count * self.BASE_HEALTH
        self.poison = 0
        self.turn_count = 1
        self.text_result = ""
        self.next_attacks = []
        self.current_attacks = []

class RaidBoss1(Boss):

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
        CHANNEL_LIST = [0,1,3,7,9]
        ATTACK_LIST = [2,4,5,6,8]
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
    
class BlueBoss(Boss):

    def __init__(self):
        pass


