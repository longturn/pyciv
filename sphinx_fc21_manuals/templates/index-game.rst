..
    SPDX-License-Identifier: GPL-3.0-or-later
    SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

.. Custom Interpretive Text Roles for longturn.net/Freeciv21
.. role:: unit
.. role:: improvement
.. role:: wonder

{{ about.name | title }} Manual
*******************************

{% if about.version %}
{{ about.name | title }} Version: ``{{ about.version }}``{{ about.version_help_rst }}
{% endif %}

General Game Information
========================

:strong:`Ruleset Summary:` {{ about.summary | clean_string }}

{% if about.capabilities %}
:strong:`Capabilities:`
  {{ about.capabilities_help_rst }}``{{ about.capabilities }}``
{% endif %}
{% if options.global_init_techs %}
:strong:`Start Technologies:`
  {{ options.global_init_techs_help_rst }}

  {{ options.global_init_techs  | list_to_uobullet }}{% endif %}
{% if options.global_init_buildings %}
:strong:`Start Buildings:`
  {{ options.global_init_buildings_help_rst }}

  {{ options.global_init_buildings | list_to_uobullet }}{% endif %}
{% if tileset.preferred %}
:strong:`Preferred Tileset:`
  {{ tileset.preferred_help_rst }}{{ tileset.preferred }}{% endif %}
{% if soundset.preferred %}
:strong:`Preferred Soundset:`
  {{ soundset.preferred_help_rst }}{{ soundset.preferred }}{% endif %}
{% if musicset.preferred %}
:strong:`Preferred Musicset:`
  {{ musicset.preferred_help_rst }}{{ musicset.preferred }}{% endif %}
:strong:`Government Status During Revolution:` {{ gov_parms.during_revolution }}


Game Settings
=============

The following pages give details of all the settings for this ruleset:

.. toctree::
  description.rst
  game-parms.rst
  plague.rst
  incite-cost.rst
  unit-rules.rst
  borders.rst
  research.rst
  culture.rst
  calendar.rst
  city.rst
  :maxdepth: 1


Ruleset Features
================

Here are links to other features of this ruleset:

.. toctree::
  advances.rst
  buildings.rst
  unit-types.rst
  unit-classes.rst
  :maxdepth: 1
