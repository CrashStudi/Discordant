import random
from dataclasses import dataclass, field
from typing import Any
from pprint import pprint


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
    team: Any = field(default=None)
    name: str = field(default="Null")
    inactive_effects: Any = field(default_factory=list)
    active_effects: Any = field(default_factory=list)
    status: Any = field(default_factory=list)

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

    def CharacterModifier_apply(self, CharacterModifier):
        self.inactive_effects.append(CharacterModifier)

    def harmonyattack(self):
        battlerun.harmonyattacklist.append(self)

    def hypeattack(self):
        battlerun.hypeattacklist.append(self)

    def discordattack(self):
        battlerun.discordattacklist.append(self)
        # FightInstance.discordattacklist.append(self)


@dataclass
class Stadium:
    name: str = field(default='Habitat')
    effects: Any = field(default=None)
    resonance1: Any = field(default=0)
    resonance2: Any = field(default=0)


@dataclass
class Teams:
    name: str
    stadium: list = field(default_factory=list)
    effects: Any = None
    hypebonus: int = 0
    wins: int = 0
    losses: int = 0
    ties: int = 0
    members: list = field(default_factory=list)
    showrunner: list = field(default_factory=list)

    def set_win(self, new_wins):
        self.wins = new_wins

    def set_losses(self, new_losses):
        self.losses = new_losses

    def set_ties(self, new_ties):
        self.ties = new_ties

    def get_members(self):
        return self.members

    def set_members(self, member: Character):
        self.members.append(member)
        member.team = (self)
        # print(f"Adding member: {member.name}")

    def set_stadium(self, stadium: Stadium):
        self.stadium.append(stadium)

    def hypetracking(self):
        self.hypebonus = max(member.hype.base for member in self.showrunner)
        # print("Hype being tracked: ", {self.hypebonus})
        for member in self.members:
            if member not in self.showrunner:
                member.harmony.hype_mod += self.hypebonus
                member.hype.hype_mod += self.hypebonus
                member.discord.hype_mod += self.hypebonus
                member.harmony.total
                member.hype.total
                member.discord.total
        self.showrunner.clear()


# CharacterModifierS
# Should apply to character, not the other way around.
# One function to check for conditions achieved, One to apply effects.
# Requires a danger value.
# Example: Tempo. Grants the character their harmony in health if they dip below half.

class Modifier:
    def __init__(self, danger, *args, **kwargs):
        self.danger = danger
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return (f"{self.kwargs} is currently in use.")

    def modifier_append(self, character):
        character.inactive_effects.append(self)

    def check_condition(self, *args, **kwargs):
        pass

    def apply_effect(self, *args, **kwargs):
        pass


class tempo(Modifier):
    def check_condition(self, character):
        if character.health.current_stat <= character.health.base / 2:
            self.apply_effect(character)

    def apply_effect(self, character):
        character.health.current_stat += character.harmony.base


@dataclass
class Battle:
    team1: Teams
    team2: Teams
    stadium: Stadium
    rounds: int = field(default=0)
    harmonyattacklist: list[Character] = field(default_factory=list)
    hypeattacklist: list[Character] = field(default_factory=list)
    discordattacklist: list[Character] = field(default_factory=list)
# Key Character, Value Modifier.
# Append X Y where X is character, modifier is Y

    def effect_clear(self):
        for member in self.team1.members:
            member.harmony.hype_mod = 0
            member.hype.hype_mod = 0
            member.discord.hype_mod = 0

        for member in self.team2.members:
            member.harmony.hype_mod = 0
            member.hype.hype_mod = 0
            member.discord.hype_mod = 0

    def run(self):
        while self.stadium.resonance1 < 10 and self.stadium.resonance2 < 10:
            print(self.stadium.resonance1, self.stadium.resonance2)
            self.round()

    def round(self):
        # Characters Tribulate. Tribulation chooses their action, and places them in that respective action list.
        # Characters in the action lists have their teams taken and are put into a list corresponding to those teams.
        # Check to see if either list is empty. If (list1) is empty, the action continues for members of (list2.)
        # If lists are not empty, Characters add their actions respective attribute to a roll of 2d6.
        # Loser is removed from their respective list. Repeat 2.
        self.harmonyattacklist.clear()
        self.hypeattacklist.clear()
        self.discordattacklist.clear()
        self.effect_clear()
        
        for member in self.team1.members:
            for modifier in member.inactive_effects:
                modifier.check_condition(member)
        # for member in self.team1.members:
            # self.team1.members.inactive_effects.check_conditions(self)

        for member in self.team1.members:
            member.tribulate_percents()
            # member.inactive_effects.CharacterModifiers.check_conditions()

        for member in self.team2.members:
            member.tribulate_percents()
            # member.inactive_effects.CharacterModifiers.check_conditions()

        team1_hypemembers = [member for member in self.hypeattacklist if member in self.team1.members]
        team2_hypemembers = [member for member in self.hypeattacklist if member in self.team2.members]

        while team1_hypemembers and team2_hypemembers:
            # print("While Performed")
            hypeclash1 = (team1_hypemembers[0].hype.total) + (random.randint(1, 6) + random.randint(1, 6))
            hypeclash2 = (team2_hypemembers[0].hype.total) + (random.randint(1, 6) + random.randint(1, 6))
            # print(team1_hypemembers, team2_hypemembers)

            if hypeclash1 > hypeclash2:
                team2_hypemembers.remove(team2_hypemembers[0])

            elif hypeclash1 < hypeclash2:
                team1_hypemembers.remove(team1_hypemembers[0])

            elif team1_hypemembers[0].hype.base > team2_hypemembers[0].hype.base:
                team2_hypemembers.pop(0)

            elif team2_hypemembers[0].hype.base < team1_hypemembers[0].hype.base:
                team1_hypemembers.pop(0)

            else:
                if random.randint(1, 2) == 1:
                    team1_hypemembers.pop(0)
                else:
                    team2_hypemembers.pop(0)
        if team1_hypemembers:
            self.team1.showrunner.extend(member for member in team1_hypemembers)
            self.team1.hypetracking()
            team1_hypemembers.clear()
            team2_hypemembers.clear()
            # print("Team 1 sublist is empty")
        elif team2_hypemembers:
            self.team2.showrunner.extend(member for member in team2_hypemembers)
            self.team2.hypetracking()
            team1_hypemembers.clear()
            team2_hypemembers.clear()

            # print("Team 2 sublist is empty")

        team1_harmonymembers = [member for member in self.harmonyattacklist if member in self.team1.members]
        team2_harmonymembers = [member for member in self.harmonyattacklist if member in self.team2.members]

        while team1_harmonymembers and team2_harmonymembers:
            # print("While Performed")
            harmonyclash1 = (team1_harmonymembers[0].harmony.total) + (random.randint(1, 6) + random.randint(1, 6))
            harmonyclash2 = (team2_harmonymembers[0].harmony.total) + (random.randint(1, 6) + random.randint(1, 6))
            # print(team1_hypemembers, team2_hypemembers)

            if harmonyclash1 > harmonyclash2:
                team2_harmonymembers.remove(team2_harmonymembers[0])

            elif harmonyclash1 < harmonyclash2:
                team1_harmonymembers.remove(team1_harmonymembers[0])

            elif team1_harmonymembers[0].harmony.base > team2_harmonymembers[0].harmony.base:
                team2_harmonymembers.pop(0)

            elif team2_harmonymembers[0].harmony.base < team1_harmonymembers[0].harmony.base:
                team1_harmonymembers.pop(0)

            else:
                if random.randint(1, 2) == 1:
                    team1_harmonymembers.pop(0)
                else:
                    team2_harmonymembers.pop(0)

        if team1_harmonymembers:
            self.stadium.resonance1 += 1
            team1_harmonymembers.clear()
            team2_harmonymembers.clear()
            # print(self.stadium.resonance1)
            if self.stadium.resonance1 >= 10:
                print(f"{self.team1.name} Is Resonating.")

        elif team2_harmonymembers:
            self.stadium.resonance2 += 1
            team1_harmonymembers.clear()
            team2_harmonymembers.clear()
            # print(self.stadium.resonance2)
            if self.stadium.resonance2 >= 10:
                print(f"{self.team2.name} Is Resonating.")

        team1_discordmembers = [member for member in self.discordattacklist if member in self.team1.members]
        team2_discordmembers = [member for member in self.discordattacklist if member in self.team2.members]

        while team1_discordmembers and team2_discordmembers:
            # print("While Performed")
            discordclash1 = (team1_discordmembers[0].discord.total) + (random.randint(1, 6) + random.randint(1, 6))
            discordclash2 = (team2_discordmembers[0].discord.total) + (random.randint(1, 6) + random.randint(1, 6))
            # print(team1_hypemembers, team2_hypemembers)

            if discordclash1 > discordclash2:
                team2_discordmembers.remove(team2_discordmembers[0])

            elif discordclash1 < discordclash2:
                team1_discordmembers.remove(team1_discordmembers[0])

            elif team1_discordmembers[0].discord.base > team2_discordmembers[0].discord.base:
                team2_discordmembers.pop(0)

            elif team2_discordmembers[0].discord.base < team1_discordmembers[0].discord.base:
                team1_discordmembers.pop(0)

            else:
                if random.randint(1, 2) == 1:
                    team1_discordmembers.pop(0)
                else:
                    team2_discordmembers.pop(0)

        if team1_discordmembers:
            for member in self.team2.members:
                x = member
            y = random.choice(self.team2.members)
            for member in team1_discordmembers:
                x = member
            y.health.current_stat += -(x.damage.total)
            print(f'{y.name} is hit for {x.damage.total}! {y.name} has {y.health.current_stat} ticks left.')
            if y.health.current_stat <= round(y.health.base * .66):
                if injury_mod not in y.active_effects:
                    injury_mod.character=y
                    injury_mod.modifier_append(y)
                    injury_mod.check_condition(y)
                    print(y.name + " Is Injured!")
            if y.health.current_stat <= round(y.health.base * .33):
                if moribund_mod not in y.active_effects:
                    moribund_mod.character=y
                    moribund_mod.modifier_append(y)
                    moribund_mod.check_condition(y)
                    print(y.name + " Is Moribund!")
            team1_discordmembers.clear()
            team2_discordmembers.clear()
            # print("Team 1 sublist is empty")
        elif team2_discordmembers:
            for member in self.team1.members:
                x = member
            y = random.choice(self.team1.members)
            for member in team2_discordmembers:
                x = member
            y.health.current_stat += -(x.damage.total)
            print(f'{y.name} is hit for {x.damage.total}! {y.name} has {y.health.current_stat} ticks left.')
            if y.health.current_stat <= round(y.health.base * .66):
                if injury_mod not in y.active_effects:
                    injury_mod.character=y
                    injury_mod.modifier_append(y)
                    injury_mod.check_condition(y)
                    print(y.name + " Is Injured!")
                    print(y.active_effects)
            if y.health.current_stat <= round(y.health.base * .33):
                if moribund_mod not in y.active_effects:
                    moribund_mod.character=y
                    moribund_mod.modifier_append(y)
                    moribund_mod.check_condition(y)
                    print(y.name + " Is Moribund!")
                    print(y.active_effects)
            team1_discordmembers.clear()
            team2_discordmembers.clear()


Turmoilrig = Stadium("Turmoilrig")
The_Great_Tree = Stadium("The Great Tree")

Philosophers = Teams("Philosophers")
Philosophers.set_stadium(Turmoilrig)
print(Philosophers.stadium)

Plato = Character(Stat(500), Stat(5), Stat(5), Stat(12, 12), Stat(2), name="Plato")
Socrates = Character(Stat(5), Stat(500), Stat(5), Stat(12, 12), Stat(2), name="Socrates")
Aristotle = Character(Stat(5), Stat(5), Stat(500), Stat(12, 12), Stat(2), name="Aristotle")

Keeblers = Teams("Keeblers")
Keeblers.set_stadium(The_Great_Tree)

Snap = Character(Stat(500), Stat(5), Stat(5), Stat(12, 12), Stat(2), name="Snap")
Crackle = Character(Stat(5), Stat(500), Stat(5), Stat(12, 12), Stat(2), name="Crackle")
Pop = Character(Stat(5), Stat(5), Stat(500), Stat(12, 12), Stat(2), name="Pop")

Philosophers.set_members(Plato)
Philosophers.set_members(Socrates)
Philosophers.set_members(Aristotle)
Keeblers.set_members(Snap)
Keeblers.set_members(Crackle)
Keeblers.set_members(Pop)


def dprint(C, Checkfull=None):
    if Checkfull is None:
        pprint((C.harmony, C.hype, C.discord, C.health, C.damage, C.name, C.team.name, C.inactive_effects))
    else:
        print(C.harmony.total, C.hype.total, C.discord.total, C.health.total, C.damage.total, C.name)


# dprint(Plato)
battlerun = Battle(Philosophers, Keeblers, Turmoilrig)

class homesteader(Modifier):
    def check_condition(self, character, battle=None):
        if battle is not None and battle.stadium == character.team.stadium:
            if self not in character.active_effects:
                self.apply_effect(character)

    def apply_effect(self, character):
        character.hype.mod_mod += 3
        character.inactive_effects.remove(self)
        character.active_effects.append(self)
        
class injured(Modifier):
    def check_condition(self, character):
        if self not in character.active_effects:
            self.apply_effect(character)
        
    def apply_effect(self, character):
        character.harmony.mod_mod += -1
        character.hype.mod_mod += -1
        character.hype.mod_mod += -1
        character.inactive_effects.remove(self)
        character.active_effects.append(self)
        
class moribund(Modifier):
    def check_condition(self, character):
        if self not in character.active_effects:
            self.apply_effect(character)
        
    def apply_effect(self, character):
        character.harmony.mod_mod += -3
        character.hype.mod_mod += -3
        character.hype.mod_mod += -3
        character.inactive_effects.remove(self)
        character.active_effects.append(self)

injury_mod = injured(0, name = "Injured", character = Character)
moribund_mod = moribund(-3, name = "Moribund", character = Character)

x = tempo(3, name="Tempo", character="Plato")
x.modifier_append(Plato)

y = homesteader(5, name="Homesteader", character="Socrates", battle=battlerun)
y.modifier_append(Socrates)


battlerun.run()
