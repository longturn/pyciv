import re
from dataclasses import dataclass, field
from typing import List, Union

from typeguard import typechecked

from freeciv.effects import Requirement

from .secfile.loader import section


@section("datafile")
@typechecked
@dataclass
class DataFileHeader:
    description: str
    options: str
    format_version: int  # 10 or 20


@section("about")
@typechecked
@dataclass
class AboutData:
    name: str
    version: int = -1
    summary: str = ""
    description: str = ""
    capabilities: str = ""  # 3.0


@section("options")
@typechecked
@dataclass
class OptionsData:
    global_init_techs: str
    global_init_buildings: str


@section("tileset")
@typechecked
@dataclass
class TilesetData:
    preferred: str = ""


@section("soundset")
@typechecked
@dataclass
class SoundsetData:
    preferred: str = ""


@section("musicset")
@typechecked
@dataclass
class MusicsetData:
    preferred: str = ""


@section("civstyle")
@typechecked
@dataclass
class CivStyleData:
    granary_food_ini: int
    granary_food_inc: int
    min_city_center_food: int
    min_city_center_shield: int
    min_city_center_trade: int
    init_city_radius_sq: int
    init_vis_radius_sq: int
    upgrade_veteran_loss: int
    autoupgrade_veteran_loss: int
    pillage_select: bool
    tech_steal_allow_holes: bool
    tech_trade_allow_holes: bool
    tech_trade_loss_allow_holes: bool
    tech_parasite_allow_holes: bool
    tech_loss_allow_holes: bool
    initial_diplomatic_state: str
    civil_war_enabled: bool
    civil_war_bonus_celebrating: int
    civil_war_bonus_unhappy: int
    gameloss_style: str
    paradrop_to_transport: bool
    gold_upkeep_style: str
    output_granularity: int


@section("illness")
@typechecked
@dataclass
class IllnessData:
    illness_on: bool
    illness_base_factor: int
    illness_min_size: int
    illness_trade_infection: int
    illness_pollution_factor: int


@section("incite_cost")
@typechecked
@dataclass
class InciteCostData:
    improvement_factor: int
    unit_factor: int
    total_factor: int


@section("combat_rules")
@typechecked
@dataclass
class CombatRulesData:
    tired_attack: bool
    only_killing_makes_veteran: bool
    nuke_pop_loss_pct: int
    nuke_defender_survival_chance_pct: int


@section("auto_attack")
@typechecked
@dataclass
class AutoAttackData:
    attack_actions: list[str]
    if_attacker: list[Requirement] = field(default_factory=list)


@section("actions")
@typechecked
@dataclass
class ActionsData:
    force_trade_route: bool
    force_capture_units: bool
    force_bombard: bool
    force_explode_nuclear: bool
    poison_empties_food_stock: bool
    steal_maps_reveals_all_cities: bool
    help_wonder_max_range: int
    recycle_unit_max_range: int
    bombard_max_range: int
    bombard_2_max_range: int
    bombard_3_max_range: int
    explode_nuclear_max_range: int
    nuke_city_max_range: int
    nuke_units_max_range: int
    ui_name_bribe_unit: str
    ui_name_sabotage_city: str
    ui_name_incite_city: str
    ui_name_establish_embassy_stay: str
    ui_name_steal_tech: str
    ui_name_investigate_city_spend_unit: str
    ui_name_establish_trade_route: str
    ui_name_enter_marketplace: str
    ui_name_help_wonder: str
    ui_name_recycle_unit: str
    ui_name_disband_unit: str
    ui_name_found_city: str
    ui_name_join_city: str
    ui_name_explode_nuclear: str
    ui_name_nuke_city: str
    ui_name_nuke_units: str
    ui_name_home_city: str
    ui_name_attack: str
    ui_name_suicide_attack: str
    ui_name_conquer_city: str
    ui_name_transform_terrain: str
    ui_name_cultivate: str
    ui_name_plant: str
    ui_name_pillage: str
    ui_name_clean_pollution: str
    ui_name_fortify: str
    ui_name_road: str
    ui_name_build_base: str
    ui_name_build_mine: str
    ui_name_irrigate: str
    ui_name_transport_alight: str
    ui_name_transport_board: str
    ui_name_transport_unload: str
    ui_name_transport_disembark: str
    ui_name_transport_embark: str
    quiet_actions: str


@section("borders")
@typechecked
@dataclass
class BordersData:
    radius_sq_city: int
    size_effect: int
    radius_sq_city_permanent: int


@section("research")
@typechecked
@dataclass
class ResearchData:
    tech_cost_style: str
    base_tech_cost: int
    tech_leakage: str
    tech_upkeep_style: str
    free_tech_method: str


@section("culture")
@typechecked
@dataclass
class CultureData:
    victory_min_points: int
    victory_lead_pct: int
    history_interest_pml: int
    migration_pml: int


@section("calendar")
@typechecked
@dataclass
class CalendarData:
    skip_year_0: bool
    fragments: int
    fragment_name0: str
    fragment_name1: str
    positive_label: str
    negative_label: str


# TODO: Figure out how to pull in the [settings] set = {} block


@typechecked
class Ruleset:
    freeciv_version: str
    name: str
    version: str
    summary: str
    description: str

    unit_classes: list
    unit_types: list
    advances: list
    veteran_levels: list
