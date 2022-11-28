from stats import Stats

class Buff:
    """
    Generic representation for a team buff for Xiao.

    Attributes:
        duration: Number of plunges the buff lasts for. If 0, buff is always active.
    """

    def __init__(self, duration: int = 0):
        self.duration = duration

    def __str__(self):
        return self.__class__.__name__

    def buff(self, num_plunge=0, num_skill=0):
        """Returns the Buff's stats if active based on the current plunge or skill."""
        if self.duration == 0 or num_plunge <= self.duration:
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
    Default duration: 7 plunges.
    """

    def __init__(self, duration: int = 7, base_atk: int = 865):
        super().__init__(duration)
        self.base_atk = base_atk

    def active(self):
        modifier = 1.19 + 0.20 # T13 + C1
        return Stats(flat_atk=modifier*self.base_atk)
    

class Noblesse(Buff):
    """
    4pc Noblesse Oblige buff. Gives 20% ATK.
    Default duration: 7 plunges.
    """

    def __init__(self, duration: int = 7):
        super().__init__(duration)

    def active(self):
        return Stats(atk=0.20)
    

class TTDS(Buff):
    """
    Thrilling Tales of Dragon Slayers. Gives 48% ATK.
    Default duration: 7 plunges.
    """

    def __init__(self, duration: int = 7):
        super().__init__(duration)

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

class FaruzanC6(Buff):
    """
    C6 Faruzan. 40% Anemo Crit DMG, 38.3% Anemo DMG Bonus, 30% Anemo Res Shred.
    TODO: Implement A4 flat damage increase.
    """

    def __init__(self, duration: int = 0, base_atk: int = 804):
        super().__init__(duration)
        self.base_atk = base_atk

    def buff(self, num_plunge=0, num_skill=0):
        if num_skill == 2:
            # Faruzan's A4 flat dmg increase is on CD during Xiao's 2nd E.
            return Stats(cdmg=0.40, anemo_dmg=0.383, res_shred=0.30)
        return Stats(cdmg=0.40, anemo_dmg=0.383, res_shred=0.30, flat_dmg=0.32*self.base_atk)
