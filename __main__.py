from artifacts import *
from buffs import *
from weapons import *
from xiao import Xiao

import csv
from functools import partial
import os
import pandas as pd
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

def optimize(num_subs: int, artifact_set, weapon: Weapon, buffs, verbose=False):
    """
    Optimize rotation damage across all substat combinations for given
    artifact set, weapon, and buffs.

    Returns:
        (atk, crate, cdmg, max_dmg): optimal substat distribution and damage
    """
    max_dmg = -1
    max_subs = ()
    for crate in range(0, num_subs + 1):
        for cdmg in range(0, num_subs - crate + 1):
            atk = num_subs - crate - cdmg

            artifact = artifact_set()
            artifact.base_stats.add_artifact_subs(atk=atk, crate=crate, cdmg=cdmg)

            dmg = rotation_dmg(weapon, artifact, buffs)
            if verbose:
                print('atk: {}, crate: {}, cdmg: {}, dmg: {}'.format(atk, crate, cdmg, dmg))
            if dmg > max_dmg:
                max_dmg = dmg
                max_subs = (atk, crate, cdmg, max_dmg)
    return max_subs

def write_csv(directory, filename, data):
    """
    Write data as CSV to specified directory/filename.
    """
    filename = '{}/{}'.format(directory, filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding='UTF8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(data)

def main(num_subs, artifact_set, buff_combos, weapons):
    for buffs in buff_combos:
        # Output.
        weapon_chart = [["Weapon", "R1", "R2", "R3", "R4", "R5"]]
        optimal_substats = [['weapon', 'refine', 'atk', 'crate', 'cdmg']]
        
        for weapon in weapons:
            weapon_name = str(weapon(1))
            row = [weapon_name]
            for refine in range(1, 6):
                atk, crate, cdmg, dmg = optimize(num_subs, artifact_set, weapon(refine), buffs)
                # Save results
                optimal_substats.append([weapon_name, 'R{}'.format(refine), atk, crate, cdmg])
                row.append(dmg)
            weapon_chart.append(row)
    
        # Print weapon chart to stdout.
        weapon_chart[1:] = sorted(weapon_chart[1:], key=lambda row: row[1], reverse=True)
        print('\nBuffs: [{}]'.format(", ".join(map(str, buffs))))
        print(tabulate(weapon_chart, headers='firstrow'))

        # Save weapon chart and substat distributions to CSVs.
        filename = '{}subs/{}.csv'.format(num_subs, "-".join(map(str, buffs)))
        write_csv('charts', filename, weapon_chart)
        write_csv('substats', filename, optimal_substats)

if __name__ == '__main__':
    """
    Configure your comparison parameters here.
        num_subs: Number of artifact substats.
        artifact_set: Artifact set.
        buff_combos: Buff combinations. Each combo corresponds to one output chart.
        weapons: List of weapons to compare for each chart.
    """

    num_subs = 20

    artifact_set = Vermillion

    buff_combos = [
        [Solo()],
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

    main(num_subs, artifact_set, buff_combos, weapons)
