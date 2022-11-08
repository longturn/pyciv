Technology Advances
*******************

.. toctree::{% for item in advances_list %}
   advances/{{ item | make_slug }}.rst{% endfor %}
   :maxdepth: 1
