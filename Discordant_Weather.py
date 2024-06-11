# Weathers to implement, primary:
# Sunny, Rainy, Cloudy, Snowy
# Secondaries (TBD)
# Ripples, Semiquaver, Electric
from dataclasses import dataclass, field
from typing import Callable, Any
import random

@dataclass
class projection:
    initial_projection: float = 0
    initial_call: float = 0
    reoccurence_rate: float = 0
    reoccurence_call: float = field(init=False)

@dataclass
class Weather:
    name: str  # Name of the weather
    effect: str  # Effect description
    projection: projection  # Occurence Rate, Trigger Rate, Reoccurence Rate, Reoccurence Trigger Rate (If Apliccable)
    cold_call: int = 0
    hot_call: int = 0
    warm_call: int = 0

    def __repr__(self):
        if self.projection.reoccurence_rate < 0.3:
            size = 'low'
        elif 0.3 <= self.projection.reoccurence_rate < 0.7:
            size = 'moderate'
        else:
            size = 'high'
        return f'It is currently {self.name}. {self.effect} with a {size} chance of reoccurence.'

    def __post_init__(self):
        self.projection.reoccurence_call = int(self.projection.initial_call / 2)

    def effect_apply_stad(self):
        pass  # for stadium-specific effects

    def effect_apply_team(self):
        pass  # for team specific effects

    def effect_apply_char(self):
        pass  # for character specific effects

    def effect_apply_else(self):
        pass  # for else specific effects

    def weather_call(self):
        pass  # right this one is what's used to call the weathers particular applies

#  EXAMPLE WEATHER
class sunny(Weather):
    projection.initial_projection = 1  # The value (1-x) of the weather
    projection.initial_call = .5  # The value required to trigger it's effect

    def weather_call(self):  # The effect trigger
        if random.uniform(0,1) <= projection.initial_call:
            self.effect_apply_else()

    def effect_apply_else(self): # The effect instance
        if random.uniform(0, 1) <= self.projection.initial_call:
            print("> > The sun is shining.")
        else:
            print("> > A cloud passes.")


shining = sunny("Sunny","The sky is bright", projection(1, .5, 1))