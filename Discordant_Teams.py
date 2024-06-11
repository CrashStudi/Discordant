from Discordant_Character import Character
from Discordant_Stadium import Stadium
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Teams:
    name: str
    stadium: Stadium = field(default_factory=Stadium)
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
        member.interviews.team = (self)
        # print(f"Adding member: {member.name}")

    def set_stadium(self, stadium):
        self.stadium = stadium

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