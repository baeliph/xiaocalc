from stats import Stats
from rotations import *
from weapons import *

class Artifact:
    """
    Represents artifact sets.
    """
    
    def __init__(self, rotation: Rotation = EE12HP()):
        self.base_stats = Stats(flat_hp=4780, flat_atk=311, atk=0.466, anemo_dmg=0.466, cdmg=0.622)
        self.rotation = rotation
    
    def __str__(self):
        return self.__class__.__name__
    
    def dynamic_stats(self, num_hits=0):
        """Dynamic stats provided by artifacts. e.g., 4pc Vermillion."""
        return Stats()

class Vermillion(Artifact):
    """
    4pc Vermillion Hereafter.
    """

    def __init__(self, rotation: Rotation = EE12HP()):
        super().__init__(rotation)
        self.base_stats.atk += 0.18

    def dynamic_stats(self, num_hits=0):
        num_stacks = self.rotation.vermillion_stacks(num_hits)
        return Stats(atk=0.08 + 0.1*num_stacks)

class AtkAtk(Artifact):
    """
    2pc +18% ATK, 2pc +18% ATK.
    """

    def __init__(self, rotation: Rotation = EE12HP()):
        super().__init__(rotation)
        self.base_stats.atk += 0.36
    
class AtkAnemo(Artifact):
    """
    2pc +18% ATK, 2pc +15% Anemo DMG.
    """

    def __init__(self, rotation: Rotation = EE12HP()):
        super().__init__(rotation)
        self.base_stats.atk += 0.18
        self.base_stats.anemo_dmg += 0.15

class DesertPavilion(Artifact):
    """
    4pc Desert Pavilion's Chronicle.
    """

    def __init__(self, rotation: Rotation = EE12HP()):
        super().__init__(rotation)
        self.base_stats.anemo_dmg += 0.30
    
    def dynamic_stats(self, num_hits=0):
        if isinstance(self.rotation, EE8N1CJP) and num_hits > 4:
            return Stats(bonus_dmg=0.40)
        return Stats()
