from stats import Stats
from weapons import *

class Artifact:
    """
    Represents artifact sets.
    """
    
    def __init__(self):
        self.base_stats = Stats(flat_hp=4780, flat_atk=311, atk=0.466, anemo_dmg=0.466, cdmg=0.622)
    
    def dynamic_stats(self, num_plunge=0):
        """Dynamic stats provided by artifacts. e.g., 4pc Vermillion."""
        return Stats()

class Vermillion(Artifact):
    """
    4pc Vermillion Hereafter.
    """

    def __init__(self):
        super().__init__()
        self.base_stats.atk += 0.18

    def dynamic_stats(self, num_plunge=0):
        num_stacks = min(num_plunge, 4)
        return Stats(atk=0.08 + 0.1*num_stacks)

class AtkAtk(Artifact):
    """
    2pc +18% ATK, 2pc +18% ATK.
    """

    def __init__(self):
        super().__init__()
        self.base_stats.atk += 0.36
    
class AtkAnemo(Artifact):
    """
    2pc +18% ATK, 2pc +15% Anemo DMG.
    """

    def __init__(self):
        super().__init__()
        self.base_stats.atk += 0.18
        self.base_stats.anemo_dmg += 0.15
