from bisect import insort
import math
import os

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
        self.furina_burst = False

    def FurinaBurst(self, time):
        self.furina_burst = True
        self.fanfare = 0.0
        return "Furina Burst", self.fanfare

    def FurinaBurstEnd(self, time):
        self.furina_burst = False
        self.fanfare = 0.0
        return "Furina Burst End", self.fanfare

    def FurinaSeaHorse(self, time):
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
    
    def FurinaOctopus(self, time):
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
    
    def FurinaCrab(self, time):
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
    
    def XiaoBurst(self, time):
        """
        Xiao's Burst HP drain.
        """
        self.fanfare += self.xiao.drain_curr(0.025)
        return "Xiao HP Drain", self.fanfare

    def XiaoE(self, time):
        """
        Xiao's Elemental Skill.
        """
        return "Xiao E", self.fanfare

    def XiaoPlunge(self, time):
        """
        Xiao's High Plunge in Burst.
        """
        self.plunge += 1
        return "Xiao Plunge {}".format(self.plunge), self.fanfare
    
    def FaruzanBurst(self, time):
        return "Faruzan Burst", self.fanfare
    
    def FaruzanSkill(self, time):
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
    
    def generate_timeline(self, xiao_start=7.65):
        """
        Generate the rotation's timeline.
        """
        # Xiao Skills
        self.add(xiao_start, self.XiaoE)
        self.add(xiao_start + 0.5, self.XiaoE)

        # Xiao Plunges, once every 1.167 second
        for i in range(12):
            self.add(xiao_start + 2.78 + 1.167 * i, self.XiaoPlunge)

        # Xiao HP Drain, once a second
        for i in range(16):
            self.add(xiao_start + 1.617 + 1.0 * i, self.XiaoBurst)

        # Furina Seahorse
        for i in range(13):
            self.add(2.217 + 1.190 * (i + 1), self.FurinaSeaHorse)

        # Furina Octopus
        for i in range(7):
            self.add(2.217 + 2.900 * (i + 1), self.FurinaOctopus)
        
        # Furina Crab
        for i in range(4):
            self.add(2.217 + 4.800 * (i + 1), self.FurinaCrab)

        # Furina Burst
        self.add(4.067, self.FurinaBurst)
        self.add(22.067, self.FurinaBurstEnd)
        
        # Faruzan Burst
        self.add(0.0, self.FaruzanBurst)

        # Faruzan Skill
        for i in range(7):
            self.add(1.0 + 3.0 * i, self.FaruzanSkill)

    def should_print(self, action_name: str):
        """
        Returns true if the action should be printed to console.
        """
        allow_list = [
            'Xiao E',
            'Xiao Plunge',
            'Jean Burst',
            'Furina',
            'Faruzan',
            'Xianyun',
            'Bennett'
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

        results = []
        for action in self.timeline:
            action_name, fanfare = action[1](action[0])
            fanfare = math.floor(min(300.0, fanfare)) if self.furina_burst else 0.0
            if self.should_print(action_name):
                results.append("{:.3f} | {}: {} Fanfare".format(action[0], action_name, math.floor(fanfare)))
            
        for x in results:
            print(x)
            
        return results

        # for character in self.characters:
        #     print("{} {}".format(character.name, character.current_hp/character.max_hp))

class JeanC0(XiaoFaruzanFurinaRotation):
    """
    Rotation with C0 Jean.
    """
    def __init__(self, current_hp: float = 1.0):
        super().__init__(current_hp)
        self.furina = Character("Furina", 35321.0, current_hp)
        self.jean = Character("Jean", 21441.0, current_hp)
        self.characters = [self.xiao, self.faruzan, self.furina, self.jean]

    def JeanBurst(self, time, heal_amount=14052.0):
        """
        Jean's Burst on-cast heal.
        """
        for character in self.characters:
            self.fanfare += character.heal(heal_amount)
        return "Jean Burst", self.fanfare
    
    def JeanBurstTick(self, time, heal_amount=1405.0):
        """
        Jean's Burst heal ticks.
        """
        self.fanfare += self.xiao.heal(heal_amount)
        self.FurinaA1(self.xiao)
        return "Jean Tick", self.fanfare

    def generate_timeline(self):
        super().generate_timeline(xiao_start=6.75)
        
        # Jean Burst
        self.add(6.0, self.JeanBurst)

        # Jean Burst Ticks
        for i in range(10):
            self.add(6.0 + 1.0 * i, self.JeanBurstTick)
        
class JeanC4(JeanC0):
    """
    Rotation with C4 Jean.
    """
    def JeanBurst(self, time):
        for character in self.characters:
            self.fanfare += character.heal(16847.0)
        return "Jean Burst", self.fanfare

    def JeanBurstTick(self, time):
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
    
    def BennettBurst(self, time):
        """
        Bennett's Burst.
        """
        return "Bennett Burst", self.fanfare
    
    def BennettBurstTick(self, time):
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
        super().generate_timeline(xiao_start=6.75)

        self.add(6.0, self.BennettBurst)
        
        # Bennett Burst Ticks
        # First one heals Bennett
        self.add(6.0, self.BennettBurstTick)
        for i in range(11):
            # First heal tick for Xiao comes on his second E
            self.add(6.0 + 1.0 * i, self.BennettBurstTick)

class XianyunC0Crane(XiaoFaruzanFurinaRotation):
    """
    Rotation with C0 Xianyun with R1 Crane.
    """
    def __init__(self, current_hp: float = 1.0):
        super().__init__(current_hp)
        self.furina = Character("Furina", 34561.0, current_hp)
        self.xianyun = Character("Xianyun", 16730.0, current_hp)
        self.characters = [self.xiao, self.faruzan, self.furina, self.xianyun]

    def XianyunEP(self, time):
        return "Xianyun EP", self.fanfare
    
    def XianyunBurst(self, time, heal=7905.0):
        for character in self.characters:
            self.fanfare += character.heal(heal)
        return "Xianyun Burst", self.fanfare

    def XianyunBurstTick(self, time, heal_amount_4no=3686.0, heal_amount=3529.0):
        heal = heal_amount_4no if time < 6.817 + 10.0 else heal_amount
        for character in self.characters:
            self.fanfare += character.heal(heal)
        return "Xianyun Burst Tick", self.fanfare
    
    def generate_timeline(self):
        super().generate_timeline()

        # Xianyun EP
        self.add(5.467, self.XianyunEP)
        
        # Xianyun Burst
        self.add(6.817, self.XianyunBurst)

        # Xianyun Burst Ticks
        for i in range(6):
            self.add(6.817 + 2.5 * (i + 1), self.XianyunBurstTick)

class XianyunC0TTDS(XianyunC0Crane):
    """
    Rotation with C0 Xianyun with R5 TTDS.
    """
    def __init__(self, current_hp: float = 1.0):
        super().__init__(current_hp)
        self.xianyun = Character("Xianyun", 20394.0, current_hp)

    def XianyunBurst(self, time):
        return super().XianyunBurst(time, heal=5823.0)

    def XianyunBurstTick(self, time):
        return super().XianyunBurstTick(time, heal_amount_4no=2716.0, heal_amount=2608.0)

class XianyunC0CraneXiaoHoma(XianyunC0Crane):
    """
    Rotation with C0 Xianyun with R1 Crane and Xiao on R1 Homa.
    """
    def __init__(self, current_hp: float = 1.0):
        super().__init__(current_hp)
        self.xiao = Character("Xiao", 21835.0, current_hp)

class XianyunC0TTDSXiaoHoma(XianyunC0TTDS):
    """
    Rotation with C0 Xianyun with R5 TTDS and Xiao on R1 Homa.
    """
    def __init__(self, current_hp: float = 1.0):
        super().__init__(current_hp)
        self.xiao = Character("Xiao", 21835.0, current_hp)

def output_result_to_file(directory, filename, results):
    """
    Write results to specified directory/filename.
    """
    filename = '{}/{}.txt'.format(directory, filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding='UTF8', newline='\n') as outfile:
        for result in results:
            outfile.write(f"{result}\n")

def main():
    configs = {
        "JeanC0_100": JeanC0(1.0),
        "JeanC0_50": JeanC0(0.5),
        "JeanC4_100": JeanC4(1.0),
        "JeanC4_50": JeanC4(0.5),
        "Bennett_100": Bennett(1.0),
        "Bennett_50": Bennett(0.5),
        "XianyunCrane": XianyunC0Crane(1.0),
        "XianyunTTDS": XianyunC0TTDS(1.0),
        "XianyunCrane_Homa": XianyunC0CraneXiaoHoma(1.0),
        "XianyunTTDS_Homa": XianyunC0TTDSXiaoHoma(1.0)
    }
    for (config_name, rotation) in configs.items():
        print(f"\n{config_name}")
        results = rotation.run()
        output_result_to_file("fanfare", config_name, results)

if __name__ == '__main__':
    main()
