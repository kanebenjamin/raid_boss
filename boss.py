import random

class RaidBoss1(object):

    result_text = ""
    BASE_HEALTH = 250

    def __init__(self, boss_name="", player_count=4, poison=0):
        self.boss_name = boss_name
        self.player_count = player_count
        self.health = player_count * self.BASE_HEALTH
        self.poison = 0
        self.turn_count = 1
        self.text_result = ""


    def two(self):
        return """Each player chooses three: sacrifice all creatures you control, sacrifice all enchantments you control, 
sacrifice all artifacts you control, exile your graveyard. Boss permanents cannot be sacrificed this way."""

    def three(self):
        return """For each player, create a colorless Boss enchantment token named Curse of Confusion under their control with 
“At the beginning of your end step, choose one: sacrifice a permanent, discard a card, or mill 5."""
        
    def four(self):
        return f"""Create {self.player_count * 4} 1/1 red goblin zombie creature tokens with first strike, decayed, and haste.
 Four tokens attack each player this combat."""

    def five(self):
        return f"""Players discard {2 * self.player_count} divided between players."""

    def six(self):
        return f"""Create {self.player_count * 2} 2/2 black vampire zombie creature tokens with menace, decayed, and haste.
 Two tokens attack each player this combat."""

    def seven(self):
        return f"""Create {self.player_count * 1} 5/5 green beast zombie creature token with trample, decayed, and haste. 
One token attacks each player this combat."""

    def eight(self):
        return f"""Create {self.player_count * 2} 2/2 blue drake zombie creature token with flying, decayed, and haste. 
One token attacks each player this combat."""

    def nine(self):
        return f"""Players sacrifice {self.player_count} nonland, non-token permanents divided between players."""
    
    def ten(self):
        return f"""Create {self.player_count * 4} 1/1 white cleric zombie creature tokens with lifelink, decayed, 
and haste. Four tokens attack each player this combat."""
    
    def eleven(self):
        return """For each player, create a colorless artifact token named Altar of Bleeding under their 
control with 'At the beginning of your end step, you lose 3 life unless you pay 2.'"""
    
    def twelve(self):
        self.health += self.player_count * 20
        return f"""{self.boss_name} heals {self.player_count * 20}
{self.boss_name}'s health is now {self.health}!"""