import re
from dataclasses import dataclass, field
from typing import Literal, Union

from typeguard import typechecked

from freeciv.effects import Requirement

from .secfile.loader import read_section, section


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
    version_help_rst: str = (
        ". If the value is ``-1``, then there is no version for this ruleset."
    )
    alt_dir: str = ""  # FIXME default?
    summary: str = ""
    description: str = ""
    capabilities: str = ""  # 3.0
    capabilities_help_rst: str = (
        "This ruleset has the following scenario capabilities: "
    )


@section("options")
@typechecked
@dataclass
class OptionsData:
    global_init_techs: str
    global_init_buildings: str

    global_init_techs_help_rst: str = "This ruleset starts a player with the folliwing technology advances at game start: "

    global_init_buildings_help_rst: str = "This ruleset starts a player with the following city improvements (buildings) at game start: "


@section("tileset")
@typechecked
@dataclass
class TilesetData:
    preferred: str = ""
    preferred_help_rst = "This ruleset has the following preferred tileset: "


@section("soundset")
@typechecked
@dataclass
class SoundsetData:
    preferred: str = ""
    preferred_help_rst = "This ruleset has the following preferred soundset: "


@section("musicset")
@typechecked
@dataclass
class MusicsetData:
    preferred: str = ""
    preferred_help_rst = "This ruleset has the following preferred musicset: "


@section("civstyle")
@typechecked
@dataclass
class CivStyleData:
    # Object Attributes
    granary_food_ini: list[int]
    base_pollution: int = 0  # FIXME default?
    happy_cost: int = 0  # FIXME default?
    food_cost: int = 0  # FIXME default?
    granary_food_inc: int = 0
    min_city_center_food: int = 0
    min_city_center_shield: int = 0
    min_city_center_trade: int = 0
    init_city_radius_sq: int = 0
    init_vis_radius_sq: int = 0
    base_bribe_cost: int = 0  # FIXME default?
    ransom_gold: int = 0  # FIXME default?
    upgrade_veteran_loss: int = 0
    autoupgrade_veteran_loss: int = 0
    pillage_select: bool = True
    tech_steal_allow_holes: bool = True  # FIXME default?
    tech_trade_allow_holes: bool = True  # FIXME default?
    tech_trade_loss_allow_holes: bool = True  # FIXME default?
    tech_parasite_allow_holes: bool = True  # FIXME default?
    tech_loss_allow_holes: bool = True  # FIXME default?
    initial_diplomatic_state: str = "War"
    civil_war_enabled: bool = True  # FIXME default?
    civil_war_bonus_celebrating: int = 0  # FIXME default?
    civil_war_bonus_unhappy: int = 0  # FIXME default?
    gameloss_style: str = ""  # FIXME default?
    paradrop_to_transport: bool = True  # FIXME default?
    gold_upkeep_style: str = ""
    output_granularity: int = 1  # FIXME default?

    # Help Strings
    base_pollution_help_rst: str = "This value represents the base amount of pollution for each city."

    happy_cost_help_rst: str = "This value represents the cost in luxury goods of making one citizen happier in a city."

    food_cost_help_rst: str = "This value represents the amount of food it takes to maintain one citizen in a city."

    granary_food_ini_help_rst: str = "This is a list of city granary sizes as cities grow from size 1 to ``x``, where ``x`` is the last value of the list. Most rulesets stop at size 8, so the list will have 8 values in it. Some rulesets have only one value, which means that the city granary does not increase with city size and remains stable.\n\n  This ruleset has the following city granary sizes: "

    granary_food_inc_help_rst: str = "This value is related to the previous list above. If this value is greater than zero, it represents how much the city granary size grows for cities larger than the last value of the list above."

    min_city_center_food_help_rst: str = "The value represetns the minimum amount of food a city center tile generates"

    min_city_center_shield_help_rst: str = "The value represents the minimum amount of production (shields) a city center tile generates"

    min_city_center_trade_help_rst: str = "The value represents the minimum amount of trade a city center tile generates,"

    init_city_radius_sq_help_rst: str = "This value represents the input to define the initial working area for a city. The math is somewhat complicated and is documented on the legacy freeciv wiki at https://freeciv.fandom.com/wiki/Radius. The larger the value, the larger the working area for the city."

    init_vis_radius_sq_help_rst: str = "This value represents the input to define the initial vision area for a city. The math is somewhat complicated and is documented on the legacy freeciv wiki at https://freeciv.fandom.com/wiki/Radius. The larger the value, the larger the vision area for the city."

    base_bribe_cost_help_rst: str = "This value represents the base cost in gold to bribe a unit."

    ransom_gold_help_rst: str = "This value represents the amound of gold is paid in ransom when a :unit:`Barbarian Leader` is killed."

    upgrade_veteran_loss_help_rst: str = "Increments of ``10`` is one veteran level per upgrade."

    autoupgrade_veteran_loss_help_rst: str = "Increments of ``10`` is one veteran level per auto-upgrade."

    pillage_select_help_rst: str = "When set to ``True``, the player gets to select which terrain improvement to pillage."

    tech_steal_allow_holes_help_rst: str = "When set to ``True``, the player can steal a technology advance for which prerequisites are not known."

    tech_trade_allow_holes_help_rst: str = "When set to ``True``, the player can trade a technology advance to another player even if the other player has not discovered the prerequisite advance(s). This can happen in reverse as well."

    tech_trade_loss_allow_holes_help_rst: str = "When set to ``True``, the player can lose a technology advance and not impact other prerequisite advances."

    tech_parasite_allow_holes_help_rst: str = "When set to ``True``, the player can gain a technology advance for which prerequisites are not known via the ``parasite`` effect (e.g. Great Library)."

    tech_loss_allow_holes_help_rst: str = "When set to ``True``, the player can lose a technology advance with negative bulbs and not impact other prerequisite advances."

    initial_diplomatic_state_help_rst: str = "This value represents the diplomatic state between two nations that meet for the first time."

    civil_war_enabled_help_rst: str = "When set to ``True``, civil war in enabled."

    civil_war_bonus_celebrating_help_rst: str = "This value indicates how many *percents* each celebrating city affects the chance of civil war."

    civil_war_bonus_unhappy_help_rst: str = "This value indicates how many *percents* each unhappy city affects the chance of civil war."

    gameloss_style_help_rst: str = "A list of things to happen, in addition to death of the owner, when a :strong:`gameloss` unit (e.g. the last unit) dies. `CivilWar`: Part of the nation remains, controlled by a new player. `Barbarians`: Depending on if there is also `CivilWar`, all or part or half of the dead player's empire goes under barbarian control. `Loot`: The player who killed the :strong:`gameloss` unit gets loot, such as a partial map, gold, technologies, or cities."

    paradrop_to_transport_help_rst: str = "When set to ``True``, units may safely paradrop to a transport on non-native terrain."

    gold_upkeep_style_help_rst: str = "This value represents the method of paying unit and improvement gold upkeep.\n\n  * `City`: The player's total gold must be non-negative after paying upkeep costs associated with each city. If for any city the player's gold is negative, random buildings in the city are sold off. If the gold is still negative, then supported units with gold upkeep are disbanded.\n\n  * `Mixed`: In the first step, the player's total gold must be non-negative after paying upkeep for all buildings within a city. If for any city the player's gold is negative, random buildings in the city are sold off. In the second step, gold upkeep for all units is paid in a lump sum. If the player does not have enough gold, random units with gold upkeep are disbanded.\n\n  * `Nation`: Gold upkeep for all buildings and units is paid in a lump sum after all cities have been processed. If the player does not have enough gold, random buildings from random cities are sold. If still more gold is needed, then random units with gold upkeep are disbanded."

    output_granularity_help_rst: str = "This value represents how granular city output is shown. This is typically some form of :math:`10^n`."


@section("illness")
@typechecked
@dataclass
class IllnessData:
    # Object Attributes
    illness_on: bool
    illness_base_factor: int
    illness_min_size: int
    illness_trade_infection: int
    illness_pollution_factor: int

    # Help Strings
    illness_on_help_rst: str = "When set to ``True``, illness (plague) is enabled for the game."

    illness_base_factor_help_rst: str = "This value defines the percentage factor of how plague is calculated."

    illness_min_size_help_rst: str = "This value defines the minimum city size for plague to be in effect."

    illness_trade_infection_help_rst: str = "This value is the percentage factor for how much trading with a plagued city increases our city's chance for plague."

    illness_pollution_factor_help_rst: str = "This value is the percentage factor for how much pollution within a city increases its chance for plague."


@section("incite_cost")
@typechecked
@dataclass
class InciteCostData:
    # Object Attributes
    improvement_factor: int
    unit_factor: int
    total_factor: int
    base_incite_cost: int = 0  # FIXME default?

    # Help Strings
    improvement_factor_help_rst: str = "The values for ``base_incite_cost``, ``improvement_factor``, ``unit_factor``, and ``total_factor`` are used as part of a math equation to calculate the cost to incide a city. The formula is:\n\n  :math:`city\_incite\_cost = total\_factor * (city\_size) * (base\_incite\_cost + (units\_cost)`\n\n  :math:`* unit\_factor + (improvements\_cost) * improvement\_factor)`\n\n  :math:`/ ((distance\_to\_capital) * 100)`"


@section("combat_rules")
@typechecked
@dataclass
class CombatRulesData:
    # Object Attributes
    tired_attack: bool

    # LT53
    incite_gold_capt_chance: int = 0
    incite_gold_loss_chance: int = 0
    timeoutmask: int = 0

    only_killing_makes_veteran: bool = False  # FIXME 3.0?
    nuke_pop_loss_pct: int = 50
    nuke_defender_survival_chance_pct: int = 0

    # LT30
    killstack: bool = True

    # Help Strings
    incite_gold_capt_chance_help_rst: str = "If a :unit:`Diplomat` or :unit:`Spy` incites for gold, this value represents the chance of success."

    incite_gold_loss_chance_help_rst: str = "If a :unit:`Diplomat` or :unit:`Spy` incites for gold, this value represents the chance of loss."

    timeoutmask_help_rst: str = "? help needs help ?"

    tired_attack_help_rst: str = "When set to ``True``, units that attack with less than a single move point (per ``move_fragments`` in Terrain) will have their attack power reduced accordingly."

    only_killing_makes_veteran_help_rst: str = "With some rules it is possible that neither side of a combat action dies. When this is set to ``True``, if unit should never gain veterancy from such a combat."

    nuke_pop_loss_pct_help_rst: str = "The value defines the percentage of population lost by a city after a nuclear attak. If set to ``100``, the city is destroyed along with all the units. If set to ``0``, the city does not loose population. Any value below ``100`` means the city can never be destroyed completely using a nuclear unit."

    nuke_defender_survival_chance_pct_help_rst: str = "The value defines the percentage chance of a city defender surviving a nuclear attack. When set to ``50``, roughly half of the defenders will survive a nuclear attack. When set to ``0`` no defenders will survive. When set to ``100`` all defenders will survive."

    killstack_help_rst: str = "When set to ``True``, a stack of units can be completely destroyed when the strongest defender is killed."



@section("auto_attack")
@typechecked
@dataclass
class AutoAttackData:
    # Object Attributes
    attack_actions: list[str] = field(default_factory=list)  # FIXME 3.0?
    if_attacker: list[Requirement] = field(default_factory=list)
    will_never: list[str] = field(default_factory=list)  # FIXME ???

    # Help Strings
    attack_actions_help_rst: str = "An auto attack may be triggered when another unit moves to an adjacent tile and the ``autoattack`` server setting is enabled. The values are the possible actions.\n\n  The values for this ruleset is: "
    if_attacker_help_rst: str = "This is a requirement vector table listing the rules that all must be true for auto attack actions to occur.\n\n  The requirements for this ruleset are: "
    will_never_help_rst: str = "? help needs help on ``will_never_help`` ?\n\n  The value for this ruleset is: "


ActionRange = Union[int, Literal["unlimited"]]

@section("actions")
@typechecked
@dataclass
class ActionsData:
    # Object Attributes
    force_trade_route: bool = True  # FIXME before 3.0?
    force_capture_units: bool = True  # FIXME before 3.0?
    force_bombard: bool = True  # FIXME before 3.0?
    force_explode_nuclear: bool = True  # FIXME before 3.0?
    poison_empties_food_stock: bool = True  # FIXME correct?
    steal_maps_reveals_all_cities: bool = True  # FIXME correct?
    help_wonder_max_range: ActionRange = 1  # FIXME before 3.0?
    recycle_unit_max_range: ActionRange = 1  # FIXME before 3.0?
    bombard_max_range: ActionRange = 1  # FIXME before 3.0?
    bombard_2_max_range: ActionRange = 1  # FIXME before 3.0?
    bombard_3_max_range: ActionRange = 1  # FIXME before 3.0?
    explode_nuclear_max_range: ActionRange = 1  # FIXME before 3.0?
    nuke_city_max_range: ActionRange = 1  # FIXME before 3.0?
    nuke_units_max_range: ActionRange = 1  # FIXME before 3.0?
    airlift_max_range: ActionRange = "unlimited"

    # Help Strings
    force_trade_route_help_rst: str = "If set to ``True``, it is illegal for a unit to enter the marketplace of a city if it can establish a trade route to it instead."

    force_capture_units_help_rst: str = "If set to ``True``, it is illegal for a unit to bombard, explode a nuclear or perform a regular attack against a tile if it can capture units on it instead."

    force_bombard_help_rst: str = "If set to ``True``, it is illegal for a unit to explode a nuclear or perform a regular attack against a tile if it can bombard it instead."

    force_explode_nuclear_help_rst: str = "If set to ``True``, it is illegal for a unit to perform a regular attack against a tile if it can explode a nuclear unit instead."

    poison_empties_food_stock_help_rst: str = "If set to ``True``, a successful `Poison City` or `Poison City Escape` action will empty the food stock (city granary)."

    steal_maps_reveals_all_cities_help_rst: str = "If set to ``True``, a successful `Steal Maps` or `Steal Maps Escape` action will transfer the map for all tiles containing a city."

    help_wonder_max_range_help_rst: str = "The maximum distance from the unit to the target of the `Help Build Wonder` action. The value ``0`` means that the target's tile must be the tile of the unit. The value ``1`` means that the city must be on a tile adjacent to the unit. The special value ``unlimited`` lifts the maximum distance restriction. The maximum distance cannot be smaller than the minimum distance."

    recycle_unit_max_range_help_rst: str = "The maximum distance from the unit to the target of the `Recycle Unit` action. The value ``0`` means that the target's tile must be the tile of the unit. The value ``1`` means that the city must be on a tile adjacent to the unit. The special value ``unlimited`` lifts the maximum distance restriction. The maximum distance cannot be smaller than the minimum distance."

    bombard_max_range_help_rst: str = "The maximum distance from the unit to the target of the `Bombard` action. The value ``1`` means that the targets must be on a tile adjacent to the unit. The special value ``unlimited`` lifts the maximum distance restriction. The maximum distance cannot be smaller than the minimum distance."

    bombard_2_max_range_help_rst: str = "The maximum distance from the unit to the target of the `Bombard 2` action. The value ``1`` means that the targets must be on a tile adjacent to the unit. The special value ``unlimited`` lifts the maximum distance restriction. The maximum distance cannot be smaller than the minimum distance."

    bombard_3_max_range_help_rst: str = "The maximum distance from the unit to the target of the `Bombard 3` action. The value ``1`` means that the targets must be on a tile adjacent to the unit. The special value ``unlimited`` lifts the maximum distance restriction. The maximum distance cannot be smaller than the minimum distance."

    explode_nuclear_max_range_help_rst: str = "The maximum distance from the unit to the target of the `Explode Nuclear` action. The value ``0`` means that the target tile must be the tile of the unit. The value ``1`` means that the tile must be a tile adjacent to the unit. The special value ``unlimited`` lifts the maximum distance restriction. The maximum distance cannot be smaller than the minimum distance."

    nuke_city_max_range_help_rst: str = "The maximum distance from the unit to the target of the `Nuke City` action. The value ``1`` means that the tile must be a tile adjacent to the unit. The special value ``unlimited`` lifts the maximum distance restriction. The maximum distance cannot be smaller than the minimum distance."

    nuke_units_max_range_help_rst: str = "The maximum distance from the unit to the target of the `Nuke Units` action. The value ``1`` means that the tile must be a tile adjacent to the unit. The special value ``unlimited`` lifts the maximum distance restriction. The maximum distance cannot be smaller than the minimum distance."

    airlift_max_range_help_rst: str = "The maximum distance from the unit to the target of the `Airlift Unit` action. The value ``1`` means that the targets must be on a tile adjacent to the unit. The special value ``unlimited`` lifts the maximum distance restriction. The maximum distance cannot be smaller than the minimum distance."

    # Collection of UI strings, not really part of documentation.
    ui_name_poison_city: str = ""  # FIXME default?
    ui_name_poison_city_escape: str = ""  # FIXME default?
    ui_name_suitcase_nuke: str = ""  # FIXME default?
    ui_name_suitcase_nuke_escape: str = ""  # FIXME default?
    ui_name_sabotage_unit: str = ""  # FIXME default?
    ui_name_sabotage_unit_escape: str = ""  # FIXME default?
    ui_name_bribe_unit: str = ""  # FIXME default?
    ui_name_sabotage_city: str = ""  # FIXME default?
    ui_name_sabotage_city_escape: str = ""  # FIXME default?
    ui_name_targeted_sabotage_city: str = ""  # FIXME default?
    ui_name_targeted_sabotage_city_escape: str = ""  # FIXME default?
    ui_name_sabotage_city_production_escape: str = ""  # FIXME default?
    ui_name_incite_city: str = ""  # FIXME default?
    ui_name_incite_city_escape: str = ""  # FIXME default?
    ui_name_establish_embassy: str = ""  # FIXME default?
    ui_name_establish_embassy_stay: str = ""  # FIXME default?
    ui_name_steal_tech: str = ""  # FIXME default?
    ui_name_steal_tech_escape: str = ""  # FIXME default?
    ui_name_targeted_steal_tech: str = ""  # FIXME default?
    ui_name_targeted_steal_tech_escape: str = ""  # FIXME default?
    ui_name_investigate_city: str = ""  # FIXME default?
    ui_name_investigate_city_spend_unit: str = ""  # FIXME default?
    ui_name_establish_trade_route: str = ""  # FIXME default?
    ui_name_enter_marketplace: str = ""  # FIXME default?
    ui_name_help_wonder: str = ""  # FIXME default?
    ui_name_recycle_unit: str = ""  # FIXME default?
    ui_name_disband_unit: str = ""  # FIXME default?
    ui_name_capture_units: str = ""  # FIXME default?
    ui_name_found_city: str = ""  # FIXME default?
    ui_name_join_city: str = ""  # FIXME default?
    ui_name_bombard: str = ""  # FIXME default?
    ui_name_explode_nuclear: str = ""  # FIXME default?
    ui_name_nuke_city: str = ""  # FIXME default?
    ui_name_nuke_units: str = ""  # FIXME default?
    ui_name_home_city: str = ""  # FIXME default?
    ui_name_upgrade_unit: str = ""  # FIXME default?
    ui_name_paradrop_unit: str = ""  # FIXME default?
    ui_name_airlift_unit: str = ""  # FIXME default?
    ui_name_attack: str = ""  # FIXME default?
    ui_name_suicide_attack: str = ""  # FIXME default?
    ui_name_conquer_city: str = ""  # FIXME default?
    ui_name_conquer_city_2: str = ""  # FIXME default?
    ui_name_transform_terrain: str = ""  # FIXME default?
    ui_name_cultivate: str = ""  # FIXME default?
    ui_name_plant: str = ""  # FIXME default?
    ui_name_pillage: str = ""  # FIXME default?
    ui_name_clean_pollution: str = ""  # FIXME default?
    ui_name_clean_fallout: str = ""  # FIXME default?
    ui_name_fortify: str = ""  # FIXME default?
    ui_name_road: str = ""  # FIXME default?
    ui_name_build_base: str = ""  # FIXME default?
    ui_name_build_mine: str = ""  # FIXME default?
    ui_name_irrigate: str = ""  # FIXME default?
    ui_name_transport_alight: str = ""  # FIXME default?
    ui_name_transport_board: str = ""  # FIXME default?
    ui_name_transport_unload: str = ""  # FIXME default?
    ui_name_transport_disembark: str = ""  # FIXME default?
    ui_name_transport_disembark_2: str = ""  # FIXME default?
    ui_name_transport_embark: str = ""  # FIXME default?
    ui_name_user_action_1: str = ""  # FIXME default?
    user_action_1_target_kind: str = ""  # FIXME default?
    user_action_1_min_range: int = 0  # FIXME default?
    user_action_1_max_range: ActionRange = "unlimited"  # FIXME default?
    user_action_1_actor_consuming_always: bool = True  # FIXME default?
    spread_plague_actor_consuming_always: bool = False  # FIXME default?

    quiet_actions: list[str] = field(default_factory=list)

    ui_name_heal_unit: str = ""  # FIXME default?
    ui_name_steal_maps_escape: str = ""  # FIXME default?
    ui_name_destroy_city: str = ""  # FIXME default?
    ui_name_spy_attack: str = ""  # FIXME default?
    ui_name_spread_plague: str = ""  # FIXME default?


@section("borders")
@typechecked
@dataclass
class BordersData:
    # Object Attributes
    radius_sq_city: int
    size_effect: int
    radius_sq_city_permanent: int = 0  # FIXME 2.6?

    # Help Strings
    radius_sq_city_help_rst: str = "This value represents the input to define the initial border area outside a city. The math is somewhat complicated and is documented on the legacy freeciv wiki at https://freeciv.fandom.com/wiki/Radius. The larger the value, the larger the border area for the city."
    size_effect_help_rst: str = "The border area increases by this amount divided by the of city size."
    radius_sq_city_permanent_help_rst: str = "This value is the difference between a city's workable area and the area permanently claimed by the city. These tiles cannot be stolen by a stronger border source. A value of ``0`` means the city workable area is immune to border stealing. A negative value means outer workable tiles can be stolen. Highly negative values (more than max city area) means any workable tile can be stolen. If the city area value is variable, so is the set of locked tiles. This is a squared value, so the radius of the ring of tiles which are workable, but not locked (or vice versa) varies but the area is constant."


@section("research")
@typechecked
@dataclass
class ResearchData:
    # Object Attributes
    tech_upkeep_style: str
    tech_cost_style: str = ""  # FIXME default?
    base_tech_cost: int = 0  # FIXME default?
    tech_leakage: str = ""  # FIXME default?
    tech_upkeep_divider: int = 0  # FIXME default?
    free_tech_method: str = ""  # FIXME default?

    # Help Strings
    tech_cost_style_help_rst: str = "This is the method of calculating technology costs.\n\n  * `Civ I|II`: Civ (I|II) style. Every new technology adds ``base_tech_cost`` (see below) to the cost of the next technology.\n\n  * `Classic`: The cost of technology is: :math:`base\_tech\_cost * (1 + reqs) * sqrt(1 + reqs) / 2`, where ``reqs`` equals the number of requirements for the technology advance, counted recursively.\n\n  * `Classic+`: The costs are read from :file:`tech.ruleset`. Missing costs are generated by style `Classic`.\n\n  * `Experimental`: The cost of technology is: :math:`base\_tech\_cost * (reqs^2 / (1 + sqrt(sqrt(reqs + 1))) - 0.5), where ``reqs`` equals the number of requirements for the technology, counted recursively. Initial technology cost will be ``base_tech_cost``.\n\n  * `Experimental+`: The costs are read from :file:`tech.ruleset`. Missing costs are generated by style `Experimental`.\n\n  * `Linear`: The cost of technology is: :math:`base\_tech\_cost * reqs`, where ``reqs`` equals the number of requirements for the technology, counted recursively."

    base_tech_cost_help_rst: str = "The value defines the base research cost for technology advances. Used in ``tech_cost_style`` (above), where the technology cost is generated. In other words: used everywhere unless the cost of :strong:`all` technologies are specified and the technology cost style is `Experimental+` or `Classic+`."

    tech_leakage_help_rst: str = "This value defined how technology leakage occurs from other civilizations.\n\n  * `None`: There is no reduction of the technology cost.\n\n  * `Embassies`: The technology cost is reduced depending on the number of players which already know the technology and you have an embassy with.\n\n  * `All Players`: The technology cost is reduced depending on the number of all players (human, AI and barbarians) which already know the technology.\n\n  * `Normal Players`: The technology cost is reduced depending on the number of normal players (human and AI) which already know the technology."

    tech_upkeep_style_help_rst: str = "This is the method of paying technology upkeep.\n\n  * `None`: This is no technology upkeep.\n\n  * `Basic`: The technology upkeep is calculated as: :math:`cost\_of\_technology / tech\_upkeep\_divider - tech\_upkeep\_free`.\n\n  * `Cities`: The technology upkeep is calculated like `Basic`, but multiplied by the number of cities."

    tech_upkeep_divider_help_rst: str = "The upkeep cost is divided by this value. It is essentially an over-ride value."

    free_tech_method_help_rst: str = "This value represents the method of selecting technologies given for free.\n\n  * `Goal`: Applied towards a player's technology goal. If no goal is set, then a random technology advance is set.\n\n  * `Random`: A random researchable technology is picked.\n\n  * `Cheapest`: The cheapest researchable technology advance, random among equal cost ones."


@section("culture")
@typechecked
@dataclass
class CultureData:
    # Object Attributes
    victory_min_points: int
    victory_lead_pct: int
    migration_pml: int
    history_interest_pml: int = 0  # FIXME 3.0?

    # Help Strings
    victory_min_points_help_rst: str = "The minimum culture points for cultural domination victory."

    victory_lead_pct_help_rst: str = "How big of a lead relative to second best player that is needed for cultural domination victory."

    migration_pml_help_rst: str = "How much existing history grows each turn. This makes older history of the same  original value more valuable as newer history, as it has gained more interest."

    history_interest_pml_help_rst: str = "How much each culture point affects the migration from/to the city. Each culture point counts as this many permilles of a migration point."

@section("calendar")
@typechecked
@dataclass
class CalendarData:
    # Object Attributes
    skip_year_0: bool
    positive_label: str
    negative_label: str
    start_year: int = 0  # FIXME default?
    fragments: int = 1  # FIXME default?
    fragment_name0: str = None
    fragment_name1: str = None
    fragment_name2: str = None

    # Help Strings
    start_year_help_rst: str = "This value defines the year the game starts."

    skip_year_0_help_rst: str = "If set to ``True`` the game starts at Year 1."

    fragments_help_rst: str = "The game calendar year can be broken into fragments. This value defines the number of year fragments."

    fragment_name0_help_rst: str = "The first calendar year fragment name."

    fragment_name1_help_rst: str = "The second calendar year fragment name."

    fragment_name2_help_rst: str = "The third calendar year fragment name."


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


class GameSettings:
    def __init__(self, sections):
        self.about = read_section(AboutData, sections)
        self.actions = read_section(ActionsData, sections, missing_ok=True)
        self.auto_attack = read_section(AutoAttackData, sections, missing_ok=True)
        self.borders = read_section(BordersData, sections)
        self.calendar = read_section(CalendarData, sections)
        self.civ_style = read_section(CivStyleData, sections)
        self.combat_rules = read_section(CombatRulesData, sections)
        self.culture = read_section(CultureData, sections, missing_ok=True)
        self.data_file_header = read_section(DataFileHeader, sections, missing_ok=True)
        self.illness = read_section(IllnessData, sections)
        self.incite_cost = read_section(InciteCostData, sections)
        self.musicset = read_section(MusicsetData, sections, missing_ok=True)
        self.options = read_section(OptionsData, sections)
        self.research = read_section(ResearchData, sections)
        self.settings = read_section(Settings, sections)
        self.soundset = read_section(SoundsetData, sections, missing_ok=True)
        self.tileset = read_section(TilesetData, sections, missing_ok=True)
