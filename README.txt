Welcome to RAID BOSS! An interavtive way to cooperatively play commander with the homies.

This is currently a text based application but we hope to involve graphiocs at a later date.
Probably TKinter first- sorry.

The boss monster has 250X life (ex. 2X = 2 times the number of players in the game). 
50X poison is required to defeat the boss monster. Each turn, roll 2d6 per the turn number divided by 2,
 rounded down. For hard mode, roll 2d6 per the turn number. The boss monster has infinite mana to pay 
for tax effects (like Rhystic Study or Windborn Muse) that affect its attacks or casting of spells and its 
spells can always be cast, although they can be countered. 
The boss monster has a regular turn structure and its spells are cast during its first main phase as sorceries. 
Players can block for each other.


*** IMPORTANT: Install Poetry ***

I like to use the "official installer" instructions instead of pipx: 
https://python-poetry.org/docs/


*** IMPORTANT: Install dependencies ***

From repo root directory execute: 
poetry install


*** Run standalone scripts ***

From repo root directory execute: 
poetry run python3 ./raid_boss/main.py
poetry run python3 ./raid_boss/run.py
poetry run python3 ./raid_boss/kivytest.py


*** Run unit tests ***

From repo root directory execute:
poetry run python3 -m unittest discover tests


*** Format code with black ***

From repo root directory execute:
poetry run black .


*** TODOs ***
1. Maybe setup pre-commit hook for black?
    1. Execute: poetry add --dev pre-commit
    2. Create file in root directory: `.pre-commit-config.yaml`:
        ```
        repos:
        - repo: https://github.com/psf/black
          rev: 22.3.0  # Use the latest version of black
          hooks:
          - id: black
        ```
    3. Execute: poetry run pre-commit install
    4. Now black will automagically format the codebase before each commit.

2. Fix Kivy bugs in `main.py`. 

3. Real GUI features, more unit tests, build for mobile, add a license, and more!
