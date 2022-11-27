from artifacts import *
from buffs import *
from stats import Stats
from weapons import *

from typing import List

class Xiao:
    """
    Xiao.

    Attributes:
        weapon: Xiao's weapon.
        artifacts: Xiao's artifact set.
        buffs: Xiao's team buffs.
    """

    def __init__(self, weapon: Weapon, artifact: Artifact, buffs: List[Buff]):
        self.weapon = weapon
        self.artifact = artifact
        self.buffs = buffs

        # add static base stats
        self.stats = Stats(base_hp=12736, base_atk=349.2, crate=0.242, cdmg=0.5)
        self.stats += weapon.base_stats
        self.stats += artifact.base_stats

        # keep track of damage
        self.damage_history = []
        self.total_damage = 0.0
        self.num_hits = 0

    ##################
    # Public Methods #
    ##################

    def skill(self, a4_stacks=0):
        """
        Xiao's Elemental Skill: Lemniscatic Wind Cycling
        """
        # Add dynamic buffs from A4, weapon, and buffs.
        dynamic_stats = Stats(bonus_dmg=a4_stacks * 0.15)
        dynamic_stats += self.weapon.dynamic_stats(num_stacks=a4_stacks, stats=self.stats)
        for buff in self.buffs:
            dynamic_stats += buff.buff(0)

        modifier = 4.5504
        self._dmgcalc(modifier, dynamic_stats)

    def burst(self):
        """
        Xiao's Elemental Burst: Bane of All Evil
        """
        self.stats.anemo_dmg += 0.952

    def high_plunge(self, num_plunge=1):
        """
        Xiao's High Plunge
        """
        # Add dynamic buffs from artifacts, weapon, A1, and buffs.
        dynamic_stats = self.artifact.dynamic_stats(num_plunge)
        dynamic_stats += self.weapon.dynamic_stats(num_stacks=self.num_hits, stats=self.stats)
        dynamic_stats += self._a1(num_plunge)
        for buff in self.buffs:
            dynamic_stats += buff.buff(num_plunge)
        
        modifier = 4.0402
        self._dmgcalc(modifier, dynamic_stats)
    
    ###################
    # Private Methods #
    ###################

    def _a1(self, num_plunge):
        """
        Xiao's Ascension 1 Talent
        """
        a1_bonus_dmg = 0.05
        if num_plunge <= 2:
            a1_bonus_dmg = 0.05
        elif num_plunge <= 5:
            a1_bonus_dmg = 0.10
        elif num_plunge <= 7:
            a1_bonus_dmg = 0.15
        elif num_plunge <= 10:
            a1_bonus_dmg = 0.20
        else:
            a1_bonus_dmg = 0.25
        return Stats(bonus_dmg=a1_bonus_dmg)

    def _dmgcalc(self, modifier, dynamic_stats: Stats):
        """
        Calculates damage using current effective stats.
        """
        effective_stats = self.stats + dynamic_stats

        # DMG formula.
        enemy_res_mult = self._get_enemy_res_mult(effective_stats.res_shred)
        enemy_def_mult = (190 / (190 + 200))
        dmg = effective_stats.effective_atk() * modifier * \
            (1 + effective_stats.anemo_dmg + effective_stats.bonus_dmg) * \
            enemy_res_mult * enemy_def_mult
        
        # Track damage instance.
        self.damage_history.append(dmg)
        self.total_damage += dmg
        self.num_hits += 1
    
    def _get_enemy_res_mult(self, res_shred):
        """
        Calculates enemy resistance multiplier.
        """
        resistance = 0.10 - res_shred
        if resistance < 0:
            return 1.0 - resistance/2.0
        elif resistance < 0.75:
            return 1.0 - resistance
        else:
            return 1.0/(4.0*resistance + 1.0)
