from artifacts import *
from buffs import *
from stats import Stats
from rotations import *
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

    def __init__(self, weapon: Weapon, artifact: Artifact, buffs: List[Buff], rotation: Rotation):
        self.weapon = weapon
        self.artifact = artifact
        self.buffs = buffs
        self.rotation = rotation

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

    def skill(self):
        """
        Xiao's Elemental Skill: Lemniscatic Wind Cycling
        """
        # Add dynamic buffs from A4, weapon, and buffs.
        modifier = 4.5504
        dynamic_stats = self._get_dynamic_stats(burst=False)
        self._dmgcalc(modifier, dynamic_stats)

    def burst(self):
        """
        Xiao's Elemental Burst: Bane of All Evil
        """
        self.stats.anemo_dmg += 0.952
    
    def n1(self):
        """
        Xiao's N1
        """
        modifier = 0.4914
        dynamic_stats = self._get_dynamic_stats(burst=True)
        # Xiao's N1 hits twice.
        self._dmgcalc(modifier, dynamic_stats)
        self._dmgcalc(modifier, dynamic_stats)
    
    def ca(self):
        """
        Xiao's Charged Attack.
        """
        modifier = 2.1603
        dynamic_stats = self._get_dynamic_stats(burst=True)
        self._dmgcalc(modifier, dynamic_stats)

    def high_plunge(self):
        """
        Xiao's High Plunge
        """
        modifier = 4.0402
        dynamic_stats = self._get_dynamic_stats(burst=True)
        self._dmgcalc(modifier, dynamic_stats)
    
    ###################
    # Private Methods #
    ###################

    def _a1(self):
        """
        Xiao's Ascension 1 Talent
        """
        return Stats(bonus_dmg=self.rotation.a1_bonus_dmg(self.num_hits))
    
    def _get_dynamic_stats(self, burst: bool):
        """"
        Get dynamic buffs from artifacts, weapon, passives, and buffs.
        """
        if burst:
            # Artifact and A1 buffs only apply in Burst.
            dynamic_stats = self.artifact.dynamic_stats(num_hits=self.num_hits)
            dynamic_stats += self._a1()
        else:
            # A4 buff only applies to Skills.
            dynamic_stats = Stats(bonus_dmg=self.num_hits * 0.15)

        # Weapon and support buffs apply to both skill and burst.
        dynamic_stats += self.weapon.dynamic_stats(num_hits=self.num_hits, stats=self.stats)        
        for buff in self.buffs:
            dynamic_stats += buff.buff(num_hits=self.num_hits)
        
        return dynamic_stats

    def _dmgcalc(self, modifier, dynamic_stats: Stats):
        """
        Calculates damage using current effective stats.
        """
        effective_stats = self.stats + dynamic_stats

        # DMG formula.
        enemy_res_mult = self._get_enemy_res_mult(effective_stats.res_shred)
        enemy_def_mult = (190 / (190 + 200))
        dmg = (effective_stats.total_atk() * modifier + effective_stats.flat_dmg) * \
            (1 + min(1.0, effective_stats.crate) * effective_stats.cdmg) * \
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
