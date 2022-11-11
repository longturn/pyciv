..
    SPDX-License-Identifier: GPL-3.0-or-later
    SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

.. Custom Interpretive Text Roles for longturn.net/Freeciv21
.. role:: unit
.. role:: improvement
.. role:: wonder

Unit Rules
==========

Combat Rules
------------

{% if combat_rules.incite_gold_capt_chance %}
:strong:`Incite Gold Capture Chance = {{ combat_rules.incite_gold_capt_chance }}%`
  {{ combat_rules.incite_gold_capt_chance_help_rst }}{% endif %}
{% if combat_rules.incite_gold_loss_chance %}
:strong:`Incite Gold Loss Chance = {{ combat_rules.incite_gold_loss_chance }}%`
  {{ combat_rules.incite_gold_loss_chance_help_rst }}{% endif %}
{% if combat_rules.timeoutmask %}
:strong:`Timeout Mask = {{ combat_rules.timeoutmask }}`
  {{ combat_rules.timeoutmask_help_rst }}{% endif %}
{% if combat_rules.tired_attack %}
:strong:`Tired Attack = {{ combat_rules.tired_attack }}`
  {{ combat_rules.tired_attack_help_rst }}{% endif %}
{% if combat_rules.only_killing_makes_veteran %}
:strong:`Kill to Veteran = {{ combat_rules.only_killing_makes_veteran }}`
  {{ combat_rules.only_killing_makes_veteran_help_rst }}{% endif %}
{% if combat_rules.nuke_pop_loss_pct %}
:strong:`Nuke Loss = {{ combat_rules.nuke_pop_loss_pct }}%`
  {{ combat_rules.nuke_pop_loss_pct_help_rst }}{% endif %}
{% if combat_rules.nuke_defender_survival_chance_pct %}
:strong:`Nuke Defender = {{ combat_rules.nuke_defender_survival_chance_pct }}%`
  {{ combat_rules.nuke_defender_survival_chance_pct_help_rst }}{% endif %}
{% if combat_rules.killstack %}
:strong:`Kill Stack = {{ combat_rules.killstack }}`
  {{ combat_rules.killstack_help_rst }}{% endif %}


Auto Attack Rules
-----------------

{% if auto_attack.attack_actions %}
:strong:`Auto Attack`
  {{ auto_attack.attack_actions_help_rst }}

  {{ auto_attack.attack_actions | list_to_uobullet }}{% endif %}
{% if auto_attack.if_attacker %}
:strong:`If Attacker`
  {{ auto_attack.if_attacker_help_rst }}

.. csv-table::
   :header: "Type", "Name", "Range", "Present"
   {% for req in auto_attack.if_attacker %}
   "{{ req.type }}","{{ req.name }}","{{ req.range }}","{{ req.present }}"{% endfor %}

  {% endif %}
{% if auto_attack.will_never %}
:strong:`Will Never`
  {{ auto_attack.will_never_help_rst }}

  {{ auto_attack.will_never | list_to_uobullet }}
  {% endif %}


Unit Action Rules
-----------------

{% if actions.force_trade_route %}
:strong:`Trade Route = {{ actions.force_trade_route }}`
  {{ actions.force_trade_route_help_rst }}{% endif %}
{% if actions.force_capture_units %}
:strong:`Capture Units = {{ actions.force_capture_units }}`
  {{ actions.force_capture_units_help_rst }}{% endif %}
{% if actions.force_bombard %}
:strong:`Bombard = {{ actions.force_bombard }}`
  {{ actions.force_bombard_help_rst }}{% endif %}
{% if actions.force_explode_nuclear %}
:strong:`Explode Nuclear = {{ actions.force_explode_nuclear }}`
  {{ actions.force_explode_nuclear_help_rst }}{% endif %}
{% if actions.poison_empties_food_stock %}
:strong:`Empty Food Granary = {{ actions.poison_empties_food_stock }}`
  {{ actions.poison_empties_food_stock_help_rst }}{% endif %}
{% if actions.steal_maps_reveals_all_cities %}
:strong:`Reveal Cities = {{ actions.steal_maps_reveals_all_cities }}`
  {{ actions.steal_maps_reveals_all_cities_help_rst }}{% endif %}
{% if actions.help_wonder_max_range %}
:strong:`Help Build Wonder Range = {{ actions.help_wonder_max_range }}`
  {{ actions.help_wonder_max_range_help_rst }}{% endif %}
{% if actions.recycle_unit_max_range %}
:strong:`Recycle Unit Range = {{ actions.recycle_unit_max_range }}`
  {{ actions.recycle_unit_max_range_help_rst }}{% endif %}
{% if actions.bombard_max_range %}
:strong:`Bombard Range = {{ actions.bombard_max_range }}`
  {{ actions.bombard_max_range_help_rst }}{% endif %}
{% if actions.bombard_2_max_range %}
:strong:`Bombard 2 Range = {{ actions.bombard_2_max_range }}`
  {{ actions.bombard_2_max_range_help_rst }}{% endif %}
{% if actions.bombard_3_max_range %}
:strong:`Bombard 3 Range = {{ actions.bombard_3_max_range }}`
  {{ actions.bombard_3_max_range_help_rst }}{% endif %}
{% if actions.explode_nuclear_max_range %}
:strong:`Explode Nuke Range = {{ actions.explode_nuclear_max_range }}`
  {{ actions.explode_nuclear_max_range_help_rst }}{% endif %}
{% if actions.nuke_city_max_range %}
:strong:`Nuke City Range = {{ actions.nuke_city_max_range }}`
  {{ actions.nuke_city_max_range_help_rst }}{% endif %}
{% if actions.nuke_units_max_range %}
:strong:`Nuke Units Range = {{ actions.nuke_units_max_range }}`
  {{ actions.nuke_units_max_range_help_rst }}{% endif %}
{% if actions.airlift_max_range %}
:strong:`Max Airlift Range = {{ actions.airlift_max_range }}`
  {{ actions.airlift_max_range_help_rst }}{% endif %}
