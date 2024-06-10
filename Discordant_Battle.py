from Discordant_Character import Character, Stat
from Discordant_Teams import Teams
from Discordant_Stadium import Stadium
from Discordant_Modifier import injured, moribund, homesteader, tempo
from Discordant_Weather import shining
from dataclasses import dataclass, field
import random
from typing import Any
from pprint import pprint


@dataclass
class Battle:
    team1: Teams
    team2: Teams
    stadium: Stadium
    weather: object = field(default=None)
    rounds: int = field(default=0)
    harmonyattacklist: list[Character] = field(default_factory=list)
    hypeattacklist: list[Character] = field(default_factory=list)
    discordattacklist: list[Character] = field(default_factory=list)
# Key Character, Value Modifier.
# Append X Y where X is character, modifier is Y

    def declare_harmonyattacklist(self):
        for member in self.team1.members + self.team2.members:
            if member.attackresult[0] == 1:
                self.harmonyattacklist.append(member)

    def declare_hypeattacklist(self):
        for member in self.team1.members + self.team2.members:
            if member.attackresult[0] == 2:
                self.hypeattacklist.append(member)

    def declare_discordattacklist(self):
        for member in self.team1.members + self.team2.members:
            if member.attackresult[0] == 3:
                self.discordattacklist.append(member)

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
        print(self.weather)
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
        self.weather.weather_call()
        
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
        self.declare_harmonyattacklist()
        self.declare_hypeattacklist()
        self.declare_discordattacklist()
            
        team1_hypemembers = [member for member in self.team1.members if member in self.hypeattacklist]
        team2_hypemembers = [member for member in self.team2.members if member in self.hypeattacklist]

        character1hype_names = ', '.join([member.name for member in team1_hypemembers])
        character2hype_names = ', '.join([member.name for member in team2_hypemembers])
        print(character1hype_names, character2hype_names)
        
        while team1_hypemembers and team2_hypemembers:
            # print("While Performed")
            hypeclash1 = (team1_hypemembers[0].hype.total) + (random.randint(1, 6) + random.randint(1, 6))
            hypeclash2 = (team2_hypemembers[0].hype.total) + (random.randint(1, 6) + random.randint(1, 6))
            # print(team1_hypemembers, team2_hypemembers)

            if hypeclash1 > hypeclash2:
                print(f"{team2_hypemembers[0].name}'s hype ({hypeclash2}) is overpowered!")
                team2_hypemembers.remove(team2_hypemembers[0])

            elif hypeclash1 < hypeclash2:
                print(f"{team1_hypemembers[0].name}'s hype ({hypeclash1}) is overpowered!")
                team1_hypemembers.remove(team1_hypemembers[0])

            elif team1_hypemembers[0].hype.base > team2_hypemembers[0].hype.base:
                print(f"{team2_hypemembers[0].name}'s hype ({hypeclash2}) is overpowered!")
                team2_hypemembers.pop(0)

            elif team2_hypemembers[0].hype.base < team1_hypemembers[0].hype.base:
                print(f"{team1_hypemembers[0].name}'s hype ({hypeclash1}) is overpowered!")
                team1_hypemembers.pop(0)

            else:
                if random.randint(1, 2) == 1:
                    print(f"{team1_hypemembers[0].name}'s hype ({hypeclash1}) is overpowered!")
                    team1_hypemembers.pop(0)
                else:
                    print(f"{team2_hypemembers[0].name}'s hype ({hypeclash2}) is overpowered!")
                    team2_hypemembers.pop(0)
        if team1_hypemembers:
            for member in team1_hypemembers:
                print(f'> {member.name} is hyped!')
            self.team1.showrunner.extend(member for member in team1_hypemembers)
            self.team1.hypetracking()
            team1_hypemembers.clear()
            team2_hypemembers.clear()
            # print("Team 1 sublist is empty")
        elif team2_hypemembers:
            for member in team2_hypemembers:
                print(f'> {member.name} is hyped!')
            self.team2.showrunner.extend(member for member in team2_hypemembers)
            self.team2.hypetracking()
            team1_hypemembers.clear()
            team2_hypemembers.clear()
        else:
            print("The stadium is dim.")

            # print("Team 2 sublist is empty")

        team1_harmonymembers = [member for member in self.team1.members if member in self.harmonyattacklist]
        team2_harmonymembers = [member for member in self.team2.members if member in self.harmonyattacklist]

        while team1_harmonymembers and team2_harmonymembers:
            # print("While Performed")
            harmonyclash1 = (team1_harmonymembers[0].harmony.total) + (random.randint(1, 6) + random.randint(1, 6))
            harmonyclash2 = (team2_harmonymembers[0].harmony.total) + (random.randint(1, 6) + random.randint(1, 6))
            # print(team1_hypemembers, team2_hypemembers)

            if harmonyclash1 > harmonyclash2:
                print(f"{team2_harmonymembers[0].name}'s harmony is overpowered by {team1_harmonymembers[0].name}!")
                team2_harmonymembers.remove(team2_harmonymembers[0])

            elif harmonyclash1 < harmonyclash2:
                print(f"{team1_harmonymembers[0].name}'s harmony is overpowered by {team2_harmonymembers[0].name}!")
                team1_harmonymembers.remove(team1_harmonymembers[0])

            elif team1_harmonymembers[0].harmony.base > team2_harmonymembers[0].harmony.base:
                print(f"{team2_harmonymembers[0].name}'s harmony is overpowered by {team1_harmonymembers[0].name}!")
                team2_harmonymembers.pop(0)

            elif team2_harmonymembers[0].harmony.base < team1_harmonymembers[0].harmony.base:
                print(f"{team1_harmonymembers[0].name}'s harmony is overpowered by {team2_harmonymembers[0].name}!")
                team1_harmonymembers.pop(0)

            else:
                if random.randint(1, 2) == 1:
                    print(f"{team1_harmonymembers[0].name}'s harmony is overpowered by {team2_harmonymembers[0].name}!")
                    team1_harmonymembers.pop(0)
                else:
                    print(f"{team2_harmonymembers[0].name}'s harmony is overpowered by {team1_harmonymembers[0].name}!")
                    team2_harmonymembers.pop(0)

        if team1_harmonymembers:
            for member in team1_harmonymembers:
                print(f'> {member.name} resonates.')
                self.stadium.resonance1 += 1
            team1_harmonymembers.clear()
            team2_harmonymembers.clear()
                # print(self.stadium.resonance1)
            if self.stadium.resonance1 >= 10:
                print(f"> > > {self.team1.name} Is Resonating.")

        elif team2_harmonymembers:
            for member in team2_harmonymembers:
                print(f'> {member.name} resonates.')
                self.stadium.resonance2 += 1
            team1_harmonymembers.clear()
            team2_harmonymembers.clear()
                # print(self.stadium.resonance2)
            if self.stadium.resonance2 >= 10:
                print(f"> > > {self.team2.name} Is Resonating.")
        else:
            print("The stadium is dull.")

        team1_discordmembers = [member for member in self.team1.members if member in self.discordattacklist]
        team2_discordmembers = [member for member in self.team2.members if member in self.discordattacklist]

        while team1_discordmembers and team2_discordmembers:
            # print("While Performed")
            discordclash1 = (team1_discordmembers[0].discord.total) + (random.randint(1, 6) + random.randint(1, 6))
            discordclash2 = (team2_discordmembers[0].discord.total) + (random.randint(1, 6) + random.randint(1, 6))


            if discordclash1 > discordclash2:
                print(f"{team2_discordmembers[0].name}'s discord is overpowered by {team1_discordmembers[0].name}!")
                team2_discordmembers.remove(team2_discordmembers[0])

            elif discordclash1 < discordclash2:
                print(f"{team1_discordmembers[0].name}'s discord is overpowered by {team2_discordmembers[0].name}!")
                team1_discordmembers.remove(team1_discordmembers[0])

            elif team1_discordmembers[0].discord.base > team2_discordmembers[0].discord.base:
                print(f"{team2_discordmembers[0].name}'s discord is overpowered by {team1_discordmembers[0].name}!")
                team2_discordmembers.pop(0)

            elif team2_discordmembers[0].discord.base < team1_discordmembers[0].discord.base:
                print(f"{team1_discordmembers[0].name}'s discord is overpowered by {team2_discordmembers[0].name}!")
                team1_discordmembers.pop(0)

            else:
                if random.randint(1, 2) == 1:
                    print(f"{team1_discordmembers[0].name}'s discord is overpowered by {team2_discordmembers[0].name}!")
                    team1_discordmembers.pop(0)
                else:
                    print(f"{team2_discordmembers[0].name}'s discord is overpowered by {team1_discordmembers[0].name}!")
                    team2_discordmembers.pop(0)

        if team1_discordmembers:
            for member in team1_discordmembers:
                y = random.choice(self.team2.members)
                x = member
                y.health.current_stat += -(x.damage.total)
                print(f'> {y.name} is hit for {x.damage.total} by {x.name}! {y.name} has {y.health.current_stat} ticks left.')
            if y.health.current_stat <= round(y.health.base * .66):
                if injury_mod not in y.active_effects:
                    injury_mod.modifier_append(y)
                    print(y.name + " Is Injured!")
            if y.health.current_stat <= round(y.health.base * .33):
                if moribund_mod not in y.active_effects:
                    moribund_mod.modifier_append(y)
                    print(y.name + " Is Moribund!")
            team1_discordmembers.clear()
            team2_discordmembers.clear()
            # print("Team 1 sublist is empty")
        elif team2_discordmembers:
            for member in team2_discordmembers:
                y = random.choice(self.team1.members)
                x = member
                y.health.current_stat += -(x.damage.total)
                print(f'> {y.name} is hit for {x.damage.total} by {x.name}! {y.name} has {y.health.current_stat} ticks left.')
            if y.health.current_stat <= round(y.health.base * .66):
                if injury_mod not in y.active_effects:
                    injury_mod.modifier_append(y)
                    injury_mod.check_condition(y)
                    print(y.name + " Is Injured!")
            if y.health.current_stat <= round(y.health.base * .33):
                if moribund_mod not in y.active_effects:
                    moribund_mod.modifier_append(y)
                    moribund_mod.check_condition(y)
                    print(y.name + " Is Moribund!")
            team1_discordmembers.clear()
            team2_discordmembers.clear()
        else:
            print("The stadium is quiet.")


Turmoilrig = Stadium("Turmoilrig")
The_Great_Tree = Stadium("The Great Tree")

Philosophers = Teams("Philosophers")
Philosophers.set_stadium(Turmoilrig)
print(Philosophers.stadium)

Plato = Character(Stat(5), Stat(5), Stat(5), Stat(12, 12), Stat(2), name="Plato")
Socrates = Character(Stat(5), Stat(5), Stat(5), Stat(12, 12), Stat(2), name="Socrates")
Aristotle = Character(Stat(5), Stat(5), Stat(5), Stat(12, 12), Stat(2), name="Aristotle")

Keeblers = Teams("Keeblers")
Keeblers.set_stadium(The_Great_Tree)

Snap = Character(Stat(5), Stat(5), Stat(5), Stat(12, 12), Stat(2), name="Snap")
Crackle = Character(Stat(5), Stat(5), Stat(5), Stat(12, 12), Stat(2), name="Crackle")
Pop = Character(Stat(5), Stat(5), Stat(5), Stat(12, 12), Stat(2), name="Pop")

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


dprint(Plato)
battlerun = Battle(Philosophers, Keeblers, Turmoilrig, shining)

injury_mod = injured(0, name="Injured", character=Character)
moribund_mod = moribund(-3, name="Moribund", character=Character)

x = tempo(3,"Tempo", "Plato")

x.modifier_append(Plato)

y = homesteader(5, "Homesteader", character="Plato", battle=battlerun)
y.modifier_append(Socrates)

battlerun.run()
print(Socrates.inactive_effects)
print(Socrates.danger_value)