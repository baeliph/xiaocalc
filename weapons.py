from rotations import *
from stats import Stats

class Weapon:
    """
    Represents a weapon.

    Attributes:
        refine: Weapon refinement. Must be between [1, 5].
        rotation: Xiao rotation combo. Default: EE12HP
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP()):
        self.base_stats = Stats()
        self.refine = refine
        self.rotation = rotation

    def __str__(self):
        return self.__class__.__name__
    
    def dynamic_stats(self, num_hits, stats: Stats):
        """
        Calculate weapon passive stats based on dynamic stacks and current stats.
        """
        return Stats()

    def _stat(self, base, increase):
        """
        Private method. Calculate stats that increase based on weapon refinement.
        """
        return base + increase * (self.refine - 1)
    

class PJWS(Weapon):
    """
    Primordial Jade Winged-Spear.

    Additional Attributes:
        stacked: True if weapon is prestacked.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP(), stacked: bool = False):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=674, crate=0.221)
        self.stacked = stacked

    def __str__(self):
        output = super().__str__()
        if self.stacked:
            output += " (Stacked)"
        return output

    def dynamic_stats(self, num_hits, stats: Stats):
        atk_increase = self._stat(0.032, 0.007)
        bonus_dmg = self._stat(0.12, 0.03)

        if num_hits < 7 and not self.stacked:
            return Stats(atk=num_hits*atk_increase)
        else:
            return Stats(atk=7*atk_increase, bonus_dmg=bonus_dmg)
    

class Homa(Weapon):
    """
    Staff of Homa.

    Additional Attributes:
        below50: True if character HP is below 50%.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP(), below50: bool = False):
        super().__init__(refine, rotation)
        hp_increase = self._stat(0.20, 0.05)
        self.base_stats = Stats(base_atk=608, hp=hp_increase, cdmg=0.662)
        self.below50 = below50

    def __str__(self):
        output = super().__str__()
        if self.below50:
            output += " (50%)"
        return output

    def dynamic_stats(self, num_hits, stats: Stats):
        atk_increase = self._stat(0.018, 0.004) if self.below50 else self._stat(0.008, 0.002)
        return Stats(flat_atk=atk_increase*stats.total_hp())
    

class Vortex(Weapon):
    """
    Vortex Vanquisher.

    Additional Attributes:
        shielded: True if character is shielded.
        stacked: True if weapon is prestacked.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP(), shielded: bool = False, stacked: bool = False):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=608, atk=0.496)
        self.shielded = shielded
        self.stacked = stacked
    
    def __str__(self):
        shielded = "Shielded" if self.shielded else "Unshielded"
        stacked = "Stacked" if self.stacked else "Unstacked"
        return '{} ({}, {})'.format(super().__str__(), shielded, stacked)

    def dynamic_stats(self, num_hits, stats: Stats):
        num_hits = 5 if self.stacked else min(num_hits, 5)
        atk_increase = self._stat(0.08, 0.02) if self.shielded else self._stat(0.04, 0.01)
        return Stats(atk=num_hits*atk_increase)

class CalamityQueller(Weapon):
    """
    Calamity Queller.

    Additional Attributes:
        stacked: True if weapon is prestacked.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP(), stacked: bool = False):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=741, atk=0.165, bonus_dmg=self._stat(0.12, 0.03))
        self.stacked = stacked
    
    def __str__(self):
        stacked = "Stacked" if self.stacked else "Unstacked"
        return '{} ({})'.format(super().__str__(), stacked)

    def dynamic_stats(self, num_hits, stats: Stats):
        atk_increase = self._stat(0.032, 0.008) 
        stacks = 6 if self.stacked else self.rotation.calamity_stacks(num_hits)
        return Stats(atk=stacks*atk_increase)

class SkywardSpine(Weapon):
    """
    Skyward Spine.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP()):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=674, crate=self._stat(0.08, 0.02), er=0.368)


class EngulfingLightning(Weapon):
    """
    Engulfing Lightning.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP()):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=608, er=0.551)
    
    def dynamic_stats(self, num_hits, stats: Stats):
        active_er = stats.er
        if self.rotation.engulfing_active(num_hits):
            active_er += self._stat(0.30, 0.05)
        atk_increase = self._stat(0.28, 0.07) * active_er
        return Stats(atk=atk_increase)


class StaffOfTheScarletSands(Weapon):
    """
    Staff of the Scarlet Sands.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP()):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=542, crate=0.441)
    
    def dynamic_stats(self, num_hits, stats: Stats):
        atk_increase = self._stat(0.52, 0.13) + self._stat(0.28, 0.07) * self.rotation.soss_stacks(num_hits)
        return Stats(flat_atk=atk_increase * stats.em)
    
class LumidouceElegy(Weapon):
    """
    Lumidouce Elegy.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP()):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=608, crate=0.331, atk=self._stat(0.15, 0.04))

class FracturedHalo(Weapon):
    """
    Fractured Halo.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP()):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=608, cdmg=0.662, atk=self._stat(0.24, 0.06))

class SacrificersStaff(Weapon):
    """
    Sacrificer's Staff.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP()):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=620, crate=0.092)
    
    def dynamic_stats(self, num_hits, stats: Stats):
        atk_increase = self._stat(0.08, 0.02) * self.rotation.sacstaff_stacks(num_hits)
        return Stats(atk=atk_increase)


class Lithic(Weapon):
    """
    Lithic Spear.

    Additional Attributes:
        stacks: Number of stacks to assume. Must be between [1, 4].
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP(), stacks: int = 1):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=565, atk=0.276)
        self.stacks = stacks
    
    def __str__(self):
        return '{} ({} Stacks)'.format(super().__str__(), self.stacks)
    
    def dynamic_stats(self, num_hits, stats: Stats):
        atk_increase = self._stat(0.07, 0.01) * self.stacks
        crate_increase = self._stat(0.03, 0.01) * self.stacks
        return Stats(atk=atk_increase, crate=crate_increase)


class Deathmatch(Weapon):
    """
    The Deathmatch.

    Additional Attributes:
        num_opponents: Number of opponents near character.
    """
    
    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP(), num_opponents: int = 1):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=454, crate=0.368)
        self.num_opponents = num_opponents
    
    def __str__(self):
        num_opponents = "1 Opponent" if self.num_opponents < 2 else "2+ Opponents"
        return '{} ({})'.format(super().__str__(), num_opponents)
    
    def dynamic_stats(self, num_hits, stats: Stats):
        atk_increase = self._stat(0.24, 0.06) if self.num_opponents < 2 else self._stat(0.16, 0.04)
        return Stats(atk=atk_increase)


class Blackcliff(Weapon):
    """
    Blackcliff Pole.

    Additional Attributes:
        stacks: Number of stacks to assume. Must be between [0, 3].
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP(), stacks: int = 0):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=510, cdmg=0.551)
        self.stacks = stacks
    
    def __str__(self):
        return '{} ({} Stacks)'.format(super().__str__(), self.stacks)
    
    def dynamic_stats(self, num_hits, stats: Stats):
        atk_increase = self._stat(0.12, 0.03) * self.stacks
        return Stats(atk=atk_increase)


class MissiveWindspear(Weapon):
    """
    Missive Windspear.

    Additional Attributes:
        passive_active: True if passive is active.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP(), passive_active: bool = False):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=510, atk=0.4135)
        self.passive_active = passive_active
    
    def __str__(self):
        return '{} ({})'.format(super().__str__(), "On" if self.passive_active else "Off")
    
    def dynamic_stats(self, num_hits, stats: Stats):
        if self.passive_active:
            return Stats(atk=self._stat(0.12, 0.03))
        return Stats()


class WavebreakersFin(Weapon):
    """
    Wavebreaker's Fin.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP()):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=620, atk=0.138)


class FavoniusLance(Weapon):
    """
    Favonius Lance.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP()):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=565, er=0.306)


class PrototypeStarglitter(Weapon):
    """
    Prototype Starglitter.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP()):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=510, er=0.459)


class WhiteTassel(Weapon):
    """
    White Tassel.
    """

    def __init__(self, refine: int = 1, rotation: Rotation = EE12HP()):
        super().__init__(refine, rotation)
        self.base_stats = Stats(base_atk=401, crate=0.234)
