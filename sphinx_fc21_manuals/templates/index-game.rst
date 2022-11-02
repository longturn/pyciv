.. Custom Interpretive Text Roles for longturn.net/Freeciv21
.. role:: unit
.. role:: improvement
.. role:: wonder

{{ about.name|title }} Manual
*****************************

{% if about.version %}
{{ about.name|title }} Version: {{ about.version }}{{ about.version_help_rst }}
{% endif %}

General Game Information
========================

:strong:`Ruleset Summary`:
{{ about.summary }}
{% if about.capabilities %}
:strong:`Capabilities`
  {{ about.capabilities_help_rst }}``{{ about.capabilities }}``
{% endif %}
{% if about.global_init_techs %}
:strong:`Start Technologies`
  {{ about.global_init_techs_help_rst }}{{ about.global_init_techs }}{% endif %}
{% if about.global_init_buildings %}
:strong:`Start Buildings`
  {{ about.global_init_buildings_help_rst }}{{ about.global_init_buildings }}{% endif %}
{% if tileset.preferred %}
:strong:`Preferred Tileset`
  {{ tileset.preferred_help_rst }}{{ tileset.preferred }}{% endif %}
{% if soundset.preferred %}
:strong:`Preferred Soundset`
  {{ soundset.preferred_help_rst }}{{ soundset.preferred }}{% endif %}
{% if musicset.preferred %}
:strong:`Preferred Musicset`
  {{ musicset.preferred_help_rst }}{{ musicset.preferred }}{% endif %}


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

Base Civilization Settings
--------------------------

{% if civ_style.base_pollution %}
:strong:`Base Pollution`
  {{ civ_style.base_pollution_help_rst }}``{{ civ_style.base_pollution }}``{% endif %}
{% if civ_style.happy_cost %}
:strong:`Happy Cost`
  {{ civ_style.happy_cost_help_rst }}``{{ civ_style.happy_cost }}``{% endif %}
{% if civ_style.food_cost %}
:strong:`Food Cost`
  {{ civ_style.food_cost_help_rst }}``{{ civ_style.food_cost }}``{% endif %}
{% if civ_style.granary_food_ini %}
:strong:`Granary Food Sizes by City Size`
  {{ civ_style.granary_food_ini_help_rst }}``{{ civ_style.granary_food_ini }}``{% endif %}
{% if civ_style.granary_food_inc %}
:strong:`Granary Size Increment`
  {{ civ_style.granary_food_inc_help_rst }}``{{ civ_style.granary_food_inc }}``{% endif %}
{% if civ_style.min_city_center_food %}
:strong:`City Center: Food`
  {{ civ_style.min_city_center_food_help_rst }}``{{ civ_style.min_city_center_food }}``{% endif %}
{% if civ_style.min_city_center_shield %}
:strong:`City Center: Shields`
  {{ civ_style.min_city_center_shield_help_rst }}``{{ civ_style.min_city_center_shield }}``{% endif %}
{% if civ_style.min_city_center_trade %}
:strong:`City Center: Trade`
  {{ civ_style.min_city_center_trade_help_rst }}``{{ civ_style.min_city_center_trade }}``{% endif %}
{% if civ_style.init_city_radius_sq %}
:strong:`Initial City Working Area`
  {{ civ_style.init_city_radius_sq_help_rst }}``{{ civ_style.init_city_radius_sq }}``{% endif %}
{% if civ_style.init_vis_radius_sq %}
:strong:`Initial City Vision Area`
  {{ civ_style.init_vis_radius_sq_help_rst }}``{{ civ_style.init_vis_radius_sq }}``{% endif %}
{% if civ_style.base_bribe_cost %}
:strong:`Base Bribe Cost`
  {{ civ_style.base_bribe_cost_help_rst }}``{{ civ_style.base_bribe_cost }}``{% endif %}
{% if civ_style.ransom_gold %}
:strong:`Ransom Gold`
  {{ civ_style.ransom_gold_help_rst }}``{{ civ_style.ransom_gold }}``{% endif %}
{% if civ_style.upgrade_veteran_loss %}
:strong:`Unit Upgrade Veteran Level Loss`
  {{ civ_style.upgrade_veteran_loss_help_rst }}``{{ civ_style.upgrade_veteran_loss }}``{% endif %}
{% if civ_style.autoupgrade_veteran_loss %}
:strong:`Autoupgrade Unit Veteran Level Loss`
  {{ civ_style.autoupgrade_veteran_loss_help_rst }}``{{ civ_style.autoupgrade_veteran_loss }}``{% endif %}
{% if civ_style.pillage_select %}
:strong:`Pillage Select`
  {{ civ_style.pillage_select_help_rst }}``{{ civ_style.pillage_select }}``{% endif %}
{% if civ_style.tech_steal_allow_holes %}
:strong:`Technology Steal Allow Holes`
  {{ civ_style.tech_steal_allow_holes_help_rst }}``{{ civ_style.tech_steal_allow_holes }}``{% endif %}
{% if civ_style.tech_trade_allow_holes %}
:strong:`Technology Trade Allow Holes`
  {{ civ_style.tech_trade_allow_holes_help_rst }}``{{ civ_style.tech_trade_allow_holes }}``{% endif %}
{% if civ_style.tech_trade_loss_allow_holes %}
:strong:`Technology Trade Loss Allow Holes`
  {{ civ_style.tech_trade_loss_allow_holes_help_rst }}``{{ civ_style.tech_trade_loss_allow_holes }}``{% endif %}
{% if civ_style.tech_parasite_allow_holes %}
:strong:`Technology Parasite Allow Hles`
  {{ civ_style.tech_parasite_allow_holes_help_rst }}``{{ civ_style.tech_parasite_allow_holes }}``{% endif %}
{% if civ_style.tech_loss_allow_holes %}
:strong:`Technology Loss Allow Holes`
  {{ civ_style.tech_loss_allow_holes_help_rst }}``{{ civ_style.tech_loss_allow_holes }}``{% endif %}
{% if civ_style.initial_diplomatic_state %}
:strong:`Initial Diplomatic State`
  {{ civ_style.initial_diplomatic_state_help_rst }}``{{ civ_style.initial_diplomatic_state }}``{% endif %}
{% if civ_style.civil_war_enabled %}
:strong:`Civil War`
  {{ civ_style.civil_war_enabled_help_rst }}``{{ civ_style.civil_war_enabled }}``{% endif %}
{% if civ_style.civil_war_bonus_celebrating %}
:strong:`Civil War Celebration`
  {{ civ_style.civil_war_bonus_celebrating_help_rst }}``{{ civ_style.civil_war_bonus_celebrating }}``{% endif %}
{% if civ_style.civil_war_bonus_unhappy %}
:strong:`Civil War Unhappiness`
  {{ civ_style.civil_war_bonus_unhappy_help_rst }}``{{ civ_style.civil_war_bonus_unhappy }}``{% endif %}
{% if civ_style.gameloss_style %}
:strong:`End Game`
  {{ civ_style.gameloss_style_help_rst }}``{{ civ_style.gameloss_style }}``{% endif %}
{% if civ_style.paradrop_to_transport %}
:strong:`Paradrop to Transport`
  {{ civ_style.paradrop_to_transport_help_rst }}``{{ civ_style.paradrop_to_transport }}``{% endif %}
{% if civ_style.gold_upkeep_style %}
:strong:`Gold Upkeep`
  {{ civ_style.gold_upkeep_style_help_rst }}``{{ civ_style.gold_upkeep_style }}``{% endif %}
{% if civ_style.output_granularity %}
:strong:`Output Granularity`
  {{ civ_style.output_granularity_help_rst }}``{{ civ_style.output_granularity }}``{% endif %}
{% if civ_style.min_dist_bw_cities %}
:strong:`Minimum Distance Between Cities`
  {{ civ_style.min_dist_bw_cities_help_rst }}``{{ civ_style.min_dist_bw_cities }}``{% endif %}


Illness (Plague) Settings
-------------------------

{% if illness.illness_on %}
:strong:`Plague`
  {{ illness.illness_on_help_rst }}``{{ illness.illness_on }}``{% endif %}
{% if illness.illness_base_factor %}
:strong:`Plague Base Factor`
  {{ illness.illness_base_factor_help_rst }}``{{ illness.illness_base_factor }}``{% endif %}
{% if illness.illness_min_size %}
:strong:`Plague Min City Size`
  {{ illness.illness_min_size_help_rst }}``{{ illness.illness_min_size }}``{% endif %}
{% if illness.illness_trade_infection %}
:strong:`Plague Follows Trade Routes`
  {{ illness.illness_trade_infection_help_rst }}``{{ illness.illness_trade_infection }}``{% endif %}
{% if illness.illness_pollution_factor %}
:strong:`Plague Pollution`
  {{ illness.illness_pollution_factor_help_rst }}``{{ illness.illness_pollution_factor }}``{% endif %}


City Incite Cost Settings
-------------------------

{% if incite_cost.improvement_factor %}
:strong:`Unit Incite Cost Factors`
  {{ incite_cost.improvement_factor_help_rst }} Base Incite Cost: ``{{ incite_cost.base_incite_cost }}``, Improvement Factor: ``{{ incite_cost.improvement_factor }}``, Unit Factor: ``{{ incite_cost.unit_factor }}``, Total Factor: ``{{ incite_cost.total_factor }}``{% endif %}


Combat Rules
------------

{% if combat_rules.incite_gold_capt_chance %}
:strong:`Incite Gold Capture Chance`
  {{ combat_rules.incite_gold_capt_chance_help_rst }}``{{ combat_rules.incite_gold_capt_chance }}``{% endif %}
{% if combat_rules.incite_gold_loss_chance %}
:strong:`Incite Gold Loss Chance`
  {{ combat_rules.incite_gold_loss_chance_help_rst }}``{{ combat_rules.incite_gold_loss_chance }}``{% endif %}
{% if combat_rules.timeoutmask %}
:strong:`Timeout Mask`
  {{ combat_rules.timeoutmask_help_rst }}``{{ combat_rules.timeoutmask }}``{% endif %}
{% if combat_rules.tired_attack %}
:strong:`Tired Attack`
  {{ combat_rules.tired_attack_help_rst }}``{{ combat_rules.tired_attack }}``{% endif %}
{% if combat_rules.only_killing_makes_veteran %}
:strong:`Kill to Veteran`
  {{ combat_rules.only_killing_makes_veteran_help_rst }}``{{ combat_rules.only_killing_makes_veteran }}``{% endif %}
{% if combat_rules.nuke_pop_loss_pct %}
:strong:`Nuke Loss`
  {{ combat_rules.nuke_pop_loss_pct_help_rst }}``{{ combat_rules.nuke_pop_loss_pct }}``{% endif %}
{% if combat_rules.nuke_defender_survival_chance_pct %}
:strong:`Nuke Defender`
  {{ combat_rules.nuke_defender_survival_chance_pct_help_rst }}``{{ combat_rules.nuke_defender_survival_chance_pct }}``{% endif %}
{% if combat_rules.killstack %}
:strong:`Kill Stack`
  {{ combat_rules.killstack_help_rst }}``{{ combat_rules.killstack }}``{% endif %}


Auto Attack Rules
-----------------

{% if auto_attack.attack_actions %}
:strong:`Auto Attack`
  {{ auto_attack.attack_actions_help_rst }}``{{ auto_attack.attack_actions }}``{% endif %}
{% if auto_attack.if_attacker %}
:strong:`If Attacker`
  {{ auto_attack.if_attacker_help_rst }}``{{ auto_attack.if_attacker }}``{% endif %}
{% if auto_attack.will_never %}
:strong:`Will Never`
  {{ auto_attack.will_never_help_rst }}``{{ auto_attack.will_never }}``{% endif %}
{% if auto_attack.ActionRange %}
:strong:`Action Range`
  {{ auto_attack.ActionRange_help_rst }}``{{ auto_attack.ActionRange }}``{% endif %}


Unit Action Rules
-----------------

{% if actions.force_trade_route %}
:strong:`Trade Route`
  {{ actions.force_trade_route_help_rst }}``{{ actions.force_trade_route }}``{% endif %}
{% if actions.force_capture_units %}
:strong:`Capture Units`
  {{ actions.force_capture_units_help_rst }}``{{ actions.force_capture_units }}``{% endif %}
{% if actions.force_bombard %}
:strong:`Bombard`
  {{ actions.force_bombard_help_rst }}``{{ actions.force_bombard }}``{% endif %}
{% if actions.force_explode_nuclear %}
:strong:`Explode Nuclear`
  {{ actions.force_explode_nuclear_help_rst }}``{{ actions.force_explode_nuclear }}``{% endif %}
{% if actions.poison_empties_food_stock %}
:strong:`Empty Food Granary`
  {{ actions.poison_empties_food_stock_help_rst }}``{{ actions.poison_empties_food_stock }}``{% endif %}
{% if actions.steal_maps_reveals_all_cities %}
:strong:`Reveal Cities`
  {{ actions.steal_maps_reveals_all_cities_help_rst }}``{{ actions.steal_maps_reveals_all_cities }}``{% endif %}
{% if actions.help_wonder_max_range %}
:strong:`Help Build Wonder Range`
  {{ actions.help_wonder_max_range_help_rst }}``{{ actions.help_wonder_max_range }}``{% endif %}
{% if actions.recycle_unit_max_range %}
:strong:`Recycle Unit Range`
  {{ actions.recycle_unit_max_range_help_rst }}``{{ actions.recycle_unit_max_range }}``{% endif %}
{% if actions.bombard_max_range %}
:strong:`Bombard Range`
  {{ actions.bombard_max_range_help_rst }}``{{ actions.bombard_max_range }}``{% endif %}
{% if actions.bombard_2_max_range %}
:strong:`Bombard 2 Range`
  {{ actions.bombard_2_max_range_help_rst }}``{{ actions.bombard_2_max_range }}``{% endif %}
{% if actions.bombard_3_max_range %}
:strong:`Bombard 3 Range`
  {{ actions.bombard_3_max_range_help_rst }}``{{ actions.bombard_3_max_range }}``{% endif %}
{% if actions.explode_nuclear_max_range %}
:strong:`Explode Nuke Range`
  {{ actions.explode_nuclear_max_range_help_rst }}``{{ actions.explode_nuclear_max_range }}``{% endif %}
{% if actions.nuke_city_max_range %}
:strong:`Nuke City Range`
  {{ actions.nuke_city_max_range_help_rst }}``{{ actions.nuke_city_max_range }}``{% endif %}
{% if actions.nuke_units_max_range %}
:strong:`Nuke Units Range`
  {{ actions.nuke_units_max_range_help_rst }}``{{ actions.nuke_units_max_range }}``{% endif %}
{% if actions.airlift_max_range %}
:strong:`Max Airlift Range`
  {{ actions.airlift_max_range_help_rst }}``{{ actions.airlift_max_range }}``{% endif %}


National Border Rules
---------------------

{% if borders.radius_sq_city %}
:strong:`Border Radius`
  {{ borders.radius_sq_city_help_rst }}``{{ borders.radius_sq_city }}``{% endif %}
{% if borders.size_effect %}
:strong:`Border Size`
  {{ borders.size_effect_help_rst }}``{{ borders.size_effect }}``{% endif %}
{% if borders.radius_sq_city_permanent %}
:strong:`Border City Range`
  {{ borders.radius_sq_city_permanent_help_rst }}``{{ borders.radius_sq_city_permanent }}``{% endif %}


Technology Research Rules
-------------------------

{% if research.tech_upkeep_style %}
:strong:`Technology Upkeep`
  {{ research.tech_upkeep_style_help_rst }}``{{ research.tech_upkeep_style }}``{% endif %}
{% if research.tech_cost_style %}
:strong:`Tech Cost Style`
  {{ research.tech_cost_style_help_rst }}``{{ research.tech_cost_style }}``{% endif %}
{% if research.base_tech_cost %}
:strong:`Base Tech Cost`
  {{ research.base_tech_cost_help_rst }}``{{ research.base_tech_cost }}``{% endif %}
{% if research.tech_leakage %}
:strong:`Technology Leakage`
  {{ research.tech_leakage_help_rst }}``{{ research.tech_leakage }}``{% endif %}
{% if research.tech_upkeep_divider %}
:strong:`Upkeep Divider`
  {{ research.tech_upkeep_divider_help_rst }}``{{ research.tech_upkeep_divider }}``{% endif %}
{% if research.free_tech_method %}
:strong:`Free Technology Method`
  {{ research.free_tech_method_help_rst }}``{{ research.free_tech_method }}``{% endif %}


Culture Victory Rules
---------------------

{% if culture.victory_min_points %}
:strong:`Culture Victory Points`
  {{ culture.victory_min_points_help_rst }}``{{ culture.victory_min_points }}``{% endif %}
{% if culture.victory_lead_pct %}
:strong:`Culture Victory Percentage Lead`
  {{ culture.victory_lead_pct_help_rst }}``{{ culture.victory_lead_pct }}``{% endif %}
{% if culture.history_interest_pml %}
:strong:`History Interest`
  {{ culture.history_interest_pml_help_rst }}``{{ culture.history_interest_pml }}``{% endif %}
{% if culture.migration_pml %}
:strong:`Migration`
  {{ culture.migration_pml_help_rst }}``{{ culture.migration_pml }}``{% endif %}


{% if calendar.start_year or calendar.skip_year_0 %}
Game Calendar Settings
----------------------
{% endif %}

{% if calendar.start_year %}
:strong:`Year Start`
  {{ calendar.start_year_help_rst }}``{{ calendar.start_year }}``{% endif %}
{% if calendar.skip_year_0 %}
:strong:`Skip Year 0`
  {{ calendar.skip_year_0_help_rst }}``{{ calendar.skip_year_0 }}``{% endif %}
{% if calendar.fragments %}
:strong:`Calendar Fragments`
  {{ calendar.fragments_help_rst }}``{{ calendar.fragments }}``{% endif %}
{% if calendar.fragment_name0 %}
:strong:`Calendar Fragment 1`
  {{ calendar.fragment_name0_help_rst }}``{{ calendar.fragment_name0 }}``{% endif %}
{% if calendar.fragment_name1 %}
:strong:`Calendar Fragment 2`
  {{ calendar.fragment_name1_help_rst }}``{{ calendar.fragment_name1 }}``{% endif %}
{% if calendar.fragment_name2 %}
:strong:`Calendar Fragment 3`
  {{ calendar.fragment_name2_help_rst }}``{{ calendar.fragment_name2 }}``{% endif %}


City Related Settings
---------------------

The following parameters are set for cities. Each impacts gameplay in some fashion.

{% if parameters.add_to_size_limit %}
:strong:`Add Size Limit`
  {{ parameters.add_to_size_limit_help_rst }}``{{ parameters.add_to_size_limit }}``{% endif %}
{% if parameters.angry_citizens %}
:strong:`Angry Citizens`
  {{ parameters.angry_citizens_help_rst }}``{{ parameters.angry_citizens }}``{% endif %}
{% if parameters.celebrate_size_limit %}
:strong:`Celebrate Size Limit`
  {{ parameters.celebrate_size_limit_help_rst }}``{{ parameters.celebrate_size_limit }}``{% endif %}
{% if parameters.changable_budget %}
:strong:`National Budget`
  {{ parameters.changable_budget_help_rst }}``{{ parameters.changable_budget }}``{% endif %}
{% if parameters.forced_science %}
:strong:`Forced Science`
  {{ parameters.forced_science_help_rst }}``{{ parameters.forced_science }}``{% endif %}
{% if parameters.forced_luxury %}
:strong:`Forced Luxury Goods`
  {{ parameters.forced_luxury_help_rst }}``{{ parameters.forced_luxury }}``{% endif %}
{% if parameters.forced_gold %}
:strong:`Forced Tax`
  {{ parameters.forced_gold_help_rst }}``{{ parameters.forced_gold }}``{% endif %}
{% if parameters.vision_reveal_tiles %}
:strong:`Vision Reveal`
  {{ parameters.vision_reveal_tiles_help_rst }}``{{ parameters.vision_reveal_tiles }}``{% endif %}
{% if citizens.nationality %}
:strong:`Nationality`
  {{ citizens.nationality_help_rst }}``{{ citizens.nationality }}``{% endif %}
{% if citizens.convert_speed %}
:strong:`Citizen Convert Speed`
  {{ citizens.convert_speed_help_rst }}``{{ citizens.convert_speed }}``{% endif %}
{% if citizens.partisans_pct %}
:strong:`Partisans`
  {{ citizens.partisans_pct_help_rst }}``{{ citizens.partisans_pct }}``{% endif %}
{% if citizens.conquest_convert_pct %}
:strong:`Conquest Convert`
  {{ citizens.conquest_convert_pct_help_rst }}``{{ citizens.conquest_convert_pct }}``{% endif %}
