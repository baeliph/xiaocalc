<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://media.discordapp.net/attachments/888517252230570084/888517346963107890/e15e3701f7179ef3f8b83bafe81bac62.png" alt="Logo" width="80" height="80">
  </a>

  <h1 align="center">Xiao Mains Weapon Calculations</h3>

  <p align="center">
    Automatic generation of weapon comparison charts for Xiao.
    <br />
    <a href="https://discord.gg/xiao"><strong>discord.gg/xiao</strong></a>
    <br />
  </p>
</div>

## How to Use
- tabulate: `pip install tabulate`
- pyyaml: `pip install pyyaml`

To run the file, you can run either `python3 .` or `python3 __main__.py` from within the repo.

## Disclaimer
**This is a WIP.** The following remain to be implemented:
- Different substat distributions per weapon per refine per buff combos.
- Automatic optimal substat distribution calculation.
- Engulfing Lightning, Staff of Scarlet Sands, other 4* spears.

The numbers you see here assume perfect rolls for the individual weapons. A true comparison is dependent on your personal artifacts, and because of this some weapons on your Xiao will perform better/worse than what these tables display.

## Assumptions

### Stats
- 10/10/10 90/90 Xiao, t100 enemy with 10% RES.
- Atk/Anemo/Crit DMG artifact main stats.
- Artifact substats use max roll values ([see below for more info](#explaining-substat-rolls)).

### Rotation
- 2 Elemental Skills and 12 High Plunges.

### Weapons
- 100% Passive Uptime taken for Shifting Windblade (On)

### Buffs
- Bennett: 865 Base T13. Duration: 7 plunges.
- TTDS: Duration: 7 plunges.
- 4pc NO: Duration: 7 plunges.
- Zhongli and C6 Faruzan: Full uptime.

## Explaining Substat Rolls
- Simulated manually via the 'damage' section on each subs page to find best DPR (damage per rotation). Balanced between Atk%, Crit Rate and Crit Damage, and capped at a maximum of 100% Crit Rate.

- Artifacts are based on 20 rolled stats (4 base + 5 level ups x 5 total artifacts) assuming best possible sub rolls per weapon.

- Taken for 4pc Vermillion Hereafter. Other stats (e.g. HP, DEF, EM, ER), unless otherwise specified will be ignored.

- All rolls are based on culminative amount of all 5 Artifacts with an expected outcome depending on how many substats were selected. Refer to 2.

## Additional Resources
- [Xiao Weapon Comparison (verm ver.)](https://docs.google.com/spreadsheets/d/17wSBGoVTChPta3LNMEelSqJcTkX3JS8lo9XWlpeapWU/edit#gid=1335423325) by Felician#5771
- [Xiao Weapon Comparison](https://docs.google.com/spreadsheets/d/1CunnPmae9K4Zt-uLdI-wkBDVFVQufo5Oz1NSyU-YPA8/edit#gid=1748622433) by Coded#2644 and Orum#8459
- [Github to Coded#2644's script](https://github.com/Codexys/Xiao-Mains-Scripts)

## Acknowledgements
- baeliph#8346: Converted weapon comparison sheets into a script.
- Felician#5771: Updated sheet for 4pc Vermillion and version 3.1.
- Coded#2644: Original weapon comparison and stat distribution scripts.
- Orum#8459: Formatting of the organized Weapon Comparison Sheet.
