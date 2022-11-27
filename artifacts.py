from stats import Stats
from weapons import *

class Artifact:
    """
    Represents artifact sets.

    Attributes:
        weapon: Determines substat distribution based on given weapon.
    """
    
    def __init__(self, weapon: Weapon):
        self.base_stats = Stats(flat_hp=4780, flat_atk=311, atk=0.466, anemo_dmg=0.466, cdmg=0.622)

        if isinstance(weapon, PJWS):
            self.base_stats.add_artifact_subs(crate=11, cdmg=9)
        elif isinstance(weapon, Homa):
            self.base_stats.add_artifact_subs(crate=18, cdmg=2)        
        elif isinstance(weapon, Vortex):
            self.base_stats.add_artifact_subs(crate=14, cdmg=6)
        elif isinstance(weapon, CalamityQueller):
            self.base_stats.add_artifact_subs(crate=14, cdmg=6)
        elif isinstance(weapon, SkywardSpine):
            if weapon.refine < 4:
                self.base_stats.add_artifact_subs(crate=13, cdmg=7)
            else:
                self.base_stats.add_artifact_subs(crate=12, cdmg=8)
        elif isinstance(weapon, Deathmatch):
            self.base_stats.add_artifact_subs(crate=9, cdmg=11)
        elif isinstance(weapon, Blackcliff):
            self.base_stats.add_artifact_subs(crate=18, cdmg=2)
        elif isinstance(weapon, MissiveWindspear):
            self.base_stats.add_artifact_subs(crate=14, cdmg=6)
        elif isinstance(weapon, Lithic):
            # TODO: Support different substats based on refine and stacks.
            self.base_stats.add_artifact_subs(crate=13, cdmg=7)
        else:
            raise Exception("No stat distribution for weapon.")
    
    def dynamic_stats(self, num_plunge=0):
        """Dynamic stats provided by artifacts. e.g., 4pc Vermillion."""
        return Stats()

class Vermillion(Artifact):
    """
    4pc Vermillion Hereafter.
    """

    def __init__(self, weapon: Weapon):
        super().__init__(weapon)
        self.base_stats.atk += 0.18

    def dynamic_stats(self, num_plunge=0):
        num_stacks = min(num_plunge, 4)
        return Stats(atk=0.08 + 0.1*num_stacks)

class AtkAtk(Artifact):
    """
    2pc +18% ATK, 2pc +18% ATK.
    """

    def __init__(self, weapon: Weapon):
        super().__init__(weapon)
        self.base_stats.atk += 0.36
    
class AtkAnemo(Artifact):
    """
    2pc +18% ATK, 2pc +15% Anemo DMG.
    """

    def __init__(self, weapon: Weapon):
        super().__init__(weapon)
        self.base_stats.atk += 0.18
        self.base_stats.anemo_dmg += 0.15
