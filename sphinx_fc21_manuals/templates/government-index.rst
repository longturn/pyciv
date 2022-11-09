..
    SPDX-License-Identifier: GPL-3.0-or-later
    SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

Governments
***********

.. toctree::{% for item in governments_list %}
   governments/{{ item | make_slug }}.rst{% endfor %}
   :maxdepth: 1

