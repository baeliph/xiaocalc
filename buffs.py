from rotations import *
from stats import Stats

class Buff:
    """
    Generic representation for a team buff for Xiao.

    Attributes:
        duration: Number of hits the buff lasts for. If 0, buff is always active.
        rotation: Rotation used for counting hits for buff uptime.
    """

    def __init__(self, rotation: Rotation = EE12HP()):
        self.duration = 0
        self.rotation = rotation

    def __str__(self):
        return self.__class__.__name__

    def buff(self, num_hits=0):
        """Returns the Buff's stats if active based on the current plunge or skill."""
        if self.duration == 0 or num_hits <= self.duration:
            return self.active()
        return Stats()

    def active(self):
        """Returns the bonus stats when the buff is active."""
        return Stats()
    
class Solo(Buff):
    """
    Solo. Dummy class to represent no buffs.
    """

class Bennett(Buff):
    """
    Bennett Burst buff. Gives 113% of his base ATK as flat ATK to Xiao.
    Default duration: 7 plunges for EE12HP.
    """

    def __init__(self, rotation: Rotation = EE12HP(), base_atk: int = 865):
        super().__init__(rotation)
        self.duration = rotation.buff_duration_for_benny_ttds_4no()
        self.base_atk = base_atk

    def active(self):
        modifier = 1.19 + 0.20 # T13 + C1
        return Stats(flat_atk=modifier*self.base_atk)
    

class Noblesse(Buff):
    """
    4pc Noblesse Oblige buff. Gives 20% ATK.
    Default duration: 7 plunges for EE12HP.
    """

    def __init__(self, rotation: Rotation = EE12HP()):
        super().__init__(rotation)
        self.duration = rotation.buff_duration_for_benny_ttds_4no()

    def active(self):
        return Stats(atk=0.20)
    

class TTDS(Buff):
    """
    Thrilling Tales of Dragon Slayers. Gives 48% ATK.
    Default duration: 7 plunges for EE12HP.
    """

    def __init__(self, rotation: Rotation = EE12HP()):
        super().__init__(rotation)
        self.duration = rotation.buff_duration_for_benny_ttds_4no()

    def active(self):
        return Stats(atk=0.48)
    

class GeoResonance(Buff):
    """
    Geo Resonance. Gives 20% DMG Bonus.
    """

    def active(self):
        return Stats(bonus_dmg=0.15)

class PyroResonance(Buff):
    """
    Pyro Resonance. Gives 25% ATK.
    """

    def active(self):
        return Stats(atk=0.25)

class Zhongli(Buff):
    """
    Zhongli Shield. 20% Res Shred.
    """

    def active(self):
        return Stats(res_shred=0.20)

class FaruzanC2(Buff):
    """
    C2 Faruzan. 32.4% Anemo DMG Bonus, 30% Anemo Res Shred.
    Assumes Favonius Warbow for base ATK.
    """

    def __init__(self, rotation: Rotation = EE12HP(), base_atk: int = 650):
        super().__init__(rotation)
        self.base_atk = base_atk

    def buff(self, num_hits=0):
        flat_dmg = 0.32*self.base_atk if self.rotation.faruzan_a4_active(num_hits) else 0.0
        return Stats(anemo_dmg=0.324, res_shred=0.30, flat_dmg=flat_dmg)


class FaruzanC6(Buff):
    """
    C6 Faruzan. 40% Anemo Crit DMG, 38.3% Anemo DMG Bonus, 30% Anemo Res Shred.
    Assumes Elegy for base ATK.
    """

    def __init__(self, rotation: Rotation = EE12HP(), base_atk: int = 804):
        super().__init__(rotation)
        self.base_atk = base_atk

    def buff(self, num_hits=0):
        flat_dmg = 0.32*self.base_atk if self.rotation.faruzan_a4_active(num_hits) else 0.0
        return Stats(cdmg=0.40, anemo_dmg=0.383, res_shred=0.30, flat_dmg=flat_dmg)
