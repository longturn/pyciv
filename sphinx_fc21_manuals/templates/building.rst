..
    SPDX-License-Identifier: GPL-3.0-or-later
    SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

.. Custom Interpretive Text Roles for longturn.net/Freeciv21
.. role:: unit
.. role:: improvement
.. role:: wonder

{{ building.name }}
***************************



.. image:: ../../../../../data/tilesets/{% if building.genus == "Improvement" or building.genus == "Special" %}buildings{% else %}wonders{% endif %}/{{ building.graphic[2:100] }}.png
    :scale: 130%
    :alt: {{ building.graphic[2:100] }}


{{ building.helptext | clean_string }}


:strong:`Type:` {{ building.genus }}

:strong:`Build Cost:` {{ building.build_cost }} Shields

:strong:`Upkeep:` {{ building.upkeep }} Gold / Turn

:strong:`Sabotage Cost:` {{ building.sabotage }} Gold

{% set rows = building.reqs | length %}{% if rows == 1 %}:strong:`Requirement:`{% else %}:strong:`Requirements:`{% endif %}
{% if building.reqs %}
  .. csv-table::
   :header: "Type", "Name", "Range", "Present", "Survives", "Quiet"
   {% for req in building.reqs %}
   "{{ req.type }}","{{ req.name }}","{{ req.range }}","{{ req.present }}","{{ req.survives }}","{{ req.quiet }}"{% endfor %}
   {% else %}  This improvement does not have any requirements.
{% endif %}

:strong:`Obsoleted By:`
{% if building.obsolete_by %}
  .. csv-table::
   :header: "Type", "Name", "Range", "Present", "Survives", "Quiet"
   {% for req in building.obsolete_by %}
   "{{ req.type }}","{{ req.name }}","{{ req.range }}","{{ req.present }}","{{ req.survives }}","{{ req.quiet }}"{% endfor %}
   {% else %}  This improvement is not obsoleted by anything.
{% endif %}

:strong:`Flags:` {{ building.flags }}
