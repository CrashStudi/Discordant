from dataclasses import dataclass, field
from typing import Any
import random

@dataclass
class Stat:
    base: int = 0
    current_stat: int = base
    hype_mod: int = 0
    mod_mod: int = 0
    item_mod: int = 0
    external_mod: int = 0

    @property
    def total(self):
        return self.base + self.hype_mod + self.mod_mod + self.item_mod + self.external_mod


@dataclass
class Character:
    harmony: Stat
    hype: Stat
    discord: Stat
    health: Stat
    damage: Stat
    danger: int = 0
    team: Any = field(default=None)
    name: str = field(default="Null")
    inactive_effects: list = field(default_factory=list)
    active_effects: list = field(default_factory=list)
    status: list = field(default_factory=list)
    attackresult: list = field(default_factory=list)
    

    def tribulate_percents(self):
        stattotal = (self.hype.base + self.harmony.base + self.discord.base)
        harmony_percent = float(self.harmony.base / stattotal)
        hype_percent = float(self.hype.base / stattotal)
        discord_percent = float(self.discord.base / stattotal)
        Statpercentages = (harmony_percent + hype_percent + discord_percent)
        course_of_action = random.uniform(0, Statpercentages)
        if course_of_action >= 0 and course_of_action <= harmony_percent:
            self.harmonyattack()
        elif course_of_action >= harmony_percent and course_of_action \
                <= (harmony_percent + hype_percent):
            self.hypeattack()
        elif course_of_action >= harmony_percent + hype_percent \
                and course_of_action <= Statpercentages:
            self.discordattack()
        # print(stattotal, harmony_percent, discord_percent)

    @property
    def danger_value(self):
        danger = self.harmony.total + self.hype.total + self.discord.total
        for mod in self.inactive_effects + self.active_effects + self.status:
            danger += mod.danger
        return danger
    
    def __post_init__(self):
        self.danger_value

    def CharacterModifier_apply(self, CharacterModifier):
        self.inactive_effects.append(CharacterModifier)

    def harmonyattack(self):
        self.attackresult = [1]

    def hypeattack(self):
        self.attackresult = [2]

    def discordattack(self):
        self.attackresult = [3]
        # FightInstance.discordattacklist.append(self)
