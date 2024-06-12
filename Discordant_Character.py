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
class MiniStat:
    mode: int = 0
    timbre: int = 0
    reach: int = 0
    threading: int = 0
    mixing: int = 0


@dataclass
class Interviews:
    team: Any = field(default=None, repr=False)
    name: str = field(default="Null")
    danger: int = 0
    genre: str = field(default="All")
    vibe: str = field(default="All")


@dataclass
class Character:
    harmony: Stat
    hype: Stat
    discord: Stat
    health: Stat
    damage: Stat
    interviews: Interviews = field(default_factory=Interviews)
    inactive_effects: list = field(default_factory=list)
    active_effects: list = field(default_factory=list)
    status: list = field(default_factory=list)
    substat: MiniStat = field(default_factory=MiniStat)
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
        self.interviews.danger = self.danger_value
        # Substat Zone - Mode, Timbre, Reach, Thread, Mixing
        self.substat.mode = round(.5 * self.harmony.total) + round(.5 * self.hype.total)
        self.substat.timbre = round(.5 * self.harmony.total) + round(.5 * self.discord.total)
        self.substat.reach = round(.5 * self.hype.total) + round(.5 * self.discord.total)
        self.substat.threading = round(.33 * self.harmony.total) + round(.66 * self.discord.total)
        self.substat.mixing = round(.33 * self.harmony.total) + round(.66 * self.hype.total)

    def CharacterModifier_apply(self, CharacterModifier):
        self.inactive_effects.append(CharacterModifier)

    def harmonyattack(self):
        self.attackresult = [1]

    def hypeattack(self):
        self.attackresult = [2]

    def discordattack(self):
        self.attackresult = [3]


firstnamelist = ["Konane", "Puff", "Slap", "Dawn", "Melvin", "Blorch", "Cache", "Jay", "Iori", "Puffbird", "Tanagar", "Petrel", "Hornbill", "Macgellan", "Salvatore", "Margarita", "Kai", "Kaylani", "Christof", "Augustine", "Lavender", "Marx-Anthony", "Eizabeth", "Macgillicutty", "Estrolfo", "Evangeline", "Remy", "Sauce", "Quail", "Lingdenstein", "Kazani", "Sasha", "Murky", "Karl", "Horrible", "Garfield", "Andrew", "Roxxas", "Scalar", "Henry", "Falco", "Trilby", "Mark", "Aro", "Ari", "Kevin", "Kelvin", "Toby", "CGO", "Elm", "Nail", "Scabbard", "Pyxis", "Pix", "Mel", "Foil"]
lastnamelist = ["Boss", "Bass", "DeWick", "Kerman", "Bylaw", "Blorch", "Diggins", "Boobie", "Parade", "Ibis", "Sunbird", "Gull", "Fableman", "Makoa", "Manu", "Anela", "Mahi'ai", "Alana", "Boyko", "Rose", "Kazani", "Dunk", "Ulliuan", "Mulligan", "Eroka", "Rupert", "Garfield", "Telli", "Smith", "Kells", "Selli", "Cone", "Mult", "Pothos", "Mason", "Wood", "Glover", "Ball", "Bently", "Trumpet", "Galapagos", "Tree", "Markul", "Egada", "Roland", "Crueller", "Elliot"]
genres = ["Crime", "Blorch", "Brakecore", "Breakcore", "Melodic EDM", "EDM", "Dreamcore", "Weirdcore", "Futurebass", "Hyperpop", "Emo", "Death", "Death Metal", "Qwopcore", "Impressionism", "Lo-Fi", "Pop Rock", "Punk", "Classical", "Low-Classical", "High-Classical", "Key Jingling", "Crispwave", "Hivemind", "Spike Trap", "Mudglitch", "Indie", "Orange","OwOCore", "Assassin"]
vibes = ["Muddy", "Friend-Shaped", "Blorch", "Instant", "Putrid", "Slightly Sticky", "Indie", "Rock", "Stone", "Wilson", "Lederhosen", "Creamy", "Crime", "Gutter", "Rat", "Redeemed", "High", "Quaint", "Dainty", "Mellow", "Refined", "Wholistic", "Explosive", "Stabbing", "Backflip", "Frontflip", "Hell"]


def Character_Create():

    def marks():
        y = int(max(0, (random.randint(0, 6)-random.randint(0, 4))))
        return y

    Harmony = marks()
    Hype = marks()
    Discord = marks()
    Health = 12
    Damage = 2
    InterviewName = random.choice(firstnamelist) + ' ' + random.choice(lastnamelist)
    InterviewTeam = None
    InterviewGenre = random.choice(genres)
    InterviewVibes = random.choice(vibes)
    x = Character(Stat(Harmony), Stat(Hype), Stat(Discord), Stat(Health, Health), Stat(Damage), Interviews(name=InterviewName, genre=InterviewGenre, vibe=InterviewVibes))
    return x


print(Character_Create())
print(len(firstnamelist))
print(len(lastnamelist))
print(len(genres))
print(len(vibes))