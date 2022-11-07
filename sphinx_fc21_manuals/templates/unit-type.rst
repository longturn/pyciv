{{ unit_type.name }}
********************

.. image:: ../../../../../data/tilesets/units/{{ unit_type.graphic[2:100] }}.png
    :scale: 150%
    :alt: {{ unit_type.graphic[2:100] }}

{{ unit_type.helptext | clean_string }}

Properties
==========

.. hlist::
  :columns: 3

  * :strong:`Attack:` {{ unit_type.attack }}
  * :strong:`Defense:` {{ unit_type.defense }}
  * :strong:`Firepower:` {{ unit_type.firepower }}
  * :strong:`Hit Points:` {{ unit_type.hitpoints }}
  * :strong:`Vision:` {{ unit_type.vision_radius_sq }}
  * :strong:`Move Points:`{% if unit_type.move_rate <= 1 %} {{ unit_type.move_rate }} tile/turn{% else %} {{ unit_type.move_rate }} tiles/turn{% endif %}
  * :strong:`Fuel:`{% if unit_type.fuel == 0 %} Unlimited Fuel{% elif unit_type.fuel == 1 %} 1 turn{% else %} {{ unit_type.fuel }} turns{% endif %}
  * :strong:`Build Cost:` {{ unit_type.build_cost }} shields{% if unit_type.pop_cost == 1 %}, and 1 citizen{% elif unit_type.pop_cost > 1 %}, and {{ unit_type.pop_cost }} citizens{% endif %}
  * :strong:`Upkeep:`{% if unit_type.uk_shield == 1 %} {{ unit_type.uk_shield }} shield{% elif unit_type.uk_shield > 1 %}{{ unit_type.uk_shield }} shields{% endif %}, {{ unit_type.uk_food }} food, {{ unit_type.uk_gold }} gold per turn.
  * :strong:`Unit Class:` :doc:`../unit-classes/{{ unit_type.uclass | make_slug }}`


.. todo:: ``unit_type.uclass.name`` generates an error, however ``unit_type.uclass`` does `work`. It produces duplicate text in the link. See Unit Class above and Obsoleted By below.

{% if obsolete %}* :strong:`Obsoletes:`{% for obs_unit_type in obsolete | sort %} :doc:`{{ obs_unit_type.name | make_slug }}`{% endfor %}
{% endif %}

{% if unit_type.tech_req %}* :strong:`Required Technology:`{% for req in unit_type.tech_req | sort %} :doc:`../advances/{{ req | make_slug }}`{% endfor %}{% else %} This unit does not have a technology requirement.{% endif %}

:strong:`Targets:`
{% for tgt in unit_type.targets | sort %}
* :doc:`{{ tgt | make_slug }}{% else %}
* No targets for this unit.{% endfor %}

:strong:`Obsoleted by:`
{% if unit_type.obsolete_by %}
* :doc:`{{ unit_type.obsolete_by | make_slug }}`{% else %}
* Never obsolete.{% endif %}

{% if unit_type.transport_cap %}
:strong:`Transport Capacity:`{% if unit_type.transport_cap == 1 %} Can carry up to 1 unit.{% elif unit_type.transport_cap > 1 %} Can carry up to {{ unit_type.transport_cap }} units.{% endif %}{% endif %}
{% if unit_type.cargo %}
:strong:`Transport Allowed Classes:`
{% for cargo in unit_type.cargo | sort %}
* :doc:`../unit-classes/{{ cargo | make_slug }}`{% endfor %}{% endif %}

Veteran levels
==============

.. csv-table::
   :header: "Level Name", "In Combat Chance", "When Working Chance", "Strength Bonus", "Mobility Bonus"

   {% for level in unit_type.veteran_levels %}
   "{{ level.name | title }}","{{ level.base_raise_chance }}%","{{ level.work_raise_chance }}%","{{ level.power_factor }}%","{{ level.move_bonus }}%"{% endfor %}


Flags
====={% if unit_type.flags %}
{% for flag in unit_type.flags | sort %}
* ``{{ flag }}``{% endfor %}{% else %}
* This unit has no flags.{% endif %}

.. todo:: Add helptext for all of the flags

Roles
====={% if unit_type.roles %}
{% for role in unit_type.roles | sort %}
* ``{{ role }}``{% endfor %}{% else %}
* This unit has no roles.{% endif %}

.. todo:: Add helptext for all of the roles
