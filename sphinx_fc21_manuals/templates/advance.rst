..
    SPDX-License-Identifier: GPL-3.0-or-later
    SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

{{ advance.name }}
**************************

{{ advance.helptext | clean_string }}

Properties
==========

:strong:`Cost:` {{ advance.cost }} Bulbs

:strong:`Requires:`
{% for req in advance.reqs %}
  * :doc:`{{ req.name | make_slug }}`{% else %}
  * This advance does not have any requirements.
{% endfor %}

:strong:`Hard Requirement:`
{% if advance.root_req %}
  * :doc:`{{ advance.root_req.name | make_slug }}`
{% else %}
  * This advance does not have any hard requirements.{% endif %}

:strong:`Required by:`
{% for req in required_by %}
  * :doc:`{{ req.name | make_slug }}`{% else %}
  * This advance is not required by any other advances.{% endfor %}

:strong:`Hard Requirement By:`
{% for req in hard_required_by %}
  * :doc:`{{ req.name | make_slug }}`{% else %}
  * This advance is not hard required by any other advances.{% endfor %}

:strong:`Required to Build:`
{% if required_by_units %}{% for unit_type in required_by_units | sort %}
  * :doc:`../units/{{ unit_type.name | make_slug }}`{% endfor %}{% else %}
  * No unit type requires this technology.
{% endif %}

:strong:`Flags:`
{% if advance.flags %}{% for flag in advance.flags | sort %}
  * ``{{ flag }}``{% endfor %}{% else %}
  * This advance does not have any flags.{% endif %}

.. todo:: Add helptext for the flags.

:strong:`Bonus Message:` {% if advance.bonus_message %}{{ advance.bonus_message }}{% else %}None.{% endif %}
