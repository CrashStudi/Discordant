import yaml
from typing import ClassVar
import random
from dataclasses import dataclass



@dataclass
class Hamburger(yaml.YAMLObject):
    bottombun: str | None = None
    toppings: tuple[str, str, str] | None = None
    patty: str | None = None
    sauces: str | None = None
    topbun: str | None = None
    yaml_tag: ClassVar[str] = "!Hamburger"

    def add_burger(self, bottombun=None, toppings: str | None=None , patty=None , sauces=None, topbun=None):
        if self.bottombun is not None:
            self.bottombun = bottombun
        if self.toppings is not None:
            self.toppings = toppings
        if self.patty is not None:
            self.patty = patty
        if self.sauces is not None:
            self.sauces = sauces
        if self.topbun is not None:
            self.topbun = topbun

    def make_burger(self) -> object:
        bun1: str = random.choice(["Brioche", "Regular", "Lettuce"])
        topping1: str = random.choice(["Lettuce", "Tomato", "Extra_Patty", "Cheese", "None"])
        topping2: str = random.choice(["Lettuce", "Tomato", "Extra_Patty", "Cheese", "None"])
        topping3: str = random.choice(["Lettuce", "Tomato", "Extra_Patty", "Cheese", "None"])
        patty1: str = random.choice(["Lamb", "Beef", "Ham", "Impossible"])
        if topping1 == "Extra_Patty":
            topping1 = patty1
        if topping2 == "Extra_Patty":
            topping2 = patty1
        if topping3 == "Extra_Patty":
            topping3 = patty1
        sauces1: str = random.choice(["Ketchup", "Mustard", "Mayo", "None", "Extra"])
        if sauces1 == "Extra":
            sauces1 = random.choice(["Ketchup", "Mustard", "Mayo"]) + ", " + random.choice(["Ketchup", "Mustard", "Mayo"])
        bun2 = bun1
        Burger_Machine = Hamburger(bun1, (topping1, topping2, topping3), patty1, sauces1, bun2)
        return Burger_Machine

burg1 = Hamburger()
burg_item = burg1.make_burger()
burg_menu = yaml.dump(burg_item)
with open('burger_item.yaml', 'w') as file:
    file.write(burg_menu)
burg_choice = yaml.load(file, Loader=yaml.Loader)
print(burg_choice)