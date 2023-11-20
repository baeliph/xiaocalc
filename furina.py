from bisect import insort
import math

class Character:
    """
    Represents a character in a rotation.

    Attributes:
        name: character name
        max_hp: character's max hp
        current_hp: character's current hp, as a % of their max hp
    """

    def __init__(self, name: str, max_hp: int, current_hp: float):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp * current_hp
    
    def heal(self, heal_hp: int):
        """
        Heal a fixed HP amount.
        """
        healed = min(heal_hp, self.max_hp - self.current_hp)
        self.current_hp += healed
        return healed / self.max_hp * 100

    def heal_max(self, heal_percent: float):
        """
        Heal a % of max HP.
        """
        healed = min(self.max_hp * heal_percent, self.max_hp - self.current_hp)
        self.current_hp += healed
        return healed / self.max_hp * 100

    def drain_max(self, drain_percent: float):
        """
        Drain a % of max HP.
        """
        self.current_hp -= self.max_hp * drain_percent
        return drain_percent * 100

    def drain_curr(self, drain_percent: float):
        """
        Drain a % of current HP.
        """
        hp_drain = self.current_hp * drain_percent
        self.current_hp -= hp_drain
        return hp_drain / self.max_hp * 100
    
    def above50(self):
        """
        Returns true if character is above 50% HP.
        """
        return self.current_hp * 2 > self.max_hp

    def below70(self):
        """
        Returns true if character is below 70% HP.
        """
        return self.current_hp < self.max_hp * 0.70

    def __eq__(self, other):
        if isinstance(other, Character):
            return self.name == other.name
        return False

class XiaoFaruzanFurinaRotation:
    """
    Rotation consisting of C0 Xiao, C6 Faruzan, and C0 Furina.

    Attributes:
        current_hp: % of max HP each character should start at
    """

    def __init__(self, current_hp: float = 1.0):
        # Rotation timeline
        self.timeline = []

        # Characters
        self.characters = []
        self.xiao = Character("Xiao", 19288.0, current_hp)
        self.faruzan = Character("Faruzan", 17722.0, current_hp)
        self.furina = Character("Furina", 34561.0, current_hp)

        # Action instances
        self.fanfare = 0.0
        self.plunge = 0
        self.faruzan_skill = 0
        self.furina_seahorse = 0
        self.furina_octopus = 0
        self.furina_crab = 0

    def FurinaSeaHorse(self):
        """
        Furina's Seahorse hits.
        """
        self.furina_seahorse += 1
        drain = 0
        for character in self.characters:
            if (character.above50()):
                self.fanfare += character.drain_max(0.016)
                drain += 1
        return "Furina Seahorse {} ({} drained)".format(self.furina_seahorse, drain), self.fanfare
    
    def FurinaOctopus(self):
        """
        Furina's Octopus hits.
        """
        self.furina_octopus += 1
        drain = 0
        for character in self.characters:
            if (character.above50()):
                self.fanfare += character.drain_max(0.024)
                drain += 1
        return "Furina Octopus {} ({} drained)".format(self.furina_octopus, drain), self.fanfare
    
    def FurinaCrab(self):
        """
        Furina's Crab hits.
        """
        self.furina_crab += 1
        drain = 0
        for character in self.characters:
            if (character.above50()):
                self.fanfare += character.drain_max(0.036)
                drain += 1
        return "Furina Crab {} ({} drained)".format(self.furina_crab, drain), self.fanfare
    
    def XiaoBurst(self):
        """
        Xiao's Burst HP drain.
        """
        self.fanfare += self.xiao.drain_curr(0.025)
        return "Xiao HP Drain", self.fanfare

    def XiaoE(self):
        """
        Xiao's Elemental Skill.
        """
        return "Xiao E", self.fanfare

    def XiaoPlunge(self):
        """
        Xiao's High Plunge in Burst.
        """
        self.plunge += 1
        return "Xiao Plunge {}".format(self.plunge), self.fanfare
    
    def FaruzanSkill(self):
        """
        C6 Faruzan's Elemental Skill.
        """
        self.faruzan_skill += 1
        return "Faruzan Skill {}".format(self.faruzan_skill), self.fanfare

    def FurinaA1(self, on_field_character: Character):
        """
        Furina's A1, which heals off-field characters for 2% of their max HP
        if the on field character is overhealed.
        """
        if on_field_character.current_hp == on_field_character.max_hp:
            for character in self.characters:
                if character is not on_field_character:
                    self.fanfare += character.heal_max(0.02)
    
    def add(self, time: float, action):
        """
        Add an action to the timeline at the given time.
        """
        insort(self.timeline, (time, action), key=lambda x: x[0])
    
    def generate_timeline(self):
        """
        Generate the rotation's timeline.
        """
        # Xiao Skills
        self.add(0.500, self.XiaoE)
        self.add(1.000, self.XiaoE)

        # Xiao Plunges, once every 1.167 second
        for i in range(12):
            self.add(3.283 + 1.167 * i, self.XiaoPlunge)

        # Xiao HP Drain, once a second
        for i in range(16):
            self.add(2.117 + 1.0 * i, self.XiaoBurst)

        # Furina Seahorse
        for i in range(13):
            self.add(1.190 * (i + 1), self.FurinaSeaHorse)

        # Furina Octopus
        for i in range(7):
            self.add(2.900 * (i + 1), self.FurinaOctopus)
        
        # Furina Crab
        for i in range(4):
            self.add(4.800 * (i + 1), self.FurinaCrab)
        
        # Faruzan Skill
        for i in range(7):
            self.add(3.0 * i, self.FaruzanSkill)

    def should_print(self, action_name: str):
        """
        Returns true if the action should be printed to console.
        """
        allow_list = [
            'Xiao E',
            'Xiao Plunge',
            'Jean Burst',
            'Furina',
            'Faruzan Skill'
        ]
        for allowed_action in allow_list:
            if action_name.find(allowed_action) > -1:
                return True
        return False

    def run(self):
        """
        Run the rotation and print each action and its Fanfare points.
        """
        self.generate_timeline()

        for action in self.timeline:
            action_name, fanfare = action[1]()
            fanfare = min(300.0, fanfare)
            results = []
            if self.should_print(action_name):
                results.append('{}: {} Fanfare'.format(action_name, math.floor(fanfare)))
            
            for x in sorted(results):
                print(x)

class JeanC0(XiaoFaruzanFurinaRotation):
    """
    Rotation with C0 Jean.
    """
    def __init__(self, current_hp: float = 1.0):
        super().__init__(current_hp)
        self.furina = Character("Furina", 35321.0, current_hp)
        self.jean = Character("Jean", 21441.0, current_hp)
        self.characters = [self.xiao, self.faruzan, self.furina, self.jean]

    def JeanBurst(self, heal_amount=14052.0):
        """
        Jean's Burst on-cast heal.
        """
        for character in self.characters:
            self.fanfare += character.heal(heal_amount)
        return "Jean Burst", self.fanfare
    
    def JeanBurstTick(self, heal_amount=1405.0):
        """
        Jean's Burst heal ticks.
        """
        self.fanfare += self.xiao.heal(heal_amount)
        self.FurinaA1(self.xiao)
        return "Jean Tick", self.fanfare

    def generate_timeline(self):
        super().generate_timeline()
        
        # Jean Burst
        self.add(0.01, self.JeanBurst)

        # Jean Burst Ticks
        for i in range(10):
            self.add(1.01 + 1.0 * i, self.JeanBurstTick)
        
class JeanC4(JeanC0):
    """
    Rotation with C4 Jean.
    """
    def JeanBurst(self):
        for character in self.characters:
            self.fanfare += character.heal(16847.0)
        return "Jean Burst", self.fanfare

    def JeanBurstTick(self):
        self.fanfare += self.xiao.heal(1685.0)
        self.FurinaA1(self.xiao)
        return "Jean Tick", self.fanfare

class Bennett(XiaoFaruzanFurinaRotation):
    """
    Rotation with Bennett.
    """
    def __init__(self, current_hp: float = 1.0):
        super().__init__(current_hp)
        self.furina = Character("Furina", 34561.0, current_hp)
        self.bennett = Character("Bennett", 29611.0, current_hp)
        self.characters = [self.xiao, self.faruzan, self.furina, self.bennett]
        self.bennett_tick = 0
    
    def BennettBurstTick(self):
        """
        Bennett's Burst heal ticks.
        """
        self.bennett_tick += 1

        if self.bennett_tick == 1:
            if self.bennett.below70():
                self.fanfare += self.bennett.heal(6835.0)
                self.FurinaA1(self.bennett)
        else:
            if self.xiao.below70():
                self.fanfare += self.xiao.heal(6835.0)
                self.FurinaA1(self.xiao)
        return "Bennett Tick", self.fanfare

    def generate_timeline(self):
        super().generate_timeline()
        
        # Bennett Burst Ticks
        # First one heals Bennett
        self.add(0.0, self.BennettBurstTick)
        for i in range(11):
            # First heal tick for Xiao comes on his second E
            self.add(0.9 + 1.0 * i, self.BennettBurstTick)

def main():
    rotation = JeanC0(1.0)
    rotation.run()

if __name__ == '__main__':
    main()
