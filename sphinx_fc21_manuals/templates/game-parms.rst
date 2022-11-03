.. Custom Interpretive Text Roles for longturn.net/Freeciv21
.. role:: unit
.. role:: improvement
.. role:: wonder

Gameplay Parameters
===================

The following game parameters are set. Each impacts gameplay in some fashion.

{% if civ_style.base_pollution %}
:strong:`Base Pollution = {{ civ_style.base_pollution }}`
  {{ civ_style.base_pollution_help_rst }}{% endif %}
{% if civ_style.happy_cost %}
:strong:`Happy Cost = {{ civ_style.happy_cost }}`
  {{ civ_style.happy_cost_help_rst }}{% endif %}
{% if civ_style.food_cost %}
:strong:`Food Cost = {{ civ_style.food_cost }}`
  {{ civ_style.food_cost_help_rst }}{% endif %}
{% if civ_style.granary_food_ini %}
:strong:`Granary Food Sizes by City Size`
  {{ civ_style.granary_food_ini_help_rst }}

  {{ civ_style.granary_food_ini | list_to_uobullet }}{% endif %}
{% if civ_style.granary_food_inc %}
:strong:`Granary Size Increment = {{ civ_style.granary_food_inc }}`
  {{ civ_style.granary_food_inc_help_rst }}{% endif %}
{% if civ_style.min_city_center_food %}
:strong:`City Center: Food = {{ civ_style.min_city_center_food }}`
  {{ civ_style.min_city_center_food_help_rst }}{% endif %}
{% if civ_style.min_city_center_shield %}
:strong:`City Center: Shields = {{ civ_style.min_city_center_shield }}`
  {{ civ_style.min_city_center_shield_help_rst }}{% endif %}
{% if civ_style.min_city_center_trade %}
:strong:`City Center: Trade = {{ civ_style.min_city_center_trade }}`
  {{ civ_style.min_city_center_trade_help_rst }}{% endif %}
{% if civ_style.init_city_radius_sq %}
:strong:`Initial City Working Area = {{ civ_style.init_city_radius_sq }}`
  {{ civ_style.init_city_radius_sq_help_rst }}{% endif %}
{% if civ_style.init_vis_radius_sq %}
:strong:`Initial City Vision Area = {{ civ_style.init_vis_radius_sq }}`
  {{ civ_style.init_vis_radius_sq_help_rst }}{% endif %}
{% if civ_style.base_bribe_cost %}
:strong:`Base Bribe Cost = {{ civ_style.base_bribe_cost }}`
  {{ civ_style.base_bribe_cost_help_rst }}{% endif %}
{% if civ_style.ransom_gold %}
:strong:`Ransom Gold = {{ civ_style.ransom_gold }}`
  {{ civ_style.ransom_gold_help_rst }}{% endif %}
{% if civ_style.upgrade_veteran_loss %}
:strong:`Unit Upgrade Veteran Level Loss = {{ civ_style.upgrade_veteran_loss }}`
  {{ civ_style.upgrade_veteran_loss_help_rst }}{% endif %}
{% if civ_style.autoupgrade_veteran_loss %}
:strong:`Autoupgrade Unit Veteran Level Loss = {{ civ_style.autoupgrade_veteran_loss }}`
  {{ civ_style.autoupgrade_veteran_loss_help_rst }}{% endif %}
{% if civ_style.pillage_select %}
:strong:`Pillage Select = {{ civ_style.pillage_select }}`
  {{ civ_style.pillage_select_help_rst }}{% endif %}
{% if civ_style.tech_steal_allow_holes %}
:strong:`Technology Steal Allow Holes = {{ civ_style.tech_steal_allow_holes }}`
  {{ civ_style.tech_steal_allow_holes_help_rst }}{% endif %}
{% if civ_style.tech_trade_allow_holes %}
:strong:`Technology Trade Allow Holes = {{ civ_style.tech_trade_allow_holes }}`
  {{ civ_style.tech_trade_allow_holes_help_rst }}{% endif %}
{% if civ_style.tech_trade_loss_allow_holes %}
:strong:`Technology Trade Loss Allow Holes = {{ civ_style.tech_trade_loss_allow_holes }}`
  {{ civ_style.tech_trade_loss_allow_holes_help_rst }}{% endif %}
{% if civ_style.tech_parasite_allow_holes %}
:strong:`Technology Parasite Allow Holes = {{ civ_style.tech_parasite_allow_holes }}`
  {{ civ_style.tech_parasite_allow_holes_help_rst }}{% endif %}
{% if civ_style.tech_loss_allow_holes %}
:strong:`Technology Loss Allow Holes = {{ civ_style.tech_loss_allow_holes }}`
  {{ civ_style.tech_loss_allow_holes_help_rst }}{% endif %}
{% if civ_style.initial_diplomatic_state %}
:strong:`Initial Diplomatic State = {{ civ_style.initial_diplomatic_state }}`
  {{ civ_style.initial_diplomatic_state_help_rst }}{% endif %}
{% if civ_style.civil_war_enabled %}
:strong:`Civil War = {{ civ_style.civil_war_enabled }}`
  {{ civ_style.civil_war_enabled_help_rst }}{% endif %}
{% if civ_style.civil_war_bonus_celebrating %}
:strong:`Civil War Celebration = {{ civ_style.civil_war_bonus_celebrating }}`
  {{ civ_style.civil_war_bonus_celebrating_help_rst }}{% endif %}
{% if civ_style.civil_war_bonus_unhappy %}
:strong:`Civil War Unhappiness = {{ civ_style.civil_war_bonus_unhappy }}`
  {{ civ_style.civil_war_bonus_unhappy_help_rst }}{% endif %}
{% if civ_style.gameloss_style %}
:strong:`End Game = {{ civ_style.gameloss_style }}`
  {{ civ_style.gameloss_style_help_rst }}{% endif %}
{% if civ_style.paradrop_to_transport %}
:strong:`Paradrop to Transport = {{ civ_style.paradrop_to_transport }}`
  {{ civ_style.paradrop_to_transport_help_rst }}{% endif %}
{% if civ_style.gold_upkeep_style %}
:strong:`Gold Upkeep = {{ civ_style.gold_upkeep_style }}`
  {{ civ_style.gold_upkeep_style_help_rst }}{% endif %}
{% if civ_style.output_granularity %}
:strong:`Output Granularity = {{ civ_style.output_granularity }}`
  {{ civ_style.output_granularity_help_rst }}{% endif %}
{% if civ_style.min_dist_bw_cities %}
:strong:`Minimum Distance Between Cities = {{ civ_style.min_dist_bw_cities }}`
  {{ civ_style.min_dist_bw_cities_help_rst }}{% endif %}

