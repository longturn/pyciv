Unit Class: {{ unit_class.name }}
*********************************

Properties
==========

:strong:`Minimum Speed:`{% if unit_class.min_speed <= 1 %} {{ unit_class.min_speed }} tile/turn{% else %} {{ unit_class.min_speed }} tiles/turn{% endif %}

{% if unit_class.hp_loss_pct %}:strong:`HP Loss Per Turn:` {{ unit_class.hp_loss_pct }}%{% endif %}

:strong:`Defense on Non-Native Terrain:` {{ unit_class.non_native_def_pct }}%

:strong:`Hut Behaviour:` {{ unit_class.hut_behavior }}

.. todo:: Add help text for all the hut behaviors.

Flags
=====
{% if unit_class.flags %}{% for flag in unit_class.flags | sort %}
* ``{{ flag }}``{% endfor %}{% else %}
* This unit class has no flags.{% endif %}

.. todo:: Add help text for all the flags and what effect they give.

{% if units_in_class %}
:strong:`Units in this class:`
{% for unit in units_in_class | sort %}
* :doc:`../units/{{ unit.name | make_slug }}`{% endfor %}{% else %}
* No units are associated with this class.
{% endif %}
