{{ about.name|title }} Manual
{{ about.name.heading }}

{% if about.version %}{{ about.name|title }} Version: {{ about.version }}{{ about.version_help_rst }}{% endif %}

General Game Information
========================

:strong:`Ruleset Summary`: {{ about.summary }}

{% if about.description %}:strong:`Ruleset Description`: {{ about.description }}{% endif %}
{% if about.capabilities %}
:strong:`Capabilities`
  {{ about.capabilities_help_rst }}{ about.capabilities }}{% endif %}
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

{% if civ_style.granary_food_ini %}
:strong:`Granary Food Initial`
  {{ civ_style.granary_food_ini_help_rst }}{{ civ_style.granary_food_ini }}{% endif %}
{% if civ_style.granary_food_inc %}
:strong:`Granary Food Increment`
  {{ civ_style.granary_food_inc_help_rst }}{{ civ_style.granary_food_inc }}{% endif %}
{% if civ_style.min_city_center_food %}
:strong:`City Center: Food`
  {{ civ_style.min_city_center_food_help_rst }}{{ civ_style.min_city_center_food }}{% endif %}
{% if civ_style.min_city_center_shield %}
:strong:`City Center: Shields`
  {{ civ_style.min_city_center_shield_help_rst }}{{ civ_style.min_city_center_shield }}{% endif %}
{% if civ_style.init_city_radius_sq %}
:strong:`Initial City Radius`
  {{ civ_style.init_city_radius_sq_help_rst }}{{ civ_style.init_city_radius_sq }}{% endif %}
{% if civ_style.init_vis_radius_sq %}
:strong:`Initial City Vision Radius`
  {{ civ_style.init_vis_radius_sq_help_rst }}{{ civ_style.init_vis_radius_sq }}{% endif %}
{% if civ_style.upgrade_veteran_loss %}
:strong:`Unit Upgrade Veteran Level Loss`
  {{ civ_style.upgrade_veteran_loss_help_rst }}{{ civ_style.upgrade_veteran_loss }}{% endif %}
{% if civ_style.autoupgrade_veteran_loss %}
:strong:`Autoupgrade Unit Veteran Level Loss`
  {{ civ_style.autoupgrade_veteran_loss_help_rst }}{{ civ_style.autoupgrade_veteran_loss }}{% endif %}
{% if civ_style.pillage_select %}
:strong:`Pillage`
  {{ civ_style.pillage_select_help_rst }}{{ civ_style.pillage_select }}{% endif %}
{% if civ_style.tech_steal_allow_holes %}
:strong:`Technology Steal`
  {{ civ_style.tech_steal_allow_holes_help_rst }}{{ civ_style.tech_steal_allow_holes }}{% endif %}
{% if civ_style.tech_trade_allow_holes %}
:strong:`Technology Trade`
  {{ civ_style.tech_trade_allow_holes_help_rst }}{{ civ_style.tech_trade_allow_holes }}{% endif %}
{% if civ_style.tech_trade_loss_allow_holes %}
:strong:`Technology Trade Allow Holes`
  {{ civ_style.tech_trade_loss_allow_holes_help_rst }}{{ civ_style.tech_trade_loss_allow_holes }}{% endif %}
{% if civ_style.tech_parasite_allow_holes %}
:strong:`Technology Parasite Allow Hles`
  {{ civ_style.tech_parasite_allow_holes_help_rst }}{{ civ_style.tech_parasite_allow_holes }}{% endif %}
{% if civ_style.tech_loss_allow_holes %}
:strong:`Technology Loss Allow Holes`
  {{ civ_style.tech_loss_allow_holes_help_rst }}{{ civ_style.tech_loss_allow_holes }}{% endif %}
{% if civ_style.initial_diplomatic_state %}
:strong:`Initial Diplomatic State`
  {{ civ_style.initial_diplomatic_state_help_rst }}{{ civ_style.initial_diplomatic_state }}{% endif %}
{% if civ_style.civil_war_enabled %}
:strong:`Civil War`
  {{ civ_style.civil_war_enabled_help_rst }}{{ civ_style.civil_war_enabled }}{% endif %}
{% if civ_style.civil_war_bonus_celebrating %}
:strong:`Civil War Celebration`
  {{ civ_style.civil_war_bonus_celebrating_help_rst }}{{ civ_style.civil_war_bonus_celebrating }}{% endif %}
{% if civ_style.civil_war_bonus_unhappy %}
:strong:`Civil War Unhappiness`
  {{ civ_style.civil_war_bonus_unhappy_help_rst }}{{ civ_style.civil_war_bonus_unhappy }}{% endif %}
{% if civ_style.gameloss_style %}
:strong:`End Game`
  {{ civ_style.gameloss_style_help_rst }}{{ civ_style.gameloss_style }}{% endif %}
{% if civ_style.gold_upkeep_style %}
:strong:`Gold Upkeep`
  {{ civ_style.gold_upkeep_style_help_rst }}{{ civ_style.gold_upkeep_style }}{% endif %}
