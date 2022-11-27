from stats import Stats

class Weapon:
    """
    Represents a weapon.

    Attributes:
        refine: Weapon refinement. Must be between [1, 5].
    """

    def __init__(self, refine: int = 1):
        self.base_stats = Stats()
        self.refine = refine

    def __str__(self):
        return self.__class__.__name__
    
    def dynamic_stats(self, num_stacks, stats: Stats):
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

    Attributes:
        refine: Weapon refinement. Must be between [1, 5].
        stacked: True if weapon is prestacked.
    """

    def __init__(self, refine: int = 1, stacked: bool = False):
        super().__init__(refine)
        self.base_stats = Stats(base_atk=674, crate=0.221)
        self.stacked = stacked

    def __str__(self):
        output = super().__str__()
        if self.stacked:
            output += " (Stacked)"
        return output

    def dynamic_stats(self, num_stacks, stats: Stats):
        atk_increase = self._stat(0.032, 0.007)
        bonus_dmg = self._stat(0.12, 0.03)

        if num_stacks < 7 and not self.stacked:
            return Stats(atk=num_stacks*atk_increase)
        else:
            return Stats(atk=7*atk_increase, bonus_dmg=bonus_dmg)
    

class Homa(Weapon):
    """
    Staff of Homa.

    Attributes:
        refine: Weapon refinement. Must be between [1, 5].
        below50: True if character HP is below 50%.
    """

    def __init__(self, refine: int = 1, below50: bool = False):
        super().__init__(refine)
        hp_increase = self._stat(0.20, 0.05)
        self.base_stats = Stats(base_atk=608, hp=hp_increase, cdmg=0.662)
        self.below50 = below50

    def __str__(self):
        output = super().__str__()
        if self.below50:
            output += " (50%)"
        return output

    def dynamic_stats(self, num_stacks, stats: Stats):
        atk_increase = self._stat(0.018, 0.004) if self.below50 else self._stat(0.008, 0.002)
        return Stats(flat_atk=atk_increase*stats.total_hp())
    

class Vortex(Weapon):
    """
    Vortex Vanquisher.

    Attributes:
        refine: Weapon refinement. Must be between [1, 5].
        shielded: True if character is shielded.
        stacked: True if weapon is prestacked.
    """

    def __init__(self, refine: int = 1, shielded: bool = False, stacked: bool = False):
        super().__init__(refine)
        self.base_stats = Stats(base_atk=608, atk=0.496)
        self.shielded = shielded
        self.stacked = stacked
    
    def __str__(self):
        shielded = "Shielded" if self.shielded else "Unshielded"
        stacked = "Stacked" if self.stacked else "Unstacked"
        return '{} ({}, {})'.format(super().__str__(), shielded, stacked)

    def dynamic_stats(self, num_stacks, stats: Stats):
        num_stacks = 5 if self.stacked else min(num_stacks, 5)
        atk_increase = self._stat(0.08, 0.02) if self.shielded else self._stat(0.04, 0.01)
        return Stats(atk=num_stacks*atk_increase)

class CalamityQueller(Weapon):
    """
    Calamity Queller.

    Attributes:
        refine: Weapon refinement. Must be between [1, 5].
        stacked: True if weapon is prestacked.
    """

    def __init__(self, refine: int = 1, stacked: bool = False):
        super().__init__(refine)
        self.base_stats = Stats(base_atk=741, atk=0.165, bonus_dmg=self._stat(0.12, 0.03))
        self.stacked = stacked
    
    def __str__(self):
        stacked = "Stacked" if self.stacked else "Unstacked"
        return '{} ({})'.format(super().__str__(), stacked)

    def dynamic_stats(self, num_stacks, stats: Stats):
        atk_increase = self._stat(0.032, 0.008)
        if num_stacks >= 5 or self.stacked:
            # 5th hit / 4th plunge onwards has full stacks.
            return Stats(atk=6*atk_increase)
        elif num_stacks == 4:
            # 4th hit / 3rd plunge has 5 stacks.
            return Stats(atk=5*atk_increase)
        else:
            # nth hit has n stacks.
            return Stats(atk=num_stacks*atk_increase)


class SkywardSpine(Weapon):
    """
    Skyward Spine.

    Attributes:
        refine: Weapon refinement. Must be between [1, 5].
    """

    def __init__(self, refine: int = 1):
        super().__init__(refine)
        self.base_stats = Stats(base_atk=674, crate=self._stat(0.08, 0.02))


class Lithic(Weapon):
    """
    Lithic Spear.

    Attributes:
        refine: Weapon refinement. Must be between [1, 5].
        stacks: Number of stacks to assume. Must be between [1, 4].
    """

    def __init__(self, refine: int = 1, stacks: int = 1):
        super().__init__(refine)
        self.base_stats = Stats(base_atk=565, atk=0.276)
        self.stacks = stacks
    
    def __str__(self):
        return '{} ({} Stacks)'.format(super().__str__(), self.stacks)
    
    def dynamic_stats(self, num_stacks, stats: Stats):
        atk_increase = self._stat(0.07, 0.01) * self.stacks
        crate_increase = self._stat(0.03, 0.01) * self.stacks
        return Stats(atk=atk_increase, crate=crate_increase)


class Deathmatch(Weapon):
    """
    The Deathmatch.

    Attributes:
        refine: Weapon refinement. Must be between [1, 5].
        num_opponents: Number of opponents near character.
    """
    
    def __init__(self, refine: int = 1, num_opponents: int = 1):
        super().__init__(refine)
        self.base_stats = Stats(base_atk=454, crate=0.368)
        self.num_opponents = num_opponents
    
    def __str__(self):
        num_opponents = "1 Opponent" if self.num_opponents < 2 else "2+ Opponents"
        return '{} ({})'.format(super().__str__(), num_opponents)
    
    def dynamic_stats(self, num_stacks, stats: Stats):
        atk_increase = self._stat(0.24, 0.06) if self.num_opponents < 2 else self._stat(0.16, 0.04)
        return Stats(atk=atk_increase)


class Blackcliff(Weapon):
    """
    Blackcliff Pole.

    Attributes:
        refine: Weapon refinement. Must be between [1, 5].
        stacks: Number of stacks to assume. Must be between [0, 3].
    """

    def __init__(self, refine: int = 1, stacks: int = 0):
        super().__init__(refine)
        self.base_stats = Stats(base_atk=510, cdmg=0.551)
        self.stacks = stacks
    
    def __str__(self):
        return '{} ({} Stacks)'.format(super().__str__(), self.stacks)
    
    def dynamic_stats(self, num_stacks, stats: Stats):
        atk_increase = self._stat(0.12, 0.03) * self.stacks
        return Stats(atk=atk_increase)


class MissiveWindspear(Weapon):
    """
    Missive Windspear.

    Attributes:
        refine: Weapon refinement. Must be between [1, 5].
        passive_active: True if passive is active.
    """

    def __init__(self, refine: int = 1, passive_active: bool = False):
        super().__init__(refine)
        self.base_stats = Stats(base_atk=510, atk=0.4135)
        self.passive_active = passive_active
    
    def __str__(self):
        return '{} ({})'.format(super().__str__(), "On" if self.passive_active else "Off")
    
    def dynamic_stats(self, num_stacks, stats: Stats):
        if self.passive_active:
            return Stats(atk=self._stat(0.12, 0.03))
        return Stats()
