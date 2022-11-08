..
    SPDX-License-Identifier: GPL-3.0-or-later
    SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

Technology Advances
*******************

.. toctree::{% for item in advances_list %}
   advances/{{ item | make_slug }}.rst{% endfor %}
   :maxdepth: 1
