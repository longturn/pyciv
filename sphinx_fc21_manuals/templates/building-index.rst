Buildings
*********

.. toctree::{% for item in building_list %}
   buildings/{{ item | make_slug }}.rst{% endfor %}
   :maxdepth: 1
