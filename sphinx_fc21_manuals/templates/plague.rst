..
    SPDX-License-Identifier: GPL-3.0-or-later
    SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

.. Custom Interpretive Text Roles for longturn.net/Freeciv21
.. role:: unit
.. role:: improvement
.. role:: wonder

Illness (Plague) Settings
=========================

{% if illness.illness_on %}
:strong:`Plague` = {{ illness.illness_on }}
  {{ illness.illness_on_help_rst }}{% endif %}
{% if illness.illness_base_factor %}
:strong:`Plague Base Factor` = {{ illness.illness_base_factor }}%
  {{ illness.illness_base_factor_help_rst }}{% endif %}
{% if illness.illness_min_size %}
:strong:`Plague Min City Size` = {{ illness.illness_min_size }}
  {{ illness.illness_min_size_help_rst }}{% endif %}
{% if illness.illness_trade_infection %}
:strong:`Plague Follows Trade Routes` = {{ illness.illness_trade_infection }}%
  {{ illness.illness_trade_infection_help_rst }}{% endif %}
{% if illness.illness_pollution_factor %}
:strong:`Plague Pollution` = {{ illness.illness_pollution_factor }}%
  {{ illness.illness_pollution_factor_help_rst }}{% endif %}
