class Stats:
    """
    Represents Genshin stats for any character, weapon, artifact, etc.
    """

    #################
    # Magic Methods #
    #################

    def __init__(
        self, base_atk=0.0, flat_atk=0.0, atk=0.0, base_hp=0.0, flat_hp=0.0,
        hp=0.0, em=0.0, crate=0.0, cdmg=0.0, anemo_dmg=0.0, bonus_dmg=0.0,
        res_shred=0.0, flat_dmg=0.0
    ):
        self.base_atk = base_atk
        self.flat_atk = flat_atk
        self.atk = atk
        self.base_hp = base_hp
        self.flat_hp = flat_hp
        self.hp = hp
        self.em = em
        self.crate = crate
        self.cdmg = cdmg
        self.anemo_dmg = anemo_dmg
        self.bonus_dmg = bonus_dmg
        self.res_shred = res_shred
        self.flat_dmg = flat_dmg

    def __add__(self, other):
        return Stats(
            self.base_atk + other.base_atk,
            self.flat_atk + other.flat_atk,
            self.atk + other.atk,
            self.base_hp + other.base_hp,
            self.flat_hp + other.flat_hp,
            self.hp + other.hp,
            self.em + other.em,
            self.crate + other.crate,
            self.cdmg + other.cdmg,
            self.anemo_dmg + other.anemo_dmg,
            self.bonus_dmg + other.bonus_dmg,
            self.res_shred + other.res_shred,
            self.flat_dmg + other.flat_dmg
        )

    def __iadd__(self, other):
        self.base_atk += other.base_atk
        self.flat_atk += other.flat_atk
        self.atk += other.atk
        self.base_hp += other.base_hp
        self.flat_hp += other.flat_hp
        self.hp += other.hp
        self.em += other.em
        self.crate += other.crate
        self.cdmg += other.cdmg
        self.anemo_dmg += other.anemo_dmg
        self.bonus_dmg += other.bonus_dmg
        self.res_shred += other.res_shred
        self.flat_dmg += other.flat_dmg
        return self
    
    def __str__(self):
        stats_dict = self.__dict__
        for k,v in stats_dict.items():
            stats_dict[k] = round(v, 3)
        return str(stats_dict)

    ##################
    # Public Methods #
    ##################
    
    def total_atk(self):
        """Returns the total ATK."""
        return self.base_atk * (1 + self.atk) + self.flat_atk

    def total_hp(self):
        """Returns the total HP."""
        return self.base_hp * (1 + self.hp) + self.flat_hp

    def add_artifact_subs(self, flat_atk=0, atk=0, flat_hp=0, hp=0, em=0, crate=0, cdmg=0):
        """
        Adds the specified number of artifact subs to stats. Uses max roll value.
        """
        self.flat_atk += flat_atk * 19.45
        self.atk += atk * 0.0583
        self.flat_hp += flat_hp * 298.75
        self.hp += hp * 0.0583
        self.em += em * 23.31
        self.crate += crate * 0.0389
        self.cdmg += cdmg * 0.0777
    
    def add_mean_artifact_subs(self, flat_atk=0, atk=0, flat_hp=0, hp=0, em=0, crate=0, cdmg=0):
        """
        Adds the specified number of artifact subs to stats. Uses mean roll value.
        """
        self.flat_atk += flat_atk * 16.535
        self.atk += atk * 0.04955
        self.flat_hp += flat_hp * 253.94
        self.hp += hp * 0.04955
        self.em += em * 19.82
        self.crate += crate * 0.0331
        self.cdmg += cdmg * 0.0662
