# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Driver:
    first_name: Optional[str] = field(default=None)
    last_name: Optional[str] = field(default=None)
    team: Optional[str] = field(default=None)
    country: Optional[str] = field(default=None)
    podiums: Optional[str] = field(default=None)
    points: Optional[str] = field(default=None)
    grand_prix_entered: Optional[str] = field(default=None)
    world_championships: Optional[str] = field(default=None)
    highest_race_finish: Optional[str] = field(default=None)
    highest_grid_position: Optional[str] = field(default=None)
    date_of_birth: Optional[str] = field(default=None)
    place_of_birth: Optional[str] = field(default=None)

@dataclass
class Team:
    full_team_name: Optional[str] = field(default=None)
    drivers : Optional[list[str]] = field(default_factory=list)
    base: Optional[str] = field(default=None)
    team_chief: Optional[str] = field(default=None)
    technical_chief: Optional[str] = field(default=None)
    chassis: Optional[str] = field(default=None)
    power_unit: Optional[str] = field(default=None)
    first_team_entry: Optional[str] = field(default=None)
    world_championships: Optional[str] = field(default=None)
    highest_race_finish: Optional[str] = field(default=None)
    pole_positions: Optional[str] = field(default=None)
    fastest_laps: Optional[str] = field(default=None)

@dataclass
class ResultDriver : 
    pos : Optional[str] = field(default=None)
    driver : Optional[str] = field(default=None)
    nationality: Optional[str] = field(default=None)
    car : Optional[str] = field(default=None)
    pts : Optional[str] = field(default=None)

@dataclass
class ResultDriverPersonalInfo : 
    driver : Optional[str] = field(default=None)
    grand_prix : Optional[str] = field(default=None)
    date : Optional[str] = field(default=None)
    car : Optional[str] = field(default=None)
    race_position : Optional[str] = field(default=None)
    pts : Optional[str] = field(default=None)

@dataclass
class ResultTeam : 
    year : Optional[str] = field(default=None)
    pos : Optional[str] = field(default=None)
    team : Optional[str] = field(default=None)
    pts : Optional[str] = field(default=None)

@dataclass
class ResultTeamDetailedInfo :
    year : Optional[str] = field(default=None)
    team : Optional[str] = field(default=None)
    grand_prix : Optional[str] = field(default=None)
    date : Optional[str] = field(default=None)
    pts : Optional[str] = field(default=None)
