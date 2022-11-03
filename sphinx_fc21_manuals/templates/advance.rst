{{ advance.name | title }}
**************************

Properties
==========

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

:strong:`Cost` {% if advance.cost %}{{ advance.cost }} bulbs.{% else %}Automatic.{% endif %}

Required to Build
=================
{% if required_by_units %}{% for unit_type in required_by_units | sort %}
  * :doc:`../units/{{ unit_type.name | make_slug }}`{% endfor %}{% else %}
  * No unit type requires this technology.
{% endif %}

Flags
=====
{% if advance.flags %}{% for flag in advance.flags | sort %}
  * ``{{ flag }}``{% endfor %}{% else %}
  * This advance does not have any flags.{% endif %}
