import re
from dataclasses import dataclass, field
from typing import Literal, Union

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
    alt_dir: str = ""  # FIXME default?


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
    granary_food_ini: list[int]
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
    civil_war_enabled: bool
    civil_war_bonus_celebrating: int
    civil_war_bonus_unhappy: int
    gameloss_style: str
    paradrop_to_transport: bool
    gold_upkeep_style: str
    output_granularity: int
    initial_diplomatic_state: str = "War"
    base_pollution: int = 0  # FIXME default?
    happy_cost: int = 0  # FIXME default?
    food_cost: int = 0  # FIXME default?
    base_bribe_cost: int = 0  # FIXME default?
    ransom_gold: int = 0  # FIXME default?


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
    base_incite_cost: int = 0  # FIXME default?


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


ActionRange = Union[int, Literal["unlimited"]]


@section("actions")
@typechecked
@dataclass
class ActionsData:
    force_trade_route: bool
    force_capture_units: bool
    force_bombard: bool
    force_explode_nuclear: bool
    help_wonder_max_range: ActionRange
    recycle_unit_max_range: ActionRange
    bombard_max_range: ActionRange
    bombard_2_max_range: ActionRange
    bombard_3_max_range: ActionRange
    explode_nuclear_max_range: ActionRange
    nuke_city_max_range: ActionRange
    nuke_units_max_range: ActionRange
    ui_name_bribe_unit: str = ""  # FIXME default?
    ui_name_sabotage_city: str = ""  # FIXME default?
    ui_name_incite_city: str = ""  # FIXME default?
    ui_name_establish_embassy_stay: str = ""  # FIXME default?
    ui_name_steal_tech: str = ""  # FIXME default?
    ui_name_investigate_city_spend_unit: str = ""  # FIXME default?
    ui_name_establish_trade_route: str = ""  # FIXME default?
    ui_name_enter_marketplace: str = ""  # FIXME default?
    ui_name_help_wonder: str = ""  # FIXME default?
    ui_name_recycle_unit: str = ""  # FIXME default?
    ui_name_disband_unit: str = ""  # FIXME default?
    ui_name_found_city: str = ""  # FIXME default?
    ui_name_join_city: str = ""  # FIXME default?
    ui_name_explode_nuclear: str = ""  # FIXME default?
    ui_name_nuke_city: str = ""  # FIXME default?
    ui_name_nuke_units: str = ""  # FIXME default?
    ui_name_home_city: str = ""  # FIXME default?
    ui_name_attack: str = ""  # FIXME default?
    ui_name_suicide_attack: str = ""  # FIXME default?
    ui_name_conquer_city: str = ""  # FIXME default?
    ui_name_transform_terrain: str = ""  # FIXME default?
    ui_name_cultivate: str = ""  # FIXME default?
    ui_name_plant: str = ""  # FIXME default?
    ui_name_pillage: str = ""  # FIXME default?
    ui_name_clean_pollution: str = ""  # FIXME default?
    ui_name_fortify: str = ""  # FIXME default?
    ui_name_road: str = ""  # FIXME default?
    ui_name_build_base: str = ""  # FIXME default?
    ui_name_build_mine: str = ""  # FIXME default?
    ui_name_irrigate: str = ""  # FIXME default?
    ui_name_transport_alight: str = ""  # FIXME default?
    ui_name_transport_board: str = ""  # FIXME default?
    ui_name_transport_unload: str = ""  # FIXME default?
    ui_name_transport_disembark: str = ""  # FIXME default?
    ui_name_transport_embark: str = ""  # FIXME default?
    ui_name_poison_city_escape: str = ""  # FIXME default?
    ui_name_suitcase_nuke_escape: str = ""  # FIXME default?
    ui_name_sabotage_unit_escape: str = ""  # FIXME default?
    ui_name_sabotage_city_escape: str = ""  # FIXME default?
    ui_name_targeted_sabotage_city_escape: str = ""  # FIXME default?
    ui_name_sabotage_city_production_escape: str = ""  # FIXME default?
    ui_name_incite_city_escape: str = ""  # FIXME default?
    ui_name_establish_embassy: str = ""  # FIXME default?
    ui_name_steal_tech_escape: str = ""  # FIXME default?
    ui_name_targeted_steal_tech_escape: str = ""  # FIXME default?
    ui_name_investigate_city: str = ""  # FIXME default?
    ui_name_upgrade_unit: str = ""  # FIXME default?
    ui_name_paradrop_unit: str = ""  # FIXME default?
    ui_name_airlift_unit: str = ""  # FIXME default?
    ui_name_capture_units: str = ""  # FIXME default?
    ui_name_bombard: str = ""  # FIXME default?
    ui_name_conquer_city_2: str = ""  # FIXME default?
    ui_name_clean_fallout: str = ""  # FIXME default?
    ui_name_transport_disembark_2: str = ""  # FIXME default?
    ui_name_steal_maps_escape: str = ""  # FIXME default?
    ui_name_destroy_city: str = ""  # FIXME default?
    ui_name_spy_attack: str = ""  # FIXME default?
    ui_name_spread_plague: str = ""  # FIXME default?
    ui_name_user_action_1: str = ""  # FIXME default?
    user_action_1_target_kind: str = "" # FIXME default?
    user_action_1_min_range: int = 0 # FIXME default?
    user_action_1_max_range: ActionRange = "unlimited" # FIXME default?
    user_action_1_actor_consuming_always: bool = True # FIXME default?
    spread_plague_actor_consuming_always: bool = False # FIXME default?
    airlift_max_range: ActionRange = "unlimited"  # FIXME correct?
    quiet_actions: list[str] = field(default_factory=list)
    poison_empties_food_stock: bool = True  # FIXME correct?
    steal_maps_reveals_all_cities: bool = True # FIXME correct?


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
    tech_upkeep_divider: int = 0  # FIXME default?


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
    positive_label: str
    negative_label: str
    fragment_name0: str = None
    fragment_name1: str = None
    start_year: int = 0  # FIXME default?


@typechecked
@dataclass
class Setting:
    name: str
    value: Union[bool, int, str]
    lock: bool = False


@section("settings")
@typechecked
@dataclass
class Settings:
    set: list[Setting] = field(default_factory=list)


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
