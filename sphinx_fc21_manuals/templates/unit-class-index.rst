..
    SPDX-License-Identifier: GPL-3.0-or-later
    SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

Unit Classes
************

.. toctree::{% for item in unit_class_list %}
   units/{{ item | make_slug }}.rst{% endfor %}
   :maxdepth: 1
