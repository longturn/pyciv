{{ about.name }} Manual
{{ about.name.heading }}

{% if about.version %}{{ about.name }} Version: {{ about.version }}{% endif %}

General Game Information
========================

:strong:`Ruleset Summary`: {{ about.summary }}

{% if about.description %}:strong:`Ruleset Description`: {{ about.description }}{% endif %}

{% if about.capabilities %}
:strong:`Capabilities`
  {{ conf.capabilities }} {about.capabilities }}{% endif %}

{% if about.global_init_techs %}
:strong:`Start Technologies`
  {{ conf.global_init_techs }} {{ about.global_init_techs }}{% endif %}

{% if about.global_init_buildings %}
:strong:`Start Buildings`
  {{ conf.global_init_buildings }} {{ about.global_init_buildings }}{% endif %}

{% if tileset.preferred %}
:strong:`Preferred Tileset`
  {{ conf.preferred }} {{ tileset.preferred }}{% endif %}

{% if soundset.preferred %}
:strong:`Preferred Soundset`
  {{ conf.preferred }} {{ soundset.preferred }}{% endif %}

{% if musicset.preferred %}
:strong:`Preferred Musicset`
  {{ conf.preferred }} {{ musicset.preferred }}{% endif %}


Ruleset Features
================

Here are links to other features of this ruleset:

.. toctree::
  advances.rst
  buildings.rst
  governments.rst
  nations.rst
  terrain.rst
  units.rst
  :maxdepth: 2


Gameplay Parameters
===================

The following game parameters are set. Each impacts gameplay in some fashion.

{% if civstyle.granary_food_ini %}
:strong:`Granary Food Initial`
  {{ conf.granary_food_ini }} {{ civstyle.granary_food_ini }}{% endif %}

{% if civstyle.granary_food_inc %}
:strong:`Granary Food Increment`
  {{ conf.granary_food_inc }} {{ civstyle.granary_food_inc }}{% endif %}

{% if civstyle.min_city_center_food %}
:strong:`City Center: Food`
  {{ conf.min_city_center_food }} {{ civstyle.min_city_center_food }}{% endif %}

{% if civstyle.min_city_center_shield %}
:strong:`City Center: Shields`
  {{ conf.min_city_center_shield }} {{ civstyle.min_city_center_shield }}{% endif %}

{% if civstyle.init_city_radius_sq %}
:strong:`Initial City Radius`
  {{ conf.init_city_radius_sq }} {{ civstyle.init_city_radius_sq }}{% endif %}

{% if civstyle.init_vis_radius_sq %}
:strong:`Initial City Vision Radius`
  {{ conf.init_vis_radius_sq }} {{ civstyle.init_vis_radius_sq }}{% endif %}

{% if civstyle.upgrade_veteran_loss %}
:strong:`Unit Upgrade Veteran Level Loss`
  {{ conf.upgrade_veteran_loss }} {{ civstyle.upgrade_veteran_loss }}{% endif %}

{% if civstyle.autoupgrade_veteran_loss %}
:strong:`Autoupgrade Unit Veteran Level Loss`
  {{ conf.autoupgrade_veteran_loss }} {{ civstyle.autoupgrade_veteran_loss }}{% endif %}

{% if civstyle.pillage_select %}
:strong:`Pillage`
  {{ conf.pillage_select }} {{ civstyle.pillage_select }}{% endif %}

{% if civstyle.tech_steal_allow_holes %}
:strong:`Technology Steal`
  {{ conf.tech_steal_allow_holes }} {{ civstyle.tech_steal_allow_holes }}{% endif %}

{% if civstyle.tech_trade_allow_holes %}
:strong:`Technology Trade`
  {{ conf.tech_trade_allow_holes }} {{ civstyle.tech_trade_allow_holes }}{% endif %}

{% if civstyle.tech_trade_loss_allow_holes %}
:strong:`Technology Trade Allow Holes`
  {{ conf.tech_trade_loss_allow_holes }} {{ civstyle.tech_trade_loss_allow_holes }}{% endif %}

{% if civstyle.tech_parasite_allow_holes %}
:strong:`Technology Parasite Allow Hles`
  {{ conf.tech_parasite_allow_holes }} {{ civstyle.tech_parasite_allow_holes }}{% endif %}

{% if civstyle.tech_loss_allow_holes %}
:strong:`Technology Loss Allow Holes`
  {{ conf.tech_loss_allow_holes }} {{ civstyle.tech_loss_allow_holes }}{% endif %}

{% if civstyle.initial_diplomatic_state %}
:strong:`Initial Diplomatic State`
  {{ conf.initial_diplomatic_state }} {{ civstyle.initial_diplomatic_state }}{% endif %}

{% if civstyle.civil_war_enabled %}
:strong:`Civil War`
  {{ conf.civil_war_enabled }} {{ civstyle.civil_war_enabled }}{% endif %}

{% if civstyle.civil_war_bonus_celebrating %}
:strong:`Civil War Celebration`
  {{ conf.civil_war_bonus_celebrating }} {{ civstyle.civil_war_bonus_celebrating }}{% endif %}

{% if civstyle.civil_war_bonus_unhappy %}
:strong:`Civil War Unhappiness`
  {{ conf.civil_war_bonus_unhappy }} {{ civstyle.civil_war_bonus_unhappy }}{% endif %}

{% if civstyle.gameloss_style %}
:strong:`End Game`
  {{ conf.gameloss_style }} {{ civstyle.gameloss_style }}{% endif %}

{% if civstyle.gold_upkeep_style %}
:strong:`Gold Upkeep`
  {{ conf.gold_upkeep_style }} {{ civstyle.gold_upkeep_style }}{% endif %}

{% if illness.illness_on %}
:strong:`Plague`
  {{ conf.illness_on }} {{ illness.illness_on }}{% endif %}

{% if illness.illness_base_factor %}
:strong:`Plague Base Factor`
  {{ conf.illness_base_factor }} {{ illness.illness_base_factor }}{% endif %}

{% if illness.illness_min_size %}
:strong:`Plague Min City Size`
  {{ conf.illness_min_size }} {{ illness.illness_min_size }}{% endif %}

{% if illness.illness_trade_infection %}
:strong:`Plague Follows Trade Routes`
  {{ conf.illness_trade_infection }} {{ illness.illness_trade_infection }}{% endif %}

{% if illness.illness_pollution_factor %}
:strong:`Plague Pollution`
  {{ conf.illness_pollution_factor }} {{ illness.illness_pollution_factor }}{% endif %}

{% if incite_cost.improvement_factor %}
:strong:`Unit Incite Cost Factors`
  {{ conf.improvement_factor }} {{ incite_cost.improvement_factor. }}, {{ conf.incite_cost.unit_factor. }},
  {{ incite_cost.total_factor. }}{% endif %}

{% if combat_rules.tired_attack %}
:strong:`Tired Attack`
  {{ conf.tired_attack }} {{ combat_rules.tired_attack }}{% endif %}

{% if combat_rules.only_killing_makes_veteran %}
:strong:`Kill to Veteran`
  {{ conf.only_killing_makes_veteran }} {{ combat_rules.only_killing_makes_veteran }}{% endif %}

{% if combat_rules.nuke_pop_loss_pct %}
:strong:`Nuke Loss`
  {{ conf.nuke_pop_loss_pct }} {{ combat_rules.nuke_pop_loss_pct }}{% endif %}

{% if combat_rules.nuke_defender_survival_chance_pct %}
:strong:`Nuke Defender`
  {{ conf.nuke_defender_survival_chance_pct }} {{ combat_rules.nuke_defender_survival_chance_pct }}{% endif %}

{% if auto_attack.attack_actions %}
:strong:`Auto Attack`
  {{ conf.attack_actions }} {{ auto_attack.attack_actions }}{% endif %}

{% if actions.force_trade_route %}
:strong:`Trade Route`
  {{ conf.force_trade_route }} {{ actions.force_trade_route }}{% endif %}

{% if actions.force_capture_units %}
:strong:`Capture Units`
  {{ conf.force_capture_units }} {{ actions.force_capture_units }}{% endif %}

{% if actions.force_bombard %}
:strong:`Bombard`
  {{ conf.force_bombard }} {{ actions.force_bombard }}{% endif %}

{% if actions.force_explode_nuclear %}
:strong:`Explode Nuclear`
  {{ conf.force_explode_nuclear }} {{ actions.force_explode_nuclear }}{% endif %}

{% if actions.poison_empties_food_stock %}
:strong:`Empty Food Granary`
  {{ conf.poison_empties_food_stock }} {{ actions.poison_empties_food_stock }}{% endif %}

{% if actions.steal_maps_reveals_all_cities %}
:strong:`Reveal Cities`
  {{ conf.steal_maps_reveals_all_cities }} {{ actions.steal_maps_reveals_all_cities }}{% endif %}

{% if actions.help_wonder_max_range %}
:strong:`Help Build Wonder Range`
  {{ conf.help_wonder_max_range }} {{ actions.help_wonder_max_range }}{% endif %}

{% if actions.recycle_unit_max_range %}
:strong:`Recycle Unit Range`
  {{ conf.recycle_unit_max_range }} {{ actions.recycle_unit_max_range }}{% endif %}

{% if actions.bombard_max_range %}
:strong:`Bombard Range`
  {{ conf.bombard_max_range }} {{ actions.bombard_max_range }}{% endif %}

{% if actions.bombard_2_max_range %}
:strong:`Bombard 2 Range`
  {{ conf.bombard_2_max_range }} {{ actions.bombard_2_max_range }}{% endif %}

{% if actions.bombard_3_max_range %}
:strong:`Bombard 3 Range`
  {{ conf.bombard_3_max_range }} {{ actions.bombard_3_max_range }}{% endif %}

{% if actions.explode_nuclear_max_range %}
:strong:`Explode Nuke Range`
  {{ conf.explode_nuclear_max_range }} {{ actions.explode_nuclear_max_range }}{% endif %}

{% if actions.nuke_city_max_range %}
:strong:`Nuke City Range`
  {{ conf.nuke_city_max_range }} {{ actions.nuke_city_max_range }}{% endif %}

{% if actions.nuke_units_max_range %}
:strong:`Nuke Units Range`
  {{ conf.nuke_units_max_range }} {{ actions.nuke_units_max_range }}{% endif %}

{% if borders.radius_sq_city %}
:strong:`Border Radius`
  {{ conf.radius_sq_city }} {{ borders.radius_sq_city }}{% endif %}

{% if borders.size_effect %}
:strong:`Border Size`
  {{ conf.size_effect }} {{ borders.size_effect }}{% endif %}

{% if borders.radius_sq_city_permanent %}
:strong:`Border City Range`
  {{ conf.radius_sq_city_permanent }} {{ borders.radius_sq_city_permanent }}{% endif %}

{% if research.tech_cost_style %}
:strong:`Tech Cost Style`
  {{ conf.tech_cost_style }} {{ research.tech_cost_style }}{% endif %}

{% if research.base_tech_cost %}
:strong:`Base Tech Cost`
  {{ conf.base_tech_cost }} {{ research.base_tech_cost }}{% endif %}

{% if research.tech_leakage %}
:strong:`Technology Leakage`
  {{ conf.tech_leakage }} {{ research.tech_leakage }}{% endif %}

{% if research.tech_upkeep_style %}
:strong:`Technology Upkeep`
  {{ conf.tech_upkeep_style }} {{ research.tech_upkeep_style }}{% endif %}

{% if research.free_tech_method %}
:strong:`Free Technology Method`
  {{ conf.free_tech_method }} {{ research.free_tech_method }}{% endif %}

{% if culture.victory_min_points %}
:strong:`Culture Victory Points`
  {{ conf.victory_min_points }} {{ culture.victory_min_points }}{% endif %}

{% if culture.victory_lead_pct %}
:strong:`Culture Victory Percentage Lead`
  {{ conf.victory_lead_pct }} {{ culture.victory_lead_pct }}{% endif %}

{% if culture.history_interest_pml %}
:strong:`History Interest`
  {{ conf.history_interest_pml }} {{ culture.history_interest_pml }}{% endif %}

{% if culture.migration_pml %}
:strong:`Migration`
  {{ conf.migration_pml }} {{ culture.migration_pml }}{% endif %}

{% if calendar.skip_year_0 %}
:strong:`Skip Year`
  {{ conf.skip_year_0 }} {{ calendar.skip_year_0 }}{% endif %}

{% if calendar.fragments %}
:strong:`Calendar Fragments`
  {{ conf.fragments }} {{ calendar.fragments }}{% endif %}


City Settings
=============

The following parameters are set for cities. Each impacts gameplay in some fashion.

{% if parameters.add_to_size_limit %}
:strong:`Add Size Limit`
  {{ conf.add_to_size_limit }} {{ parameters.add_to_size_limit }}{% endif %}

{% if parameters.angry_citizens %}
:strong:`Angry Citizens`
  {{ conf.angry_citizens }} {{ parameters.angry_citizens }}{% endif %}

{% if parameters.celebrate_size_limit %}
:strong:`Celebrate Size Limit`
  {{ conf.celebrate_size_limit }} {{ parameters.celebrate_size_limit }}{% endif %}

{% if parameters.changable_budget %}
:strong:`National Budget`
  {{ conf.changable_budget }} {{ parameters.changable_budget }}{% endif %}

{% if parameters.forced_science %}
:strong:`Forced Science`
  {{ conf.forced_science }} {{ parameters.forced_science }}{% endif %}

{% if parameters.forced_luxury %}
:strong:`Forced Luxury Goods`
  {{ conf.forced_luxury }} {{ parameters.forced_luxury }}{% endif %}

{% if parameters.forced_gold %}
:strong:`Forced Tax`
  {{ conf.forced_gold }} {{ parameters.forced_gold }}{% endif %}

{% if parameters.vision_reveal_tiles %}
:strong:`Vision Reveal`
  {{ conf.vision_reveal_tiles }} {{ parameters.vision_reveal_tiles }}{% endif %}

{% if citizen.nationality %}
:strong:`Nationality`
  {{ conf.nationality }} {{ citizen.nationality }}{% endif %}

{% if citizen.convert_speed %}
:strong:`Citizen Convert Speed`
  {{ conf.convert_speed }} {{ citizen.convert_speed }}{% endif %}

{% if citizen.partisans_pct %}
:strong:`Partisans`
  {{ conf.partisans_pct }} {{ citizen.partisans_pct }}{% endif %}

{% if citizen.conquest_convert_pct %}
:strong:`Conquest Convert`
  {{ conf.conquest_convert_pct }} {{ citizen.conquest_convert_pct }}{% endif %}

{% if missing_unit_upkeep.food_protected %}
:strong:`Food Protected`
  {{ conf.food_protected }} {{ missing_unit_upkeep.food_protected }}{% endif %}

{% if missing_unit_upkeep.food_unit_act %}
:strong:`Food Action`
  {{ conf.food_unit_act }} {{ missing_unit_upkeep.food_unit_act }}{% endif %}

{% if missing_unit_upkeep.food_wipe %}
:strong:`Food Wipe`
  {{ conf.food_wipe }} {{ missing_unit_upkeep.food_wipe }}{% endif %}

{% if missing_unit_upkeep.gold_protected %}
:strong:`Gold Protected`
  {{ conf.gold_protected }} {{ missing_unit_upkeep.gold_protected }}{% endif %}

{% if missing_unit_upkeep.gold_unit_act %}
:strong:`Gold Action`
  {{ conf.gold_unit_act }} {{ missing_unit_upkeep.gold_unit_act }}{% endif %}

{% if missing_unit_upkeep.gold_wipe %}
:strong:`Gold Wipe`
  {{ conf.gold_wipe }} {{ missing_unit_upkeep.gold_wipe }}{% endif %}

{% if missing_unit_upkeep.shield_protected %}
:strong:`Shield Protected`
  {{ conf.shield_protected }} {{ missing_unit_upkeep.shield_protected }}{% endif %}

{% if missing_unit_upkeep.shield_unit_act %}
:strong:`Shield Action`
  {{ conf.shield_unit_act }} {{ missing_unit_upkeep.shield_unit_act }}{% endif %}

{% if missing_unit_upkeep.shield_wipe %}
:strong:`Shield Wipe`
  {{ conf.shield_wipe }} {{ missing_unit_upkeep.shield_wipe }}{% endif %}
