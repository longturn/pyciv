.. Custom Interpretive Text Roles for longturn.net/Freeciv21
.. role:: unit
.. role:: improvement
.. role:: wonder

{% if calendar.start_year or calendar.skip_year_0 %}
Calendar Settings
=================

{% if calendar.start_year %}
:strong:`Year Start` = {{ calendar.start_year }}
  {{ calendar.start_year_help_rst }}{% endif %}
{% if calendar.skip_year_0 %}
:strong:`Skip Year 0` = {{ calendar.skip_year_0 }}
  {{ calendar.skip_year_0_help_rst }}{% endif %}
{% if calendar.fragments %}
:strong:`Calendar Fragments` = {{ calendar.fragments }}
  {{ calendar.fragments_help_rst }}{% endif %}
{% if calendar.fragment_name0 %}
:strong:`Calendar Fragment 1` = {{ calendar.fragment_name0 }}
  {{ calendar.fragment_name0_help_rst }}{% endif %}
{% if calendar.fragment_name1 %}
:strong:`Calendar Fragment 2` = {{ calendar.fragment_name1 }}
  {{ calendar.fragment_name1_help_rst }}{% endif %}
{% if calendar.fragment_name2 %}
:strong:`Calendar Fragment 3` = {{ calendar.fragment_name2 }}
  {{ calendar.fragment_name2_help_rst }}{% endif %}
{% if calendar.fragment_name3 %}
:strong:`Calendar Fragment 4` = {{ calendar.fragment_name3 }}
  {{ calendar.fragment_name3_help_rst }}{% endif %}
{% endif %}
