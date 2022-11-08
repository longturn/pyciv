.. Custom Interpretive Text Roles for longturn.net/Freeciv21
.. role:: unit
.. role:: improvement
.. role:: wonder

National Border Rules
=====================

{% if borders.radius_sq_city %}
:strong:`Border Radius` = {{ borders.radius_sq_city }}
  {{ borders.radius_sq_city_help_rst }}{% endif %}
{% if borders.size_effect %}
:strong:`Border Size` = {{ borders.size_effect }}
  {{ borders.size_effect_help_rst }}{% endif %}
{% if borders.radius_sq_city_permanent %}
:strong:`Border City Range` = {{ borders.radius_sq_city_permanent }}
  {{ borders.radius_sq_city_permanent_help_rst }}{% endif %}
