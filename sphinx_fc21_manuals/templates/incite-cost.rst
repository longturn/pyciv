..
    SPDX-License-Identifier: GPL-3.0-or-later
    SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

.. Custom Interpretive Text Roles for longturn.net/Freeciv21
.. role:: unit
.. role:: improvement
.. role:: wonder

City Incite Cost Settings
=========================

{% if incite_cost.improvement_factor %}
:strong:`Unit Incite Cost Factors`
  {{ incite_cost.improvement_factor_help_rst }}

  The values for this ruleset are:

  * Base Incite Cost: ``{{ incite_cost.base_incite_cost }}``
  * Improvement Factor: ``{{ incite_cost.improvement_factor }}``
  * Unit Factor: ``{{ incite_cost.unit_factor }}``
  * Total Factor: ``{{ incite_cost.total_factor }}``
  {% endif %}
