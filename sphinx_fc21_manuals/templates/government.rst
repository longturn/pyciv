..
    SPDX-License-Identifier: GPL-3.0-or-later
    SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

{{ government.name }}
**************************

{{ government.helptext | clean_string }}

:strong:`Male Leader Name:` {{ government.ruler_male_title | clean_string }}

:strong:`Female Leader Name:` {{ government.ruler_female_title | clean_string }}

:strong:`AI Better` = {{ government.ai_better }}

  {{ government.ai_better_help_rst }}

:strong:`Requirements:`
{% if government.reqs %}
  .. csv-table::
   :header: "Type", "Name", "Range", "Present", "Survives", "Quiet"
   {% for req in government.reqs %}
   "{{ req.type }}","{{ req.name }}","{{ req.range }}","{{ req.present }}","{{ req.survives }}","{{ req.quiet }}"{% endfor %}
   {% else %}  This government has no requirements.
{% endif %}
