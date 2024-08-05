<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://media.discordapp.net/attachments/888517252230570084/888517346963107890/e15e3701f7179ef3f8b83bafe81bac62.png?ex=66b131c3&is=66afe043&hm=0f83e44c970f3d47b57e8094ef2ce832b0c499f921f36d11c79a0533843d0f69&=&format=webp&quality=lossless&width=375&height=375" alt="Logo" width="80" height="80">
  </a>

  <h1 align="center">Xiao Mains Weapon Calculations</h3>

  <p align="center">
    Automatic generation of weapon comparison charts for Xiao.
    <br />
    <br />
    <a href="https://discord.gg/u5QS2tRHm6">
      <img src="https://img.shields.io/discord/805680025776160768?color=4eb9a0&label=.gg%2Fxiao&logo=discord&style=for-the-badge" alt="Support"/>
    </a>
    <a href="https://www.reddit.com/r/XiaoMains/">
      <img src="https://img.shields.io/reddit/subreddit-subscribers/XiaoMains?color=4eb9a0&label=r%2FXiaoMains&logo=reddit&logoColor=%4eb9a0&style=for-the-badge" alt="Reddit"/>
    </a>
    <br />
  </p>
</div>

## How to Use
Install required packages: `pip3 install -r requirements.txt`.

To run the file, you can run either `python3 main.py` from within the repo.

Weapon charts will be printed to your terminal, and weapon charts and substat distribution CSVs will be saved in `charts/` and `substats/`.

## Disclaimer
The numbers you see here assume perfect rolls for the individual weapons. A true comparison is dependent on your personal artifacts, and because of this some weapons on your Xiao will perform better/worse than what these tables display.

## Assumptions

### Stats
- 10/10/10 90/90 Xiao, t100 enemy with 10% RES.
- Atk/Anemo/Crit DMG artifact main stats.
- Artifact substats use max roll values ([see below for more info](#explaining-substat-rolls)).

### Rotation
Options:
- 2 Elemental Skills and 12 High Plunges (EE12HP)
- 2 Elemental Skills and 8 Rakes (EE8N1CJP)

### Dynamic Buffs
Dynamic buff mappings per rotation can be found here: [Xiao Weapon Calc Buff Uptime](https://docs.google.com/spreadsheets/d/1hR4dgRM6P5FHlMLTOh9D11Rcf6e6pj2gG5OM0XpOCrw/edit?usp=sharing).

## Explaining Substat Rolls
- Simulated manually via the 'damage' section on each subs page to find best DPR (damage per rotation). Balanced between Atk%, Crit Rate and Crit Damage, and capped at a maximum of 100% Crit Rate.

- Artifacts are based on 20/25 rolled stats, assuming best possible sub rolls per weapon.

- Other stats (e.g. HP, DEF, EM, ER), unless otherwise specified, will be ignored.
  - There is an option `extra_er_subs` that you can set to `True` in order to give all ER weapons 5 extra subs.

- All rolls are based on culminative amount of all 5 Artifacts with an expected outcome depending on how many substats were selected. Refer to bullet 2.

## Additional Resources
- [FFXX Weapon Comparison](https://docs.google.com/spreadsheets/d/1yeZFgWrXTxAvAVzvES36HXKf5qnwsPt-FS1QSxV3bQY/edit?usp=sharing) by felic1an
- [Xiao Weapon Comparison (verm ver.)](https://docs.google.com/spreadsheets/d/17wSBGoVTChPta3LNMEelSqJcTkX3JS8lo9XWlpeapWU/edit#gid=1335423325) by felic1an
- [Xiao Weapon Comparison](https://docs.google.com/spreadsheets/d/1CunnPmae9K4Zt-uLdI-wkBDVFVQufo5Oz1NSyU-YPA8/edit#gid=1748622433) by coded and orum
- [Github to Coded#2644's script](https://github.com/Codexys/Xiao-Mains-Scripts)

## Acknowledgements
- baeliph: Converted weapon comparison sheets into a script.
- felic1an: FFXX weapon comparisons and updated sheet for 4pc Vermillion and version 3.1.
- coded: Original weapon comparison and stat distribution scripts.
- orum: Formatting of the organized Weapon Comparison Sheet.
