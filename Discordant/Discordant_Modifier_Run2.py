from Discordant_Character import Character, Stat, Interviews, MiniStat
from Discordant_Teams import Teams
from Discordant_Stadium import Stadium
from typing import Any


philosophers = Teams("Philosophers")
philosophers.set_stadium(Stadium("Turmoilrig"))
print(philosophers.stadium)

plato = Character(Stat(5), Stat(5), Stat(5), Stat(12, 12), Stat(2), Interviews(name="Plato"))
socrates = Character(Stat(5), Stat(5), Stat(5), Stat(12, 12), Stat(2), Interviews(name="Socrates"))
aristotle = Character(Stat(5), Stat(5), Stat(5), Stat(12, 12), Stat(2), Interviews(name="Aristotle"))


class Modifier:
    def __init__(self, name="None"):
        self.name = name
        self.characterapplied = Character

    def __repr__(self):
        return f"{self.name} is present."

    def apply_to_char(self, Character):
        self.characterapplied = Character
        Character.inactive_effects += [self]

    def statecheck(self):
        print("State-Checking")

    def statetrigger(self):
        print("State-Triggering")

    def stateeffect(self):
        print("State-Effect")


class first_aid(Modifier):
    def statecheck(self):
        if self.characterapplied:
            if self.characterapplied.health.current_stat <= (self.characterapplied.health.base):
                self.statetrigger()

    def statetrigger(self):
        self.characterapplied.active_effects.append(self)
        self.characterapplied.inactive_effects.remove(self)
        self.stateeffect()

    def stateeffect(self):
        self.characterapplied.health.current_stat += 3


class second_aid(Modifier):
    def statecheck(self):
        if self.characterapplied:
            for character in self.characterapplied.interviews.team.members:
                if character.health.current_stat < character.health.base:
                    self.statetrigger(character)

    def statetrigger(self, character):
        if self in character.inactive_effects:
            character.inactive_effects.remove(self)
            character.active_effects.append(self)
        self.stateeffect(character)

    def stateeffect(self, character):
        character.health.current_stat += 3
        
class first_beat(Modifier):
    def statecheck(self):
        if self.characterapplied:
            if self.characterapplied.harmony.current_stat <= self.characterapplied.harmony.total: 
                self.statetriggerharmony()
            if self.characterapplied.discord.current_stat <= self.characterapplied.discord.total:
                self.statetriggerdiscord()
            if self.characterapplied.hype.current_stat <= self.characterapplied.hype.total:
                self.statetriggerhype()

    def statetriggerharmony(self):
        self.stateeffectharmony()

    def stateeffectharmony(self):
        print(f"Player {self.characterapplied.interviews.name} is under harmony-cap.")

    def statetriggerdiscord(self):
        self.stateeffectdiscord()

    def stateeffectdiscord(self):
        print(f"Player {self.characterapplied.interviews.name} is under discord-cap.")

    def statetriggerhype(self):
        self.stateeffecthype()

    def stateeffecthype(self):
        print(f"Player {self.characterapplied.interviews.name} is under hype-cap.")

second_aid2 = second_aid("second_aid")
first_beat1 = first_beat("second_aid")

philosophers.set_members(plato)
philosophers.set_members(socrates)
philosophers.set_members(aristotle)
first_beat1.apply_to_char(plato)

plato.harmony.current_stat -= 4
print(plato.harmony.current_stat)
print(plato.hype.current_stat)

for x in philosophers.members:
    print(x.health.current_stat)
    print(f"inactive effects for " + x.interviews.name, x.inactive_effects)
    print(f"active effects for " + x.interviews.name, x.active_effects)

for x in philosophers.members:
    if x.inactive_effects:
        for y in x.inactive_effects:
            y.statecheck()

for x in philosophers.members:
    print(x.health.current_stat)
    print(f"inactive effects for " + x.interviews.name, x.inactive_effects)
    print(f"active effects for " + x.interviews.name, x.active_effects)