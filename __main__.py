from artifacts import *
from buffs import *
from weapons import *
from xiao import Xiao

from functools import partial
from tabulate import tabulate

def rotation_dmg(weapon: Weapon, artifact: Artifact, buffs, verbose=False):
    """
    Calculates Xiao's total damage over a single EE Q 12HP rotation.
    """
    xiao = Xiao(weapon, artifact, buffs)

    # Rotation: EE Q 12HP
    xiao.skill()
    xiao.skill(1)
    xiao.burst()
    for i in range(1, 13):
        xiao.high_plunge(i)

    if verbose:
        print('Weapon: {} R{}'.format(weapon, weapon.refine))
        print('Artifact: {}'.format(artifact.__class__.__name__))
        print('Total DMG (EE Q 12HP): {}\n'.format(xiao.total_damage))

    return xiao.total_damage

if __name__ == '__main__':
    header = ["Weapon", "R1", "R2", "R3", "R4", "R5"]

    buff_combos = [
        [],
        [TTDS()],
        [Bennett(), Noblesse()],
        [TTDS(), Bennett(), Noblesse()],
        [FaruzanC6()]
    ]

    weapons = [
        partial(PJWS),
        partial(PJWS, stacked=True),
        partial(Homa),
        partial(Homa, below50=True),
        partial(Vortex, shielded=False, stacked=False),
        partial(Vortex, shielded=False, stacked=True),
        partial(Vortex, shielded=True, stacked=False),
        partial(Vortex, shielded=True, stacked=True),
        partial(CalamityQueller, stacked=False),
        partial(CalamityQueller, stacked=True),
        partial(SkywardSpine),
        partial(Lithic, stacks=1),
        partial(Lithic, stacks=2),
        partial(Lithic, stacks=3),
        partial(Lithic, stacks=4),
        partial(Deathmatch, num_opponents=1),
        partial(Deathmatch, num_opponents=2),
        partial(Blackcliff, stacks=0),
        partial(Blackcliff, stacks=1),
        partial(Blackcliff, stacks=2),
        partial(Blackcliff, stacks=3),
        partial(MissiveWindspear, passive_active=False),
        partial(MissiveWindspear, passive_active=True)
    ]
    
    for buffs in buff_combos:
        table = []
        for weapon in weapons:
            row = [str(weapon(1))]
            for refine in range(1, 6):
                weapon_with_refine = weapon(refine)
                artifact = Vermillion(weapon_with_refine)
                dmg = rotation_dmg(weapon_with_refine, artifact, buffs)
                row.append(dmg)
            table.append(row)
    
        table.sort(key=lambda row: row[1], reverse=True)
        print('\nBuffs: [{}]'.format(", ".join(map(str, buffs))))
        print(tabulate(table, headers=header))
