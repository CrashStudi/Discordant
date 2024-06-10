from typing import Any
from dataclasses import field


class Modifier:
    def __init__(self, danger, name, *args, **kwargs):
        self.danger = danger
        self.name = name
        for arg in args:
            setattr(self, arg, arg)
        for key, value in kwargs.items():
            setattr(self, key, value)
            # print(key, value)

    def __repr__(self):
        return (f"{self.name} is currently in use.")

    def modifier_append(self, character):
        character.inactive_effects.append(self)

    def check_condition(self, *args, **kwargs):
        pass

    def apply_effect(self, *args, **kwargs):
        pass


class homesteader(Modifier):
    def check_condition(self, character):
        print(self.battle.stadium)
        print(character.team.stadium)
        if self.battle.stadium == character.team.stadium:
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
        character.discord.mod_mod += -1
        character.inactive_effects.remove(self)
        character.active_effects.append(self)


class moribund(Modifier):
    def check_condition(self, character):
        if self not in character.active_effects:
            self.apply_effect(character)
        
    def apply_effect(self, character):
        character.harmony.mod_mod += -3
        character.hype.mod_mod += -3
        character.discord.mod_mod += -3
        character.inactive_effects.remove(self)
        character.active_effects.append(self)


class tempo(Modifier):
    def check_condition(self, character):
        if character.health.current_stat <= character.health.base / 2:
            self.apply_effect(character)

    def apply_effect(self, character):
        character.health.current_stat += character.harmony.base