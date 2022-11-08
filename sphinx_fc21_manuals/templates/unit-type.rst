..
    SPDX-License-Identifier: GPL-3.0-or-later
    SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

{{ unit_type.name }}
********************

.. image:: ../../../../../data/tilesets/units/{{ unit_type.graphic[2:100] }}.png
    :scale: 130%
    :alt: {{ unit_type.graphic[2:100] }}

{{ unit_type.helptext | clean_string }}

Unit Type Properties
====================

.. hlist::
  :columns: 3

  * :strong:`Attack:` {{ unit_type.attack }}
  * :strong:`Defense:` {{ unit_type.defense }}
  * :strong:`Firepower:` {{ unit_type.firepower }}
  * :strong:`Hit Points:` {{ unit_type.hitpoints }}
  * :strong:`Vision:` {{ unit_type.vision_radius_sq }}
  * :strong:`Move Points:`{% if unit_type.move_rate <= 1 %} {{ unit_type.move_rate }} tile/turn{% else %} {{ unit_type.move_rate }} tiles/turn{% endif %}
  * :strong:`Fuel:`{% if unit_type.fuel == 0 %} Unlimited{% elif unit_type.fuel == 1 %} 1 turn{% else %} {{ unit_type.fuel }} turns{% endif %}
  * :strong:`Build Cost:Shields` {{ unit_type.build_cost }} shields
  {% if unit_type.pop_cost >= 1 %}* :strong:`Build Cost: Citizens`{% if unit_type.pop_cost == 1 %} 1 citizen{% elif unit_type.pop_cost > 1 %} {{ unit_type.pop_cost }} citizens{% endif %}{% endif %}
  * :strong:`Upkeep: Food` {{ unit_type.uk_food }} food
  * :strong:`Upkeep: Gold` {{ unit_type.uk_gold }} gold
  * :strong:`Upkeep: Shield`{% if unit_type.uk_shield == 1 %} {{ unit_type.uk_shield }} shield{% elif unit_type.uk_shield > 1 %}{{ unit_type.uk_shield }} shields{% endif %}
  * :strong:`Gov Required:`{% if unit_type.gov_req %} {{ unit_type.gov_req }}{% else %} None{% endif %}
  * :strong:`Unit Class:` :doc:`{{ unit_type.uclass.name | make_slug }}`
  * :strong:`Converts To:`{% if unit_type.convert_to %} {{ unit_type.convert_to }} in {{ unit_type.convert_time }} turns{% else %} None{% endif %}


:strong:`Obsoletes:`{% if obsolete %}
  {% for obs_unit_type in obsolete | sort %}
  :doc:`{{ obs_unit_type.name | make_slug }}`{% endfor %}{% else %}
  This unit does not obsolete another unit.{% endif %}

:strong:`Required Technology:`{% if unit_type.tech_req %}
  {% for req in unit_type.tech_req | sort %}
  :doc:`../advances/{{ req.name | make_slug }}`{% endfor %}{% else %}
  This unit does not have a technology requirement.{% endif %}

:strong:`Targets:`
{% if unit_type.targets %}
{{ unit_type.targets_help_rst }}
{% for tgt in unit_type.targets | sort %}
* :doc:`{{ tgt.name | make_slug }}`{% else %}
* No targets for this unit.{% endfor %}{% endif %}

:strong:`Obsoleted by:`
{% if unit_type.obsolete_by %}
* :doc:`{{ unit_type.obsolete_by.name | make_slug }}`{% else %}
* Never obsolete.{% endif %}

{% if unit_type.transport_cap %}
:strong:`Transport Capacity:`{% if unit_type.transport_cap == 1 %} The {{ unit_type.name }} can carry up to 1 unit.{% elif unit_type.transport_cap > 1 %} The {{ unit_type.name }} can carry up to {{ unit_type.transport_cap }} units.{% endif %}{% endif %}
{% if unit_type.cargo %}
:strong:`Transport Allowed Classes:`
{% for cargo in unit_type.cargo | sort %}
* :doc:`{{ cargo.name | make_slug }}`{% endfor %}{% endif %}

:strong:`Veteran levels:`

.. csv-table::
   :header: "Level Name", "In Combat Chance", "When Working Chance", "Strength Bonus", "Mobility Bonus"
   {% for level in unit_type.veteran_levels %}
   "{{ level.name | title }}","{{ level.base_raise_chance }}%","{{ level.work_raise_chance }}%","{{ level.power_factor }}%","{{ level.move_bonus }}%"{% endfor %}


:strong:`Flags:`
{% if unit_type.flags %}
{% for flag in unit_type.flags | sort %}
* ``{{ flag }}``{% endfor %}{% else %}
* This unit has no flags.{% endif %}

.. todo:: Add helptext for all of the flags

:strong:`Roles:`
{% if unit_type.roles %}
{% for role in unit_type.roles | sort %}
* ``{{ role }}``{% endfor %}{% else %}
* This unit has no roles.{% endif %}

.. todo:: Add helptext for all of the roles
