..
    SPDX-License-Identifier: GPL-3.0-or-later
    SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

Buildings
*********

.. toctree::{% for item in building_list %}
   buildings/{{ item | make_slug }}.rst{% endfor %}
   :maxdepth: 1
