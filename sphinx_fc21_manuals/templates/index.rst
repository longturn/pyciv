..
    SPDX-License-Identifier: GPL-3.0-or-later
    SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

Freeciv21 Ruleset Manuals
*************************

.. toctree::{% for item in rulesets | sort %}
   {{ item }}/index.rst{% endfor %}
   :maxdepth: 1

Common Reference Pages
======================

.. toctree::
   Common/building_flags.rst
   Common/tech_adv_flags.rst
   Common/unit_class_flags.rst
   Common/unit_type_flags.rst
   Common/unit_type_roles.rst
   :maxdepth: 1
